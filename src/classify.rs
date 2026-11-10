//! Structural test: which known rule family is a program, judged by what it does to memory
//! states that occur in real episodes (not by its accuracy, and not on random matrices).
//!
//! The rule is run on held-out episodes. Every step gives a sample (S, k, v, S'). The update is
//! fitted by least squares with four terms:
//!     S' ≈ a·S + b·(v kᵀ) + c·((S k) kᵀ) + g·((vᵀS k)·v kᵀ)
//!   linear attention        (1, b, 0, 0)        decayed: a ≠ 1
//!   delta rule, step e      (1, w, −e, 0)       gated:   (a, w, −a·e, 0)
//!   Kronecker delta rule    (1, β·c, 0, −β)
//! R² is taken over the part of the update that is not the carry a·S, so a rule that leaves the
//! memory almost unchanged cannot score well for free. A rule counts as a member of a family
//! only if R² ≥ 0.99; state-dependent gates and extra state fall below and stay "unclassified".

use crate::program::{Program, Regs};
use crate::task::Task;

pub const R2_MIN: f64 = 0.99;
const TOL: f64 = 0.05;

pub struct Fit {
    pub coef: [f64; 4],
    pub r2: f64,
    pub samples: usize,
    /// Family name without numbers; used to count rediscoveries.
    pub family: String,
}

impl Fit {
    pub fn describe(&self) -> String {
        let [a, b, c, g] = self.coef;
        format!(
            "{}  [a={a:.3} b={b:.3} c={c:.3} g={g:.3}, erase c/a={:.3}, R²={:.4}, {} steps]",
            self.family,
            if a.abs() > 1e-9 { -c / a } else { 0.0 },
            self.r2,
            self.samples
        )
    }
}

fn dot(x: &[f32], y: &[f32]) -> f64 {
    x.iter().zip(y).map(|(a, b)| (*a as f64) * (*b as f64)).sum()
}

pub fn classify(prog: &Program, task: &Task) -> Fit {
    let d = task.cfg.d;
    let eff = prog.effective();
    let mut regs = Regs::new(d);
    let mut gram = [[0.0f64; 4]; 4];
    let mut h = [0.0f64; 4];
    let (mut yy, mut samples) = (0.0f64, 0usize);
    let mut f: [Vec<f32>; 4] = std::array::from_fn(|_| vec![0.0f32; d * d]);
    let mut sk = vec![0.0f32; d];
    'episodes: for ep in &task.episodes {
        regs.reset();
        for &(ki, vi) in &ep.writes {
            let (k, v) = (task.key(ki), task.val(vi));
            f[0].copy_from_slice(&regs.m[0]);
            for i in 0..d {
                sk[i] = (0..d).map(|j| f[0][i * d + j] * k[j]).sum();
            }
            let vsk: f32 = v.iter().zip(&sk).map(|(a, b)| a * b).sum();
            for i in 0..d {
                for j in 0..d {
                    f[1][i * d + j] = v[i] * k[j];
                    f[2][i * d + j] = sk[i] * k[j];
                    f[3][i * d + j] = vsk * v[i] * k[j];
                }
            }
            regs.load(k, v);
            regs.run(&eff);
            if !regs.state_ok() {
                break 'episodes;
            }
            let y = &regs.m[0];
            for i in 0..4 {
                h[i] += dot(&f[i], y);
                for j in i..4 {
                    let g = dot(&f[i], &f[j]);
                    gram[i][j] += g;
                    gram[j][i] = gram[i][j];
                }
            }
            yy += dot(y, y);
            samples += 1;
        }
    }
    // Solve the 4×4 normal equations; terms that never occur (e.g. S ≡ 0) get coefficient 0.
    let scale = (0..4).map(|i| gram[i][i]).fold(0.0, f64::max).max(1e-30);
    let active: Vec<usize> = (0..4).filter(|&i| gram[i][i] > 1e-9 * scale).collect();
    let n = active.len();
    let mut a = vec![0.0f64; n * (n + 1)];
    for (r, &i) in active.iter().enumerate() {
        for (c, &j) in active.iter().enumerate() {
            a[r * (n + 1) + c] = gram[i][j] + if r == c { 1e-10 * scale } else { 0.0 };
        }
        a[r * (n + 1) + n] = h[i];
    }
    for c in 0..n {
        let p = (c..n).max_by(|&i, &j| a[i * (n + 1) + c].abs().total_cmp(&a[j * (n + 1) + c].abs())).unwrap();
        for j in 0..=n {
            a.swap(c * (n + 1) + j, p * (n + 1) + j);
        }
        let piv = a[c * (n + 1) + c];
        for i in 0..n {
            if i != c && piv.abs() > 0.0 {
                let fct = a[i * (n + 1) + c] / piv;
                for j in c..=n {
                    a[i * (n + 1) + j] -= fct * a[c * (n + 1) + j];
                }
            }
        }
    }
    let mut coef = [0.0f64; 4];
    for (r, &i) in active.iter().enumerate() {
        let piv = a[r * (n + 1) + r];
        coef[i] = if piv.abs() > 0.0 { a[r * (n + 1) + n] / piv } else { 0.0 };
    }
    let mut resid = yy;
    for i in 0..4 {
        resid -= 2.0 * coef[i] * h[i];
        for j in 0..4 {
            resid += coef[i] * coef[j] * gram[i][j];
        }
    }
    let carry = yy - 2.0 * coef[0] * h[0] + coef[0] * coef[0] * gram[0][0];
    let (family, r2) = if samples == 0 {
        ("invalid (state diverges)".to_string(), 0.0)
    } else if carry <= 1e-9 * yy.max(1e-30) || yy < 1e-20 {
        ("no write".to_string(), 1.0)
    } else {
        let r2 = 1.0 - resid.max(0.0) / carry;
        let [a0, _, c0, g0] = coef;
        let rel = |x: f64| if a0.abs() > 1e-9 { x / a0 } else { x };
        let gate = (a0 - 1.0).abs() > TOL;
        let (erase, kron) = (rel(c0) < -TOL, rel(g0) < -TOL);
        let odd = rel(c0) > TOL || rel(g0) > TOL; // reinforcing instead of correcting
        let name = if r2 < R2_MIN {
            "unclassified".to_string()
        } else if odd {
            "linear, not error-correcting".to_string()
        } else {
            match (erase, kron, gate) {
                (false, false, false) => "linear attention",
                (false, false, true) => "decayed linear attention",
                (true, false, false) => "delta rule",
                (true, false, true) => "gated delta rule",
                (false, true, false) => "Kronecker delta rule",
                (false, true, true) => "gated Kronecker delta rule",
                (true, true, _) => "delta + Kronecker mix",
            }
            .to_string()
        };
        (name, r2)
    };
    Fit { coef, r2, samples, family }
}

//! Hand-written reference points that are NOT programs in the search space: a ceiling and two
//! rules with a second d×d state. They are only ever printed next to results (sweep); nothing
//! here enters a population, a mutation or the fitness.

use crate::task::{Tally, Task};

/// Solve A x = b for a small dense system (Gaussian elimination, partial pivoting). A is n×n
/// row-major, b holds `m` right-hand sides as columns (n×m row-major); the solution replaces b.
fn solve(a: &mut [f64], b: &mut [f64], n: usize, m: usize) {
    for c in 0..n {
        let p = (c..n).max_by(|&i, &j| a[i * n + c].abs().total_cmp(&a[j * n + c].abs())).unwrap();
        if p != c {
            for j in 0..n {
                a.swap(c * n + j, p * n + j);
            }
            for j in 0..m {
                b.swap(c * m + j, p * m + j);
            }
        }
        let piv = a[c * n + c];
        if piv.abs() < 1e-12 {
            continue;
        }
        for i in 0..n {
            if i == c {
                continue;
            }
            let f = a[i * n + c] / piv;
            if f == 0.0 {
                continue;
            }
            for j in c..n {
                a[i * n + j] -= f * a[c * n + j];
            }
            for j in 0..m {
                b[i * m + j] -= f * b[c * m + j];
            }
        }
    }
    for c in 0..n {
        let piv = a[c * n + c];
        for j in 0..m {
            b[c * m + j] = if piv.abs() < 1e-12 { 0.0 } else { b[c * m + j] / piv };
        }
    }
}

/// Ceiling for the fixed linear readout: batch ridge regression on the latest (key, value)
/// pair of every key, S = Vᵀ (K Kᵀ + λI)⁻¹ K. Uses knowledge no online rule has (which writes
/// are stale), so it bounds every rule from above.
pub fn ridge_acc(task: &Task, lam: f32) -> f32 {
    let d = task.cfg.d;
    let mut tally = Tally::default();
    for ep in &task.episodes {
        let n = ep.queries.len();
        let mut g = vec![0.0f64; n * n];
        let mut rhs = vec![0.0f64; n * d]; // (K Kᵀ + λI)⁻¹ K, n×d
        for (i, &(ki, _)) in ep.queries.iter().enumerate() {
            for (j, &(kj, _)) in ep.queries.iter().enumerate() {
                g[i * n + j] = task.key(ki).iter().zip(task.key(kj)).map(|(a, b)| (a * b) as f64).sum();
            }
            g[i * n + i] += lam as f64;
            for c in 0..d {
                rhs[i * d + c] = task.key(ki)[c] as f64;
            }
        }
        solve(&mut g, &mut rhs, n, d);
        let mut s = vec![0.0f32; d * d];
        for (i, &(_, vi)) in ep.queries.iter().enumerate() {
            let v = task.val(vi);
            for r in 0..d {
                for c in 0..d {
                    s[r * d + c] += v[r] * rhs[i * d + c] as f32;
                }
            }
        }
        tally.readout(task, ep, &s);
    }
    tally.acc()
}

/// Delta error with a Kalman gain; keeps a second d×d state P (P₀ = I/λ):
///   g = P k / (1 + kᵀP k),  S' = S + (v − S k) gᵀ,  P' = P − g (P k)ᵀ + q·I.
/// q = 0 is recursive least squares.
pub fn kalman_acc(task: &Task, lam: f32, q: f32) -> f32 {
    let d = task.cfg.d;
    let mut tally = Tally::default();
    let (mut s, mut p) = (vec![0.0f32; d * d], vec![0.0f32; d * d]);
    let (mut pk, mut err) = (vec![0.0f32; d], vec![0.0f32; d]);
    for ep in &task.episodes {
        s.fill(0.0);
        p.fill(0.0);
        for i in 0..d {
            p[i * d + i] = 1.0 / lam;
        }
        for &(ki, vi) in &ep.writes {
            let (k, v) = (task.key(ki), task.val(vi));
            for i in 0..d {
                pk[i] = (0..d).map(|j| p[i * d + j] * k[j]).sum();
                err[i] = v[i] - (0..d).map(|j| s[i * d + j] * k[j]).sum::<f32>();
            }
            let denom = 1.0 + k.iter().zip(&pk).map(|(a, b)| a * b).sum::<f32>();
            for i in 0..d {
                for j in 0..d {
                    s[i * d + j] += err[i] * pk[j] / denom;
                    p[i * d + j] -= pk[i] * pk[j] / denom;
                }
                p[i * d + i] += q;
            }
        }
        tally.readout(task, ep, &s);
    }
    tally.acc()
}

//! Testbed 2: optimizer update rules (README, "Testbed 2: optimizer update rules", fixed
//! 21 Nov 2026 before any implementation or run).
//!
//! One step of an optimizer is a program of the same register machine as the memory rules:
//! on entry V0 = w (parameters) and V1 = g (a stochastic gradient at w); the new parameters are
//! V0 at the end of the step. Persistent state: M0 (always) and V2.. by `--persist-v`, all zero
//! at the start of an episode. Nothing here knows of any optimizer; the hand-written ladder
//! lives in `verify/probe_opt.py` as reference programs only (CLAUDE.md rule 6).
//!
//! Problems (d-dimensional, T steps, ‖w₀ − w*‖ = 1, largest curvature 1):
//!   quadratic   f(w) = ½ (w − w*)ᵀ A (w − w*),  A = Q diag(λ) Qᵀ,  λ log-uniform in [1/κ, 1],
//!               Q = I (axis-aligned) or a random rotation; g = A (w − w*) + σ ξ, ξ ~ N(0, I/d)
//!   regression  f(w) = ‖X w − y‖² / (2n), n = 64 rows with feature covariance Q diag(λ) Qᵀ,
//!               y = X w* + 0.1 ε; g is the gradient on 8 rows drawn per step
//! Every gradient is multiplied by the episode's scale (1 except in the scale suite).
//! Episode objective: log₁₀(f(w_T) / f(w₀)) clipped to [−10, 3]; 3 if w leaves |wᵢ| < 1e4
//! or is not finite at any step. Lower is better.

use crate::program::{persist_m, persist_v, Program, Regs, NM, NV};
use crate::rng::Rng;

pub const N_ROWS: usize = 64;
pub const BATCH: usize = 8;

#[derive(Clone, Debug)]
pub struct OptCfg {
    pub d: usize,
    pub t: usize,
    pub n_episodes: usize,
    pub seed: u64,
    pub kappas: Vec<f32>,
    pub sigmas: Vec<f32>,
    pub scales: Vec<f32>,
}

impl OptCfg {
    /// The train distribution of the README: d 16, T 50, κ ∈ {10, 100}, σ ∈ {0, 0.1}.
    pub fn train(seed: u64, n_episodes: usize) -> OptCfg {
        OptCfg { d: 16, t: 50, n_episodes, seed, kappas: vec![10.0, 100.0], sigmas: vec![0.0, 0.1], scales: vec![1.0] }
    }
}

/// The seven held-out suites of the README, fixed seed 99, 512 episodes each.
pub fn test_suites() -> Vec<(String, OptCfg)> {
    let b = || OptCfg::train(99, 512);
    vec![
        ("test opt train-distribution".into(), b()),
        ("test opt kappa1000".into(), OptCfg { kappas: vec![1000.0], ..b() }),
        ("test opt d32".into(), OptCfg { d: 32, ..b() }),
        ("test opt d8".into(), OptCfg { d: 8, ..b() }),
        ("test opt sigma0.3".into(), OptCfg { sigmas: vec![0.3], ..b() }),
        ("test opt T200".into(), OptCfg { t: 200, ..b() }),
        ("test opt scale10/0.1".into(), OptCfg { scales: vec![10.0, 0.1], ..b() }),
    ]
}

#[derive(Clone, Debug)]
pub enum Problem {
    /// A (d×d, row-major) and the additive gradient noise (T×d).
    Quad { a: Vec<f32>, noise: Vec<f32> },
    /// X (n×d), y (n) and the minibatch rows of each step (T×BATCH).
    Reg { x: Vec<f32>, y: Vec<f32>, batch: Vec<u16> },
}

#[derive(Clone, Debug)]
pub struct OptEpisode {
    pub d: usize,
    pub t: usize,
    pub kappa: f32,
    pub sigma: f32,
    pub rotated: bool,
    pub scale: f32,
    pub w0: Vec<f32>,
    pub wstar: Vec<f32>,
    pub prob: Problem,
    pub f0: f64,
}

pub struct OptTask {
    pub cfg: OptCfg,
    pub episodes: Vec<OptEpisode>,
}

fn orthogonal(rng: &mut Rng, d: usize) -> Vec<f32> {
    // Gram-Schmidt on a Gaussian matrix; rows are the basis vectors.
    let mut q = vec![0.0f64; d * d];
    for i in 0..d {
        let mut v: Vec<f64> = (0..d).map(|_| rng.normal() as f64).collect();
        for j in 0..i {
            let dot: f64 = (0..d).map(|k| v[k] * q[j * d + k]).sum();
            for k in 0..d {
                v[k] -= dot * q[j * d + k];
            }
        }
        let n = v.iter().map(|x| x * x).sum::<f64>().sqrt();
        for k in 0..d {
            q[i * d + k] = v[k] / n;
        }
    }
    q.iter().map(|&x| x as f32).collect()
}

impl OptTask {
    pub fn new(cfg: OptCfg) -> OptTask {
        let mut rng = Rng::new(cfg.seed ^ 0x6f70_7431_7465_7374);
        let (d, t) = (cfg.d, cfg.t);
        let (lk, ls, lsc) = (cfg.kappas.len(), cfg.sigmas.len(), cfg.scales.len());
        let mut episodes = Vec::with_capacity(cfg.n_episodes);
        for e in 0..cfg.n_episodes {
            let quad = e % 2 == 0;
            let kappa = cfg.kappas[(e / 2) % lk];
            let sigma = cfg.sigmas[(e / (2 * lk)) % ls];
            let rotated = !quad || (e / (2 * lk * ls)) % 2 == 1;
            let scale = cfg.scales[(e / (4 * lk * ls)) % lsc];
            let lam: Vec<f32> = (0..d)
                .map(|i| if i == 0 { 1.0 } else if i == d - 1 { 1.0 / kappa } else { kappa.powf(-rng.uniform()) })
                .collect();
            let q = if rotated {
                orthogonal(&mut rng, d)
            } else {
                (0..d * d).map(|i| if i / d == i % d { 1.0 } else { 0.0 }).collect()
            };
            let wstar: Vec<f32> = (0..d).map(|_| rng.normal()).collect();
            let u: Vec<f32> = (0..d).map(|_| rng.normal()).collect();
            let un = u.iter().map(|x| x * x).sum::<f32>().sqrt();
            let w0: Vec<f32> = (0..d).map(|i| wstar[i] + u[i] / un).collect();
            let prob = if quad {
                // A = Qᵀ diag(λ) Q with the rows of q as eigenvectors
                let mut a = vec![0.0f32; d * d];
                for i in 0..d {
                    for j in 0..d {
                        a[i * d + j] = (0..d).map(|k| q[k * d + i] * lam[k] * q[k * d + j]).sum();
                    }
                }
                let sd = sigma / (d as f32).sqrt();
                let noise = (0..t * d).map(|_| sd * rng.normal()).collect();
                Problem::Quad { a, noise }
            } else {
                // X = Z diag(√λ) Q: rows of Z standard normal, so E[XᵀX/n] = Qᵀ diag(λ) Q
                let mut x = vec![0.0f32; N_ROWS * d];
                for r in 0..N_ROWS {
                    let z: Vec<f32> = (0..d).map(|_| rng.normal()).collect();
                    for j in 0..d {
                        x[r * d + j] = (0..d).map(|k| z[k] * lam[k].sqrt() * q[k * d + j]).sum();
                    }
                }
                let y = (0..N_ROWS)
                    .map(|r| (0..d).map(|j| x[r * d + j] * wstar[j]).sum::<f32>() + 0.1 * rng.normal())
                    .collect();
                let batch = (0..t * BATCH).map(|_| rng.below(N_ROWS) as u16).collect();
                Problem::Reg { x, y, batch }
            };
            let mut ep = OptEpisode { d, t, kappa, sigma, rotated, scale, w0, wstar, prob, f0: 0.0 };
            ep.f0 = ep.loss(&ep.w0);
            episodes.push(ep);
        }
        OptTask { cfg, episodes }
    }

    pub fn to_json(&self) -> String {
        let fl = |v: &[f32]| v.iter().map(|x| format!("{x}")).collect::<Vec<_>>().join(",");
        let mut s = format!("{{\"task\":\"opt\",\"d\":{},\"t\":{},\"seed\":{},\"episodes\":[", self.cfg.d, self.cfg.t, self.cfg.seed);
        for (i, e) in self.episodes.iter().enumerate() {
            if i > 0 {
                s.push(',');
            }
            s += &format!(
                "{{\"kappa\":{},\"sigma\":{},\"rotated\":{},\"scale\":{},\"f0\":{},\"w0\":[{}],\"wstar\":[{}],",
                e.kappa, e.sigma, e.rotated, e.scale, e.f0, fl(&e.w0), fl(&e.wstar)
            );
            match &e.prob {
                Problem::Quad { a, noise } => s += &format!("\"kind\":\"quad\",\"a\":[{}],\"noise\":[{}]}}", fl(a), fl(noise)),
                Problem::Reg { x, y, batch } => {
                    let b = batch.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",");
                    s += &format!("\"kind\":\"reg\",\"x\":[{}],\"y\":[{}],\"batch\":[{}]}}", fl(x), fl(y), b)
                }
            }
        }
        s + "]}"
    }
}

impl OptEpisode {
    /// Exact loss in f64.
    pub fn loss(&self, w: &[f32]) -> f64 {
        let d = self.d;
        match &self.prob {
            Problem::Quad { a, .. } => {
                let e: Vec<f64> = (0..d).map(|i| (w[i] - self.wstar[i]) as f64).collect();
                let mut f = 0.0;
                for i in 0..d {
                    let ae: f64 = (0..d).map(|j| a[i * d + j] as f64 * e[j]).sum();
                    f += e[i] * ae;
                }
                0.5 * f
            }
            Problem::Reg { x, y, .. } => {
                let mut f = 0.0;
                for r in 0..N_ROWS {
                    let p: f64 = (0..d).map(|j| x[r * d + j] as f64 * w[j] as f64).sum();
                    f += (p - y[r] as f64).powi(2);
                }
                f / (2.0 * N_ROWS as f64)
            }
        }
    }

    /// Stochastic gradient of step `step` at w, times the episode's scale.
    pub fn grad(&self, w: &[f32], step: usize, out: &mut [f32]) {
        let d = self.d;
        match &self.prob {
            Problem::Quad { a, noise } => {
                for i in 0..d {
                    let ae: f32 = (0..d).map(|j| a[i * d + j] * (w[j] - self.wstar[j])).sum();
                    out[i] = self.scale * (ae + noise[step * d + i]);
                }
            }
            Problem::Reg { x, y, batch } => {
                out.iter_mut().for_each(|g| *g = 0.0);
                for &r in &batch[step * BATCH..(step + 1) * BATCH] {
                    let r = r as usize;
                    let res: f32 = (0..d).map(|j| x[r * d + j] * w[j]).sum::<f32>() - y[r];
                    for j in 0..d {
                        out[j] += res * x[r * d + j];
                    }
                }
                out.iter_mut().for_each(|g| *g *= self.scale / BATCH as f32);
            }
        }
    }

    pub fn objective(&self, w: &[f32], diverged: bool) -> f64 {
        if diverged {
            return 3.0;
        }
        (self.loss(w) / self.f0).log10().clamp(-10.0, 3.0)
    }
}

/// Result of running one program on a task.
#[derive(Clone, Debug)]
pub struct OptScore {
    /// Mean episode objective (lower is better).
    pub objective: f64,
    /// Fraction of episodes in which w diverged.
    pub diverged: f64,
    /// Largest absolute entry of the persistent state (M0, persistent V) over all steps.
    pub max_state: f32,
    #[allow(dead_code)]
    pub per_episode: Vec<f64>,
}

fn load_step(regs: &mut Regs, w: &[f32], g: &[f32]) {
    for i in 0..NM {
        if !persist_m(i) {
            regs.m[i].fill(0.0);
        }
    }
    regs.v[0].copy_from_slice(w);
    regs.v[1].copy_from_slice(g);
    for i in 2..NV {
        if !persist_v(i) {
            regs.v[i].fill(0.0);
        }
    }
    regs.s = [0.0; crate::program::NS];
}

fn state_abs(regs: &Regs) -> f32 {
    let mx = |x: &[f32]| x.iter().fold(0.0f32, |a, x| if x.is_finite() { a.max(x.abs()) } else { f32::INFINITY });
    let mut s = 0.0f32;
    for i in 0..NM {
        if persist_m(i) {
            s = s.max(mx(&regs.m[i]));
        }
    }
    for i in 2..NV {
        if persist_v(i) {
            s = s.max(mx(&regs.v[i]));
        }
    }
    s
}

/// Run one program over one episode; returns (final w, diverged, max |state|).
pub fn run_episode(prog: &Program, ep: &OptEpisode, regs: &mut Regs) -> (Vec<f32>, bool, f32) {
    regs.reset();
    let mut w = ep.w0.clone();
    let mut g = vec![0.0f32; ep.d];
    let mut mx = 0.0f32;
    for step in 0..ep.t {
        ep.grad(&w, step, &mut g);
        load_step(regs, &w, &g);
        regs.run(prog);
        w.copy_from_slice(&regs.v[0]);
        mx = mx.max(state_abs(regs));
        if !w.iter().all(|x| x.is_finite() && x.abs() < 1e4) {
            return (w, true, mx);
        }
    }
    (w, false, mx)
}

pub fn evaluate(prog: &Program, task: &OptTask) -> OptScore {
    let d = task.cfg.d;
    let mut regs = Regs::new(d);
    let mut per = Vec::with_capacity(task.episodes.len());
    let (mut div, mut mx) = (0usize, 0.0f32);
    for ep in &task.episodes {
        let (w, diverged, m) = run_episode(prog, ep, &mut regs);
        div += diverged as usize;
        mx = mx.max(m);
        per.push(ep.objective(&w, diverged));
    }
    let n = per.len().max(1) as f64;
    OptScore { objective: per.iter().sum::<f64>() / n, diverged: div as f64 / n, max_state: mx, per_episode: per }
}

/// Small dense solve (Gaussian elimination with partial pivoting) in f64.
fn solve(mut a: Vec<f64>, mut b: Vec<f64>, d: usize) -> Vec<f64> {
    for c in 0..d {
        let p = (c..d).max_by(|&i, &j| a[i * d + c].abs().total_cmp(&a[j * d + c].abs())).unwrap();
        for k in 0..d {
            a.swap(c * d + k, p * d + k);
        }
        b.swap(c, p);
        for r in c + 1..d {
            let f = a[r * d + c] / a[c * d + c];
            for k in c..d {
                a[r * d + k] -= f * a[c * d + k];
            }
            b[r] -= f * b[c];
        }
    }
    let mut x = vec![0.0; d];
    for r in (0..d).rev() {
        let s: f64 = (r + 1..d).map(|k| a[r * d + k] * x[k]).sum();
        x[r] = (b[r] - s) / a[r * d + r];
    }
    x
}

/// Ceiling references, not expressible in the space: (a) Newton steps with the exact Hessian
/// on the same stochastic gradients, w' = w − H⁻¹ g / scale; (b) the optimum itself (w* on the
/// quadratics, the least-squares solution on regression). Returns the mean objectives.
pub fn ceilings(task: &OptTask) -> (f64, f64) {
    let (mut newton, mut opt) = (0.0, 0.0);
    for ep in &task.episodes {
        let d = ep.d;
        let h: Vec<f64> = match &ep.prob {
            Problem::Quad { a, .. } => a.iter().map(|&x| x as f64).collect(),
            Problem::Reg { x, .. } => {
                let mut h = vec![0.0; d * d];
                for r in 0..N_ROWS {
                    for i in 0..d {
                        for j in 0..d {
                            h[i * d + j] += (x[r * d + i] * x[r * d + j]) as f64 / N_ROWS as f64;
                        }
                    }
                }
                h
            }
        };
        let mut w = ep.w0.clone();
        let mut g = vec![0.0f32; d];
        for step in 0..ep.t {
            ep.grad(&w, step, &mut g);
            let dw = solve(h.clone(), g.iter().map(|&x| x as f64 / ep.scale as f64).collect(), d);
            for i in 0..d {
                w[i] -= dw[i] as f32;
            }
        }
        newton += ep.objective(&w, false);
        let wopt: Vec<f32> = match &ep.prob {
            Problem::Quad { .. } => ep.wstar.clone(),
            Problem::Reg { x, y, .. } => {
                let mut xty = vec![0.0f64; d];
                for r in 0..N_ROWS {
                    for j in 0..d {
                        xty[j] += (x[r * d + j] * y[r]) as f64 / N_ROWS as f64;
                    }
                }
                solve(h.clone(), xty, d).iter().map(|&x| x as f32).collect()
            }
        };
        opt += ep.objective(&wopt, false);
    }
    let n = task.episodes.len() as f64;
    (newton / n, opt / n)
}

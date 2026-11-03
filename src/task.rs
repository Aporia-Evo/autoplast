//! Multi-query associative recall (MQAR) with overwrites.
//!
//! Each episode writes T (key, value) pairs into an empty memory S, one rule application per
//! pair. With probability `p_overwrite` a write reuses a key already written in this episode
//! but with a new value. Afterwards every distinct key is queried; the target is its most
//! recent value. Readout is the same for every rule: o = S q, decoded by the best-matching
//! value embedding. Embeddings are fixed random unit vectors (no learning outside the rule).

use crate::program::{Program, Regs};
use crate::rng::Rng;

#[derive(Clone, Debug)]
pub struct TaskCfg {
    pub d: usize,
    pub n_keys: usize,
    pub n_vals: usize,
    pub t_writes: usize,
    pub p_overwrite: f32,
    pub n_episodes: usize,
    pub seed: u64,
}

impl TaskCfg {
    pub fn search_default(seed: u64) -> TaskCfg {
        TaskCfg {
            d: 16,
            n_keys: 64,
            n_vals: 64,
            t_writes: 12,
            p_overwrite: 0.3,
            n_episodes: 96,
            seed,
        }
    }
}

pub struct Episode {
    pub writes: Vec<(usize, usize)>,  // (key id, value id)
    pub queries: Vec<(usize, usize)>, // (key id, target value id)
}

pub struct Task {
    pub cfg: TaskCfg,
    pub keys: Vec<f32>, // n_keys * d
    pub vals: Vec<f32>, // n_vals * d
    pub episodes: Vec<Episode>,
}

fn unit_vectors(rng: &mut Rng, n: usize, d: usize) -> Vec<f32> {
    let mut out = vec![0.0; n * d];
    for r in 0..n {
        let row = &mut out[r * d..(r + 1) * d];
        for x in row.iter_mut() {
            *x = rng.normal();
        }
        let norm = row.iter().map(|x| x * x).sum::<f32>().sqrt();
        for x in row.iter_mut() {
            *x /= norm;
        }
    }
    out
}

impl Task {
    pub fn new(cfg: TaskCfg) -> Task {
        let mut rng = Rng::new(cfg.seed);
        let keys = unit_vectors(&mut rng, cfg.n_keys, cfg.d);
        let vals = unit_vectors(&mut rng, cfg.n_vals, cfg.d);
        let mut episodes = Vec::with_capacity(cfg.n_episodes);
        for _ in 0..cfg.n_episodes {
            let mut writes = Vec::with_capacity(cfg.t_writes);
            let mut used: Vec<usize> = Vec::new();
            for t in 0..cfg.t_writes {
                let key = if t > 0 && rng.uniform() < cfg.p_overwrite {
                    used[rng.below(used.len())]
                } else {
                    loop {
                        let k = rng.below(cfg.n_keys);
                        if !used.contains(&k) {
                            used.push(k);
                            break k;
                        }
                    }
                };
                writes.push((key, rng.below(cfg.n_vals)));
            }
            let queries = used
                .iter()
                .map(|&k| {
                    let latest = writes.iter().rev().find(|w| w.0 == k).unwrap().1;
                    (k, latest)
                })
                .collect();
            episodes.push(Episode { writes, queries });
        }
        Task {
            cfg,
            keys,
            vals,
            episodes,
        }
    }

    fn key(&self, i: usize) -> &[f32] {
        &self.keys[i * self.cfg.d..(i + 1) * self.cfg.d]
    }
    fn val(&self, i: usize) -> &[f32] {
        &self.vals[i * self.cfg.d..(i + 1) * self.cfg.d]
    }
}

#[derive(Clone, Copy, Debug, Default)]
pub struct Score {
    pub fitness: f32,
    pub acc: f32,
    pub margin: f32,
    #[allow(dead_code)]
    pub valid: bool,
}

pub const MARGIN_WEIGHT: f32 = 0.05;
pub const LEN_PENALTY: f32 = 1e-4;

/// Evaluate a rule. `prog` should already be the effective (dead-code-free) program.
pub fn evaluate(prog: &Program, task: &Task, regs: &mut Regs) -> Score {
    let d = task.cfg.d;
    let mut s_mem = vec![0.0f32; d * d];
    let mut o = vec![0.0f32; d];
    let (mut correct, mut total, mut margin_sum) = (0usize, 0usize, 0.0f32);
    for ep in &task.episodes {
        s_mem.fill(0.0);
        for &(k, v) in &ep.writes {
            regs.load(&s_mem, task.key(k), task.val(v));
            regs.run(prog);
            let out = &regs.m[0];
            if out.iter().any(|x| !x.is_finite() || x.abs() > 1e4) {
                return Score::default();
            }
            s_mem.copy_from_slice(out);
        }
        for &(k, target) in &ep.queries {
            let q = task.key(k);
            for i in 0..d {
                o[i] = (0..d).map(|j| s_mem[i * d + j] * q[j]).sum();
            }
            let norm = o.iter().map(|x| x * x).sum::<f32>().sqrt();
            total += 1;
            if norm < 1e-6 {
                continue; // empty readout: counts as wrong, zero margin
            }
            let mut best = f32::NEG_INFINITY;
            let mut best_id = usize::MAX;
            let mut other_best = f32::NEG_INFINITY;
            let mut target_score = 0.0;
            for j in 0..task.cfg.n_vals {
                let sc: f32 = task.val(j).iter().zip(&o).map(|(a, b)| a * b).sum::<f32>() / norm;
                if sc > best {
                    best = sc;
                    best_id = j;
                }
                if j == target {
                    target_score = sc;
                } else if sc > other_best {
                    other_best = sc;
                }
            }
            if best_id == target {
                correct += 1;
            }
            margin_sum += (target_score - other_best).clamp(-1.0, 1.0);
        }
    }
    let acc = correct as f32 / total.max(1) as f32;
    let margin = margin_sum / total.max(1) as f32;
    Score {
        fitness: acc + MARGIN_WEIGHT * margin - LEN_PENALTY * prog.instrs.len() as f32,
        acc,
        margin,
        valid: true,
    }
}

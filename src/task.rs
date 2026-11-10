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
    /// Maximum number of distinct keys per episode; once reached, every further write
    /// rewrites one of them. 0 = no limit.
    pub key_pool: usize,
    /// Keys are normalize(c + cluster·u) around one shared unit centre c (u a random unit
    /// vector), so pairwise cosine is about 1/(1 + cluster²). 0 = independent random keys.
    pub cluster: f32,
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
            key_pool: 0,
            cluster: 0.0,
        }
    }

    /// Named regimes (d = 16). `base` is the v1/v2 search task; the others are the regimes
    /// where `verify/headroom.py` measured a gap between Gated DeltaNet and the ridge ceiling.
    pub fn regime(name: &str, seed: u64) -> Option<TaskCfg> {
        let b = TaskCfg::search_default(seed);
        Some(match name {
            "base" => b,
            "full" => TaskCfg { t_writes: 24, ..b },
            "overload" => TaskCfg { t_writes: 48, ..b },
            "rewrite8" => TaskCfg { t_writes: 96, key_pool: 8, ..b },
            "rewrite14" => TaskCfg { t_writes: 96, key_pool: 14, ..b },
            "clustered" => TaskCfg { cluster: 0.5, ..b },
            "clustered8" => TaskCfg { t_writes: 48, key_pool: 8, cluster: 0.5, ..b },
            _ => return None,
        })
    }
}

pub const REGIMES: [&str; 7] = ["base", "full", "overload", "rewrite8", "rewrite14", "clustered", "clustered8"];

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
        let keys = if cfg.cluster > 0.0 {
            let centre = unit_vectors(&mut rng, 1, cfg.d);
            let mut ks = unit_vectors(&mut rng, cfg.n_keys, cfg.d);
            for row in ks.chunks_mut(cfg.d) {
                for (x, c) in row.iter_mut().zip(&centre) {
                    *x = c + cfg.cluster * *x;
                }
                let norm = row.iter().map(|x| x * x).sum::<f32>().sqrt();
                for x in row.iter_mut() {
                    *x /= norm;
                }
            }
            ks
        } else {
            unit_vectors(&mut rng, cfg.n_keys, cfg.d)
        };
        let vals = unit_vectors(&mut rng, cfg.n_vals, cfg.d);
        let mut episodes = Vec::with_capacity(cfg.n_episodes);
        for _ in 0..cfg.n_episodes {
            let mut writes = Vec::with_capacity(cfg.t_writes);
            let mut used: Vec<usize> = Vec::new();
            for t in 0..cfg.t_writes {
                let full = cfg.key_pool > 0 && used.len() >= cfg.key_pool;
                let key = if t > 0 && (full || rng.uniform() < cfg.p_overwrite) {
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

    pub fn key(&self, i: usize) -> &[f32] {
        &self.keys[i * self.cfg.d..(i + 1) * self.cfg.d]
    }
    pub fn val(&self, i: usize) -> &[f32] {
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
    /// Number of queries behind `acc`.
    pub n: usize,
}

impl Score {
    /// Binomial standard error of the accuracy.
    pub fn se(&self) -> f32 {
        (self.acc * (1.0 - self.acc) / self.n.max(1) as f32).sqrt()
    }
}

pub const MARGIN_WEIGHT: f32 = 0.05;
pub const LEN_PENALTY: f32 = 1e-4;

/// Running count of correct readouts and margins. The readout is the same for every rule and
/// every reference: o = S q, decoded by the best-matching value embedding (cosine).
#[derive(Default)]
pub struct Tally {
    correct: usize,
    total: usize,
    margin_sum: f32,
}

impl Tally {
    /// Query every distinct key of the episode against memory `s_mem` (row-major d×d).
    pub fn readout(&mut self, task: &Task, ep: &Episode, s_mem: &[f32]) {
        let d = task.cfg.d;
        let mut o = vec![0.0f32; d];
        for &(k, target) in &ep.queries {
            let q = task.key(k);
            for i in 0..d {
                o[i] = (0..d).map(|j| s_mem[i * d + j] * q[j]).sum();
            }
            let norm = o.iter().map(|x| x * x).sum::<f32>().sqrt();
            self.total += 1;
            if norm < 1e-6 || !norm.is_finite() {
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
                self.correct += 1;
            }
            self.margin_sum += (target_score - other_best).clamp(-1.0, 1.0);
        }
    }

    pub fn acc(&self) -> f32 {
        self.correct as f32 / self.total.max(1) as f32
    }
    pub fn margin(&self) -> f32 {
        self.margin_sum / self.total.max(1) as f32
    }
    /// Number of queries; the binomial standard error of `acc` is sqrt(acc(1-acc)/n).
    pub fn n(&self) -> usize {
        self.total
    }
}

/// Evaluate a rule. `prog` should already be the effective (dead-code-free) program.
pub fn evaluate(prog: &Program, task: &Task, regs: &mut Regs) -> Score {
    let mut tally = Tally::default();
    for ep in &task.episodes {
        regs.reset();
        for &(k, v) in &ep.writes {
            regs.load(task.key(k), task.val(v));
            regs.run(prog);
            if !regs.state_ok() {
                return Score::default();
            }
        }
        tally.readout(task, ep, &regs.m[0]);
    }
    let (acc, margin) = (tally.acc(), tally.margin());
    Score {
        fitness: acc + MARGIN_WEIGHT * margin - LEN_PENALTY * prog.instrs.len() as f32,
        acc,
        margin,
        valid: true,
        n: tally.n(),
    }
}

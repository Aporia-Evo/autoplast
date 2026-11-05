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
    /// Extra long episodes appended after the `n_episodes` standard ones (0 = none, v2 task).
    pub long_episodes: usize,
    pub long_t: usize,
    /// Cap on distinct keys per long episode; once reached, every further write overwrites.
    pub long_max_keys: usize,
    /// Stage-2 regimes (0 / 1.0 = off, v2/v3 behaviour). Keys drawn around `key_clusters`
    /// random centres with expected within-cluster cosine `cluster_cos`.
    pub key_clusters: usize,
    pub cluster_cos: f32,
    /// Query vectors are normalize(c·k + √(1−c²)·u), u a random unit vector, so cos(q, k) ≈ c;
    /// 1.0 = exact keys.
    pub query_noise_cos: f32,
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
            long_episodes: 0,
            long_t: 0,
            long_max_keys: 0,
            key_clusters: 0,
            cluster_cos: 0.0,
            query_noise_cos: 1.0,
        }
    }
}

pub struct Episode {
    pub writes: Vec<(usize, usize)>,  // (key id, value id)
    pub queries: Vec<(usize, usize)>, // (key id, target value id)
    /// Noisy query vectors (queries.len() * d), empty when queries use the exact keys.
    pub qvecs: Vec<f32>,
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
        let keys = if cfg.key_clusters == 0 {
            unit_vectors(&mut rng, cfg.n_keys, cfg.d)
        } else {
            // clustered keys: k = normalize(√c·centre + √(1−c)·u); key i belongs to centre i % C
            let centres = unit_vectors(&mut rng, cfg.key_clusters, cfg.d);
            let noise = unit_vectors(&mut rng, cfg.n_keys, cfg.d);
            let (a, b) = (cfg.cluster_cos.sqrt(), (1.0 - cfg.cluster_cos).sqrt());
            let mut out = vec![0.0; cfg.n_keys * cfg.d];
            for i in 0..cfg.n_keys {
                let c = i % cfg.key_clusters;
                let row = &mut out[i * cfg.d..(i + 1) * cfg.d];
                for j in 0..cfg.d {
                    row[j] = a * centres[c * cfg.d + j] + b * noise[i * cfg.d + j];
                }
                let n = row.iter().map(|x| x * x).sum::<f32>().sqrt();
                row.iter_mut().for_each(|x| *x /= n);
            }
            out
        };
        let vals = unit_vectors(&mut rng, cfg.n_vals, cfg.d);
        let mut episodes = Vec::with_capacity(cfg.n_episodes + cfg.long_episodes);
        // Standard episodes first, then long ones from the same RNG stream, so a config with
        // long_episodes = 0 produces exactly the v2 task.
        let plan = (0..cfg.n_episodes)
            .map(|_| (cfg.t_writes, usize::MAX))
            .chain((0..cfg.long_episodes).map(|_| (cfg.long_t, cfg.long_max_keys)));
        for (t_writes, max_keys) in plan {
            let mut writes = Vec::with_capacity(t_writes);
            let mut used: Vec<usize> = Vec::new();
            for t in 0..t_writes {
                let key = if t > 0 && (rng.uniform() < cfg.p_overwrite || used.len() >= max_keys) {
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
            episodes.push(Episode { writes, queries, qvecs: Vec::new() });
        }
        if cfg.query_noise_cos < 1.0 {
            // drawn after all episodes so the episode stream is the same as without noise
            let (a, b) = (cfg.query_noise_cos, (1.0 - cfg.query_noise_cos * cfg.query_noise_cos).sqrt());
            for ep in episodes.iter_mut() {
                let u = unit_vectors(&mut rng, ep.queries.len(), cfg.d);
                let mut q = vec![0.0; ep.queries.len() * cfg.d];
                for (qi, &(k, _)) in ep.queries.iter().enumerate() {
                    let row = &mut q[qi * cfg.d..(qi + 1) * cfg.d];
                    for j in 0..cfg.d {
                        row[j] = a * keys[k * cfg.d + j] + b * u[qi * cfg.d + j];
                    }
                    let n = row.iter().map(|x| x * x).sum::<f32>().sqrt();
                    row.iter_mut().for_each(|x| *x /= n);
                }
                ep.qvecs = q;
            }
        }
        Task {
            cfg,
            keys,
            vals,
            episodes,
        }
    }

    /// JSON dump of embeddings and episodes, for offline references (verify/ceiling.py).
    pub fn to_json(&self) -> String {
        let f = |v: &[f32]| v.iter().map(|x| format!("{x}")).collect::<Vec<_>>().join(",");
        let eps: Vec<String> = self
            .episodes
            .iter()
            .map(|e| {
                let w = e.writes.iter().map(|(k, v)| format!("[{k},{v}]")).collect::<Vec<_>>().join(",");
                let q = e.queries.iter().map(|(k, v)| format!("[{k},{v}]")).collect::<Vec<_>>().join(",");
                format!("{{\"w\":[{w}],\"q\":[{q}],\"qv\":[{}]}}", f(&e.qvecs))
            })
            .collect();
        format!(
            "{{\"d\":{},\"keys\":[{}],\"vals\":[{}],\"episodes\":[{}]}}",
            self.cfg.d, f(&self.keys), f(&self.vals), eps.join(",")
        )
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
        for (qi, &(k, target)) in ep.queries.iter().enumerate() {
            let q = if ep.qvecs.is_empty() { task.key(k) } else { &ep.qvecs[qi * d..(qi + 1) * d] };
            match &prog.read {
                None => {
                    for i in 0..d {
                        o[i] = (0..d).map(|j| s_mem[i * d + j] * q[j]).sum();
                    }
                }
                Some(read) => {
                    regs.load_read(&s_mem, q);
                    regs.run_instrs(read);
                    o.copy_from_slice(&regs.v[1]);
                    if o.iter().any(|x| !x.is_finite()) {
                        total += 1;
                        continue; // invalid readout: wrong, zero margin
                    }
                }
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
        fitness: acc + MARGIN_WEIGHT * margin - LEN_PENALTY * prog.total_len() as f32,
        acc,
        margin,
        valid: true,
    }
}

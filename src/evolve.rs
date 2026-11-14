//! Regularized (aging) evolution, as in AutoML-Zero (Real et al. 2020).
//! Population starts as copies of the EMPTY program: the memory is never written.
//! Every rule the search ends with has to be assembled from the instruction set.

use crate::program::{Instr, Op, Program, Regs, MAX_LEN};
use crate::rng::Rng;
use crate::task::{evaluate_beh, Score, Task};
use std::sync::Arc;
use std::collections::{HashMap, VecDeque};
use std::io::Write;
use std::time::Instant;

pub struct SearchCfg {
    pub seed: u64,
    pub budget: usize,
    pub pop: usize,
    pub tournament: usize,
    pub batch: usize,
    pub threads: usize,
    pub log_every: usize,
    /// `--tune-consts K` (added 14 Nov 2026, off = 0): when a child has a structure (effective
    /// code without the values of its constants) that this run has not seen before and that
    /// contains at least one constant, K copies with perturbed constants are evaluated with it
    /// and the best of the K + 1 enters the population. Every copy counts as a candidate.
    pub tune_consts: usize,
    /// `--algo random`: baseline without selection. Every candidate is a fresh random program
    /// of 1 to MAX_LEN random instructions; the best one seen is kept.
    pub random: bool,
    /// `--level-acc A --level-long L` (logging only): with `--val-log`, the first log row at
    /// which the best rule has validation accuracy > A, long-episode accuracy >= L and
    /// train − validation <= 0.03 is recorded.
    pub level: Option<(f32, f32)>,
    /// `--select` (added 15 Nov 2026). Parent selection inside the tournament.
    pub select: Select,
    /// `--share-radius`: niche radius for `Select::Share`, as a fraction of all train queries.
    pub share_radius: f32,
}

/// How the parent is chosen among the `tournament` randomly drawn individuals.
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Select {
    /// Highest fitness (the search as it was).
    Fitness,
    /// Lexicase: episodes are drawn at random one after another; after each, only the
    /// candidates with the most correct queries on that episode stay. When one is left, or
    /// after 32 episodes, the fittest of those left is the parent.
    Lexicase,
    /// Fitness sharing: fitness is divided by the niche count, the number of individuals in the
    /// population whose per-episode behaviour is within the radius (weighted 1 − distance/radius).
    Share,
}

#[derive(Clone)]
pub struct Indiv {
    pub prog: Program,
    pub eff: Program,
    pub score: Score,
    /// Correct queries per train episode; only kept for behaviour-based selection.
    pub beh: Option<Arc<[u8]>>,
}

pub struct Milestone {
    pub name: String,
    pub acc: f32,
    pub hit_at: Option<usize>,
}

pub struct Outcome {
    pub best: Indiv,
    pub evals: usize,
    pub real_evals: usize,
    pub milestones: Vec<Milestone>,
    /// Structural family of the best rule, with the candidate count at which a best rule of
    /// that family first appeared (see classify.rs).
    pub families: Vec<(String, usize)>,
    /// With a validation log: candidate count of the first log row that met `level`.
    pub level_hit: Option<usize>,
    pub seconds: f64,
}

/// Hash of the effective code without constant values: two programs with the same key differ
/// at most in their constants.
fn structure_key(eff: &Program) -> u64 {
    use std::hash::{Hash, Hasher};
    let mut h = std::collections::hash_map::DefaultHasher::new();
    for (part, instrs) in [(0u8, Some(&eff.instrs)), (1u8, eff.read.as_ref())] {
        part.hash(&mut h);
        for i in instrs.into_iter().flatten() {
            (i.op.name(), i.out, i.a, i.b).hash(&mut h);
        }
    }
    h.finish()
}

fn has_const(eff: &Program) -> bool {
    eff.instrs.iter().chain(eff.read.iter().flatten()).any(|i| i.op == Op::Const)
}

/// One perturbed copy for `--tune-consts`: every constant is rescaled, shifted or redrawn.
fn perturb_consts(prog: &mut Program, rng: &mut Rng) {
    for i in prog.instrs.iter_mut().chain(prog.read.iter_mut().flatten()) {
        if i.op != Op::Const {
            continue;
        }
        let u = rng.uniform();
        if u < 0.5 {
            i.c *= (rng.normal() * 0.7).exp();
        } else if u < 0.8 {
            i.c += rng.normal() * 0.3;
        } else {
            i.c = rng.uniform() * 4.0 - 2.0;
        }
    }
}

fn random_program(rng: &mut Rng) -> Program {
    let mut p = crate::program::initial_program();
    for _ in 0..1 + rng.below(MAX_LEN) {
        p.instrs.push(Instr::random(rng));
    }
    p
}

/// Functional-equivalence cache: programs whose effective code is identical get the cached
/// score instead of being re-run (same idea as AutoML-Zero's FEC; here exact, not hashed
/// behaviour). Returns (individuals, number of real evaluations performed).
fn eval_batch(
    progs: Vec<Program>,
    task: &Task,
    threads: usize,
    cache: &mut HashMap<String, Score>,
    mut beh_cache: Option<&mut HashMap<String, Arc<[u8]>>>,
) -> (Vec<Indiv>, usize) {
    let d = task.cfg.d;
    let want_beh = beh_cache.is_some();
    let effs: Vec<Program> = progs.iter().map(|p| p.effective()).collect();
    let keys: Vec<String> = effs.iter().map(|e| e.to_json()).collect();
    let mut todo: Vec<usize> = Vec::new();
    let mut seen: HashMap<&str, ()> = HashMap::new();
    for (i, k) in keys.iter().enumerate() {
        if !cache.contains_key(k) && seen.insert(k.as_str(), ()).is_none() {
            todo.push(i);
        }
    }
    let chunk = todo.len().div_ceil(threads).max(1);
    let mut fresh: Vec<(usize, Score, Vec<u8>)> = Vec::with_capacity(todo.len());
    std::thread::scope(|sc| {
        let handles: Vec<_> = todo
            .chunks(chunk)
            .map(|ch| {
                let effs = &effs;
                sc.spawn(move || {
                    let mut regs = Regs::new(d);
                    ch.iter()
                        .map(|&i| {
                            let mut b = Vec::new();
                            let sc = evaluate_beh(&effs[i], task, &mut regs, if want_beh { Some(&mut b) } else { None });
                            (i, sc, b)
                        })
                        .collect::<Vec<_>>()
                })
            })
            .collect();
        for h in handles {
            fresh.extend(h.join().unwrap());
        }
    });
    let n_real = fresh.len();
    // the behaviour cache holds a vector per program, so it is cleared earlier
    if cache.len() > if want_beh { 1_000_000 } else { 3_000_000 } {
        cache.clear();
        if let Some(bc) = beh_cache.as_deref_mut() {
            bc.clear();
        }
    }
    for (i, sc, b) in fresh {
        cache.insert(keys[i].clone(), sc);
        if let Some(bc) = beh_cache.as_deref_mut() {
            bc.insert(keys[i].clone(), b.into());
        }
    }
    let out = progs
        .into_iter()
        .zip(effs)
        .zip(keys)
        .map(|((prog, eff), k)| Indiv {
            prog,
            eff,
            score: cache[&k],
            beh: beh_cache.as_deref().map(|bc| bc[&k].clone()),
        })
        .collect();
    (out, n_real)
}

/// Niche counts for fitness sharing: for every individual, the sum over the population of
/// max(0, 1 − distance/radius), distance = L1 distance of the behaviour vectors.
fn niche_counts(pop: &VecDeque<Indiv>, radius: f32) -> Vec<f32> {
    let behs: Vec<&[u8]> = pop.iter().map(|i| i.beh.as_deref().unwrap()).collect();
    behs.iter()
        .map(|a| {
            behs.iter()
                .map(|b| {
                    let dist: u32 = a.iter().zip(b.iter()).map(|(x, y)| x.abs_diff(*y) as u32).sum();
                    (1.0 - dist as f32 / radius).max(0.0)
                })
                .sum()
        })
        .collect()
}

pub fn search(
    cfg: &SearchCfg,
    task: &Task,
    milestones: Vec<(String, f32)>,
    family_of: &dyn Fn(&Program) -> String,
    val: Option<&dyn Fn(&Program) -> (f32, f32)>,
    log: &mut dyn Write,
) -> Outcome {
    let t0 = Instant::now();
    let mut rng = Rng::new(cfg.seed);
    let mut cache: HashMap<String, Score> = HashMap::new();
    let mut beh_store: HashMap<String, Arc<[u8]>> = HashMap::new();
    let niching = cfg.select != Select::Fitness;
    let n_queries: usize = task.episodes.iter().map(|e| e.queries.len()).sum();
    let radius = (cfg.share_radius * n_queries as f32).max(1.0);
    let (init, mut real_evals) = eval_batch(
        vec![crate::program::initial_program(); cfg.pop],
        task,
        cfg.threads,
        &mut cache,
        if niching { Some(&mut beh_store) } else { None },
    );
    let mut pop: VecDeque<Indiv> = init.into_iter().collect();
    let mut evals = cfg.pop;
    let mut best = pop[0].clone();
    let mut ms: Vec<Milestone> = milestones
        .into_iter()
        .map(|(name, acc)| Milestone {
            name,
            acc,
            hit_at: None,
        })
        .collect();
    let mut families: Vec<(String, usize)> = Vec::new();
    let mut next_log = 0;
    writeln!(
        log,
        "candidates,real_evals,seconds,best_fitness,best_acc,best_len,pop_mean_acc{}",
        if val.is_some() { ",val_acc,long_acc" } else { "" }
    )
    .ok();
    let mut seen_structures: std::collections::HashSet<u64> = std::collections::HashSet::new();
    let mut level_hit: Option<usize> = None;

    while evals < cfg.budget {
        let shared: Vec<f32> = if cfg.select == Select::Share {
            let m = niche_counts(&pop, radius);
            pop.iter().zip(m).map(|(i, m)| if i.score.fitness > 0.0 { i.score.fitness / m } else { i.score.fitness }).collect()
        } else {
            Vec::new()
        };
        let children: Vec<Program> = (0..cfg.batch)
            .map(|_| {
                if cfg.random {
                    return random_program(&mut rng);
                }
                let mut winner: Option<&Indiv> = None;
                if cfg.select == Select::Fitness {
                    for _ in 0..cfg.tournament {
                        let c = &pop[rng.below(pop.len())];
                        if winner.map_or(true, |w| c.score.fitness > w.score.fitness) {
                            winner = Some(c);
                        }
                    }
                } else {
                    let mut cand: Vec<usize> = (0..cfg.tournament).map(|_| rng.below(pop.len())).collect();
                    if cfg.select == Select::Lexicase {
                        let n_ep = task.episodes.len();
                        for _ in 0..32 {
                            if cand.len() <= 1 {
                                break;
                            }
                            let e = rng.below(n_ep);
                            let top = cand.iter().map(|&i| pop[i].beh.as_ref().unwrap()[e]).max().unwrap();
                            cand.retain(|&i| pop[i].beh.as_ref().unwrap()[e] == top);
                        }
                    }
                    let key = |i: usize| if cfg.select == Select::Share { shared[i] } else { pop[i].score.fitness };
                    let mut best_i = cand[0];
                    for &i in &cand[1..] {
                        if key(i) > key(best_i) {
                            best_i = i;
                        }
                    }
                    winner = Some(&pop[best_i]);
                }
                let mut child = winner.unwrap().prog.clone();
                child.mutate(&mut rng);
                while rng.uniform() < 0.3 {
                    child.mutate(&mut rng);
                }
                child
            })
            .collect();
        // --tune-consts: add perturbed copies of children with a new structure. `group[i]` is
        // the child that program i belongs to; without tuning every group has one member.
        let mut group: Vec<usize> = (0..children.len()).collect();
        let mut children = children;
        if cfg.tune_consts > 0 {
            for g in 0..cfg.batch {
                let eff = children[g].effective();
                if has_const(&eff) && seen_structures.insert(structure_key(&eff)) {
                    for _ in 0..cfg.tune_consts {
                        let mut v = children[g].clone();
                        perturb_consts(&mut v, &mut rng);
                        children.push(v);
                        group.push(g);
                    }
                }
            }
        }
        let (evaluated, n_real) = eval_batch(children, task, cfg.threads, &mut cache, if niching { Some(&mut beh_store) } else { None });
        evals += evaluated.len();
        real_evals += n_real;
        // best member of every group, the original child on ties
        let mut winners: Vec<Option<Indiv>> = (0..cfg.batch).map(|_| None).collect();
        for (ind, g) in evaluated.into_iter().zip(group) {
            if winners[g].as_ref().map_or(true, |w| ind.score.fitness > w.score.fitness) {
                winners[g] = Some(ind);
            }
        }
        for ind in winners.into_iter().flatten() {
            if ind.score.fitness > best.score.fitness {
                best = ind.clone();
                let fam = family_of(&best.eff);
                if !families.iter().any(|(f, _)| *f == fam) {
                    families.push((fam, evals));
                }
            }
            pop.push_back(ind);
            pop.pop_front();
        }
        for m in ms.iter_mut() {
            if m.hit_at.is_none() && best.score.acc >= m.acc - 0.005 {
                m.hit_at = Some(evals);
            }
        }
        if evals >= next_log {
            let mean_acc = pop.iter().map(|i| i.score.acc).sum::<f32>() / pop.len() as f32;
            let extra = match val {
                Some(f) => {
                    let (va, la) = f(&best.eff);
                    if let Some((a, l)) = cfg.level {
                        if level_hit.is_none() && va > a && la >= l && best.score.acc - va <= 0.03 {
                            level_hit = Some(evals);
                        }
                    }
                    format!(",{va:.4},{la:.4}")
                }
                None => String::new(),
            };
            writeln!(
                log,
                "{},{},{:.1},{:.5},{:.4},{},{:.4}{}",
                evals,
                real_evals,
                t0.elapsed().as_secs_f64(),
                best.score.fitness,
                best.score.acc,
                best.eff.instrs.len(),
                mean_acc,
                extra
            )
            .ok();
            next_log += cfg.log_every;
        }
    }
    Outcome {
        best,
        evals,
        real_evals,
        milestones: ms,
        families,
        level_hit,
        seconds: t0.elapsed().as_secs_f64(),
    }
}

mod classify;
mod evolve;
mod program;
mod reference;
mod rng;
mod task;

use program::{baselines, Program, Regs};
use std::fs;
use std::io::Write;
use task::{evaluate, Task, TaskCfg};

/// `--task-seed N` (default 1, the seed of every run before 10 Nov 2026) and
/// `--train-episodes N` (default 0 = the task's own size, 96 standard episodes).
static TRAIN_TASK_SEED: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(1);
static TRAIN_EPISODES: std::sync::atomic::AtomicUsize = std::sync::atomic::AtomicUsize::new(0);

fn task_seed() -> u64 {
    TRAIN_TASK_SEED.load(std::sync::atomic::Ordering::Relaxed)
}
fn train_episodes() -> usize {
    match TRAIN_EPISODES.load(std::sync::atomic::Ordering::Relaxed) {
        0 => 96,
        n => n,
    }
}

/// `--task v3` (any command): train on the v2 episodes plus 48 long episodes (T = 64, at most
/// 8 distinct keys), so that growth factors a > 1 are punished. Default is the v2 task.
static TASK_V3: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

/// `--regime NAME` (any command): stage-2 regime as the train task and as an extra held-out
/// suite. Overrides `--task`. Names: collision, overload, noisyq, longgap.
static REGIME: std::sync::OnceLock<String> = std::sync::OnceLock::new();

fn regime_cfg(name: &str, seed: u64, n_ep: usize) -> TaskCfg {
    let mut c = TaskCfg { n_episodes: n_ep, ..TaskCfg::search_default(seed) };
    match name {
        "collision" => {
            c.key_clusters = 8;
            c.cluster_cos = 0.85;
        }
        "overload" => c.t_writes = 32,
        "noisyq" => c.query_noise_cos = 0.9,
        "collision3" => {
            // collision keys plus v3-style long episodes, so that a > 1 is punished
            c.key_clusters = 8;
            c.cluster_cos = 0.85;
            c.long_episodes = n_ep / 2;
            c.long_t = 64;
            c.long_max_keys = 8;
        }
        "longgap" => {
            c.n_episodes = 0;
            c.long_episodes = n_ep / 2;
            c.long_t = 128;
            c.long_max_keys = 8;
        }
        // Regimes added 10 Nov 2026 (headroom against the ridge ceiling, see README).
        "full" => c.t_writes = 24,
        "overload48" => c.t_writes = 48,
        "rewrite8" | "rewrite14" => {
            // only long episodes: 96 writes onto at most 8 / 14 keys
            c.n_episodes = 0;
            c.long_episodes = n_ep;
            c.long_t = 96;
            c.long_max_keys = if name == "rewrite8" { 8 } else { 14 };
        }
        "clustered" => {
            // all keys around one centre, pairwise cosine about 0.8
            c.key_clusters = 1;
            c.cluster_cos = 0.8;
        }
        "clustered8" => {
            c.key_clusters = 1;
            c.cluster_cos = 0.8;
            c.n_episodes = 0;
            c.long_episodes = n_ep;
            c.long_t = 48;
            c.long_max_keys = 8;
        }
        _ => panic!("unknown regime {name}"),
    }
    c
}

fn train_cfg() -> TaskCfg {
    if let Some(r) = REGIME.get() {
        return regime_cfg(r, task_seed(), train_episodes());
    }
    let mut c = TaskCfg { n_episodes: train_episodes(), ..TaskCfg::search_default(task_seed()) };
    if TASK_V3.load(std::sync::atomic::Ordering::Relaxed) {
        c.long_episodes = 48;
        c.long_t = 64;
        c.long_max_keys = 8;
    }
    c
}

fn task_name() -> String {
    if let Some(r) = REGIME.get() {
        return format!("regime {r}");
    }
    (if TASK_V3.load(std::sync::atomic::Ordering::Relaxed) { "v3" } else { "v2" }).to_string()
}

/// Held-out evaluation suites: fresh episodes and embeddings, plus shifted sizes the rule
/// never saw during search (rules are dimension-agnostic programs, so they run unchanged).
fn test_suites() -> Vec<(String, TaskCfg)> {
    let mut v: Vec<(String, TaskCfg)> = Vec::new();
    if let Some(r) = REGIME.get() {
        v.push((format!("test regime {r}"), regime_cfg(r, 9, 512)));
    }
    v.extend(base_suites().into_iter().map(|(n, c)| (n.to_string(), c)));
    v
}

fn base_suites() -> Vec<(&'static str, TaskCfg)> {
    vec![
        (
            "test d16 T12 ow0.3",
            TaskCfg {
                n_episodes: 512,
                ..TaskCfg::search_default(2)
            },
        ),
        (
            "test d16 T12 ow0.0",
            TaskCfg {
                n_episodes: 512,
                p_overwrite: 0.0,
                ..TaskCfg::search_default(3)
            },
        ),
        (
            "test d16 T12 ow0.6",
            TaskCfg {
                n_episodes: 512,
                p_overwrite: 0.6,
                ..TaskCfg::search_default(4)
            },
        ),
        (
            "test d32 T24 ow0.3",
            TaskCfg {
                d: 32,
                n_keys: 128,
                n_vals: 128,
                t_writes: 24,
                n_episodes: 256,
                ..TaskCfg::search_default(5)
            },
        ),
        (
            "test d8 T6 ow0.3",
            TaskCfg {
                d: 8,
                n_keys: 32,
                n_vals: 32,
                t_writes: 6,
                n_episodes: 512,
                ..TaskCfg::search_default(6)
            },
        ),
        (
            "test d16 T64 K8 ow0.3",
            TaskCfg {
                n_episodes: 0,
                long_episodes: 256,
                long_t: 64,
                long_max_keys: 8,
                ..TaskCfg::search_default(7)
            },
        ),
        (
            "test d16 T128 K8 ow0.3",
            TaskCfg {
                n_episodes: 0,
                long_episodes: 128,
                long_t: 128,
                long_max_keys: 8,
                ..TaskCfg::search_default(8)
            },
        ),
    ]
}

fn eval_on(prog: &Program, cfg: &TaskCfg) -> task::Score {
    let task = Task::new(cfg.clone());
    let mut regs = Regs::new(cfg.d);
    evaluate(&prog.effective(), &task, &mut regs)
}

fn arg<T: std::str::FromStr>(args: &[String], name: &str, default: T) -> T {
    args.iter()
        .position(|a| a == name)
        .and_then(|i| args.get(i + 1))
        .and_then(|v| v.parse().ok())
        .unwrap_or(default)
}

fn has(args: &[String], name: &str) -> bool {
    args.iter().any(|a| a == name)
}

/// Episodes the structural test takes its memory states from: the train task's setting with
/// other embeddings and episodes, cut down to a few episodes.
fn classify_task() -> Task {
    let mut c = train_cfg();
    c.seed += 1000;
    c.n_episodes = c.n_episodes.min(32);
    c.long_episodes = c.long_episodes.min(16);
    Task::new(c)
}

fn git_commit(args: &[String]) -> String {
    let given: String = arg(args, "--commit", String::new());
    if !given.is_empty() {
        return given;
    }
    std::process::Command::new("git")
        .args(["rev-parse", "--short", "HEAD"])
        .output()
        .ok()
        .filter(|o| o.status.success())
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
        .unwrap_or_else(|| "unknown".into())
}

fn baseline_table() -> String {
    let train = train_cfg();
    let suites = test_suites();
    let ctask = classify_task();
    let mut s = String::from("| rule | structural class | train acc | ");
    s += &suites.iter().map(|(n, _)| n.as_str()).collect::<Vec<_>>().join(" | ");
    s += " |\n|---|---|---|";
    s += &"---|".repeat(suites.len());
    s += "\n";
    for (name, p) in baselines() {
        let tr = eval_on(&p, &train);
        s += &format!("| {name} | {} | {:.3} |", classify::classify(&p, &ctask).family, tr.acc);
        for (_, cfg) in &suites {
            s += &format!(" {:.3} |", eval_on(&p, cfg).acc);
        }
        s += "\n";
    }
    s
}

fn report(prog: &Program) -> String {
    let eff = prog.effective();
    let train = eval_on(prog, &train_cfg());
    let mut s = format!(
        "{}\n\nEffective program ({} instructions):\n{}\n\nstructure: {}\n\ntrain acc {:.3} ±{:.3}\n",
        eff.formula(),
        eff.instrs.len(),
        eff.listing(),
        classify::classify(prog, &classify_task()).describe(),
        train.acc,
        train.se()
    );
    for (name, cfg) in test_suites() {
        let sc = eval_on(prog, &cfg);
        s += &format!("{name}: acc {:.3}  margin {:.3}  ±{:.3}\n", sc.acc, sc.margin, sc.se());
    }
    s
}

/// Known families as programs in the search space, for `sweep`. Parameters: [a, x].
fn family_prog(kind: &str, a: f32, x: f32) -> Program {
    let l: Vec<String> = match kind {
        // S' = a·S + v kᵀ
        "la" => vec![format!("Const 0 0 0 {a}"), "MatScale 0 0 0".into(), "Outer 1 1 0".into(), "MatAdd 0 0 1".into()],
        // S' = a·S(I − e·kkᵀ) + e·v kᵀ   (x = e)
        "delta" => vec![
            format!("Const 0 0 0 {x}"),
            "MatVec 2 0 0".into(),
            "Outer 1 2 0".into(),
            "MatScale 1 0 1".into(),
            "MatSub 0 0 1".into(),
            format!("Const 1 0 0 {a}"),
            "MatScale 0 1 0".into(),
            "Outer 3 1 0".into(),
            "MatScale 3 0 3".into(),
            "MatAdd 0 0 3".into(),
        ],
        // S' = a·S − β·(vᵀ(a·S)k − 1)·v kᵀ   (x = β), Kronecker Delta Rule with target 1
        "kron" => vec![
            format!("Const 3 0 0 {a}"),
            "MatScale 0 3 0".into(),
            "MatVec 2 0 0".into(),
            "Dot 0 1 2".into(),
            format!("Const 1 0 0 {}", -x),
            "SMul 0 0 1".into(),
            format!("Const 2 0 0 {x}"),
            "SAdd 0 0 2".into(),
            "Outer 1 1 0".into(),
            "MatScale 1 0 1".into(),
            "MatAdd 0 0 1".into(),
        ],
        _ => unreachable!(),
    };
    program::prog(&l.iter().map(|x| x.as_str()).collect::<Vec<_>>())
}

/// Fair baselines: every known family is tuned on the TRAIN task of the chosen regime and
/// reported on all held-out suites, next to the ridge ceiling.
fn sweep(args: &[String]) {
    let (regime, train) = (task_name(), train_cfg());
    let task = Task::new(train.clone());
    let mut regs = Regs::new(task.cfg.d);
    let suites = test_suites();
    let alphas = [0.7f32, 0.75, 0.8, 0.85, 0.9, 0.95, 0.97, 0.98, 0.99, 1.0, 1.01, 1.02, 1.03, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3];
    let steps = |n: usize| (1..=n).map(|i| i as f32 * 0.05).collect::<Vec<f32>>();
    let one = [1.0f32];
    println!(
        "task {regime}, tuned on {} train episodes (task seed {}), commit {}\n",
        train.n_episodes + train.long_episodes,
        train.seed,
        git_commit(args)
    );
    println!("| family (tuned on train) | parameters | train | {} |", suites.iter().map(|x| x.0.as_str()).collect::<Vec<_>>().join(" | "));
    println!("|---|---|---|{}", "---|".repeat(suites.len()));
    let prog_rows: [(&str, &str, &[f32], Vec<f32>, &str); 6] = [
        ("linear attention", "la", &one, vec![0.0], ""),
        ("decayed linear attention", "la", &alphas, vec![0.0], "a"),
        ("DeltaNet", "delta", &one, steps(20), "e"),
        ("Gated DeltaNet", "delta", &alphas, steps(20), "a,e"),
        ("Kronecker delta rule", "kron", &one, steps(30), "β"),
        ("gated Kronecker delta rule", "kron", &alphas, steps(30), "a,β"),
    ];
    for (name, kind, a_grid, x_grid, pnames) in prog_rows {
        let mut best = (-1.0f32, 1.0f32, 0.0f32);
        for &a in a_grid {
            for &x in &x_grid {
                let acc = evaluate(&family_prog(kind, a, x).effective(), &task, &mut regs).acc;
                if acc > best.0 {
                    best = (acc, a, x);
                }
            }
        }
        let p = family_prog(kind, best.1, best.2);
        let params = match pnames {
            "" => "–".to_string(),
            "a" => format!("a={}", best.1),
            "e" | "β" => format!("{pnames}={:.2}", best.2),
            _ => format!("a={}, {}={:.2}", best.1, &pnames[2..], best.2),
        };
        let row: Vec<String> = suites.iter().map(|(_, c)| format!("{:.3}", eval_on(&p, c).acc)).collect();
        println!("| {name} | {params} | {:.3} | {} |", best.0, row.join(" | "));
    }
    // References outside the search space: second d×d state, and the ceiling.
    let lams = [1e-4f32, 1e-3, 1e-2, 3e-2, 0.1, 0.3, 1.0, 3.0];
    let qs = [0.0f32, 0.01, 0.1, 1.0, 10.0, 100.0];
    let native: [(&str, &[f32], Box<dyn Fn(&Task, f32, f32) -> f32>); 3] = [
        ("RLS (2 states)", &qs[..1], Box::new(|t, l, q| reference::kalman_acc(t, l, q))),
        ("Kalman delta (2 states)", &qs, Box::new(|t, l, q| reference::kalman_acc(t, l, q))),
        ("ridge ceiling", &qs[..1], Box::new(|t, l, _| reference::ridge_acc(t, l))),
    ];
    for (name, q_grid, f) in native {
        let mut best = (-1.0f32, 0.0f32, 0.0f32);
        for &l in &lams {
            for &q in q_grid {
                let acc = f(&task, l, q);
                if acc > best.0 {
                    best = (acc, l, q);
                }
            }
        }
        let params = if q_grid.len() > 1 { format!("λ={}, q={}", best.1, best.2) } else { format!("λ={}", best.1) };
        let row: Vec<String> = suites.iter().map(|(_, c)| format!("{:.3}", f(&Task::new(c.clone()), best.1, best.2))).collect();
        println!("| {name} | {params} | {:.3} | {} |", best.0, row.join(" | "));
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let cmd = args.get(1).map(String::as_str).unwrap_or("help");
    if arg(&args, "--task", String::from("v2")) == "v3" {
        TASK_V3.store(true, std::sync::atomic::Ordering::Relaxed);
    }
    let regime: String = arg(&args, "--regime", String::new());
    if !regime.is_empty() {
        regime_cfg(&regime, 0, 2); // validate the name early
        REGIME.set(regime).ok();
    }
    // alphabet-sensitivity switches (queue item 3a); without them the alphabet is unchanged
    let no_ops: Vec<program::Op> = arg(&args, "--no-op", String::new())
        .split(',')
        .filter(|s| !s.is_empty())
        .map(|s| program::Op::from_name(s).expect("unknown op in --no-op"))
        .collect();
    let extra = args.iter().any(|a| a == "--extra-ops");
    let recip = has(&args, "--recip");
    if arg(&args, "--persist-init", String::from("zero")) == "identity" {
        program::PERSIST_IDENTITY.store(true, std::sync::atomic::Ordering::Relaxed);
    }
    task::QUERY_GAP.store(arg(&args, "--query-gap", 0usize), std::sync::atomic::Ordering::Relaxed);
    TRAIN_TASK_SEED.store(arg(&args, "--task-seed", 1u64), std::sync::atomic::Ordering::Relaxed);
    TRAIN_EPISODES.store(arg(&args, "--train-episodes", 0usize), std::sync::atomic::Ordering::Relaxed);
    program::PERSIST_M.store(arg(&args, "--persist-m", 1usize).clamp(1, program::NM), std::sync::atomic::Ordering::Relaxed);
    program::PERSIST_V.store(arg(&args, "--persist-v", 0usize).min(program::NV - 2), std::sync::atomic::Ordering::Relaxed);
    if args.iter().any(|a| a == "--evolve-readout") {
        program::READ_EVOLVE.store(true, std::sync::atomic::Ordering::Relaxed);
    }
    if !no_ops.is_empty() || extra || recip {
        program::set_alphabet(&no_ops, extra, recip);
    }
    let alphabet = format!(
        "{} ops{}{}",
        program::active_ops().len(),
        if no_ops.is_empty() { String::new() } else { format!(", without {}", no_ops.iter().map(|o| o.name()).collect::<Vec<_>>().join(",")) },
        if extra { ", with extra ops" } else { "" }
    ) + if recip { ", with Recip" } else { "" };
    match cmd {
        "baselines" => {
            println!("{}", baseline_table());
            for (name, p) in baselines() {
                println!("{name}: {}", p.formula());
            }
        }
        "sweep" => sweep(&args),
        "dump" => {
            // dump the train task or the regime test suite as JSON for offline references
            let split: String = arg(&args, "--split", String::from("train"));
            let cfg = if split == "train" {
                train_cfg()
            } else {
                test_suites().into_iter().find(|(n, _)| n.starts_with("test regime")).expect("--regime needed").1
            };
            let out: String = arg(&args, "--out", String::from("task.json"));
            fs::write(&out, Task::new(cfg).to_json()).unwrap();
        }
        "eval" => {
            let path: String = arg(&args, "--prog", String::new());
            let text = fs::read_to_string(&path).expect("read prog");
            // the state budget a rule was found with is part of the rule
            let (pm, pv, pid) = Program::json_budget(&text);
            program::PERSIST_M.store(pm, std::sync::atomic::Ordering::Relaxed);
            program::PERSIST_V.store(pv, std::sync::atomic::Ordering::Relaxed);
            program::PERSIST_IDENTITY.store(pid == 1, std::sync::atomic::Ordering::Relaxed);
            let prog = Program::from_json(&text)
                .expect("parse prog");
            println!("{}", report(&prog));
        }
        "search" => {
            if args.iter().any(|a| a == "--no-split-edge") {
                program::SPLIT_EDGE.store(false, std::sync::atomic::Ordering::Relaxed);
            }
            let cfg = evolve::SearchCfg {
                seed: arg(&args, "--seed", 0),
                budget: arg(&args, "--budget", 200_000),
                pop: arg(&args, "--pop", 500),
                tournament: arg(&args, "--tournament", 10),
                batch: arg(&args, "--batch", 64),
                threads: arg(&args, "--threads", 2),
                log_every: arg(&args, "--log-every", 5_000),
                tune_consts: arg(&args, "--tune-consts", 0usize),
                random: arg(&args, "--algo", String::from("evolve")) == "random",
                level: if has(&args, "--level-acc") {
                    Some((arg(&args, "--level-acc", 0.0f32), arg(&args, "--level-long", 0.0f32)))
                } else {
                    None
                },
            };
            let out: String = arg(&args, "--out", format!("runs/seed{}", cfg.seed));
            fs::create_dir_all(&out).unwrap();
            let task = Task::new(train_cfg());
            let mut regs = Regs::new(task.cfg.d);
            let milestones: Vec<(String, f32)> = baselines()
                .into_iter()
                .skip(1)
                .map(|(n, p)| (n.to_string(), evaluate(&p.effective(), &task, &mut regs).acc))
                .collect();
            let mut log = fs::File::create(format!("{out}/log.csv")).unwrap();
            let ctask = classify_task();
            let family_of = |p: &Program| classify::classify(p, &ctask).family;
            // --val-log: at every log row the best rule is also scored on a validation draw of
            // the train task and on 128-write episodes (both with seeds no suite uses). Logging
            // only; nothing of it reaches the search.
            let val_task = {
                let mut c = train_cfg();
                c.seed += 2000;
                c.n_episodes *= 2;
                c.long_episodes *= 2;
                Task::new(c)
            };
            let long_task = Task::new(TaskCfg {
                n_episodes: 0,
                long_episodes: 64,
                long_t: 128,
                long_max_keys: 8,
                ..TaskCfg::search_default(task_seed() + 2008)
            });
            let val_fn = |p: &Program| {
                let mut r = Regs::new(val_task.cfg.d);
                (evaluate(p, &val_task, &mut r).acc, evaluate(p, &long_task, &mut r).acc)
            };
            let val: Option<&dyn Fn(&Program) -> (f32, f32)> = if has(&args, "--val-log") { Some(&val_fn) } else { None };
            let res = evolve::search(&cfg, &task, milestones, &family_of, val, &mut log);
            fs::write(format!("{out}/best.json"), res.best.prog.effective().to_json()).unwrap();
            let mut summary = format!(
                "# Search seed {}\n\ntask: {}  alphabet: {}  readout: {}  add-node mutation: {}  candidates: {}  real evaluations (after cache): {}  time: {:.0}s  pop: {}  tournament: {}\n\n",
                cfg.seed,
                task_name(),
                alphabet,
                if program::READ_EVOLVE.load(std::sync::atomic::Ordering::Relaxed) { "evolved" } else { "fixed o = S q" },
                if program::SPLIT_EDGE.load(std::sync::atomic::Ordering::Relaxed) { "on" } else { "off" },
                res.evals, res.real_evals, res.seconds, cfg.pop, cfg.tournament
            );
            summary += &format!(
                "commit: {}  task seed: {}  train episodes: {}  persistent registers: {} matrix, {} vector, start {}  batch: {}\n\n",
                git_commit(&args),
                task.cfg.seed,
                task.cfg.n_episodes + task.cfg.long_episodes,
                program::PERSIST_M.load(std::sync::atomic::Ordering::Relaxed),
                program::PERSIST_V.load(std::sync::atomic::Ordering::Relaxed),
                if program::PERSIST_IDENTITY.load(std::sync::atomic::Ordering::Relaxed) { "identity" } else { "zero" },
                cfg.batch
            );
            summary += &format!(
                "search: {}  tune-consts: {}\n\n",
                if cfg.random { "random programs, no selection" } else { "regularized evolution" },
                cfg.tune_consts
            );
            if let Some((a, l)) = cfg.level {
                summary += &format!(
                    "validation level (val > {a}, T128 K8 val >= {l}, train - val <= 0.03; checked every {} candidates): {}\n\n",
                    cfg.log_every,
                    res.level_hit.map_or("not reached".to_string(), |e| format!("{e} candidates"))
                );
            }
            summary += "## Structural rediscovery (first candidate count at which the best rule belongs to a family)\n\n";
            for (fam, at) in &res.families {
                summary += &format!("* {fam}: {at} candidates\n");
            }
            summary += "\n## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)\n\n";
            for m in &res.milestones {
                summary += &format!(
                    "- {} (acc {:.3}): {}\n",
                    m.name,
                    m.acc,
                    m.hit_at.map_or("not reached".into(), |e| format!("{e} candidates"))
                );
            }
            summary += "\n## Best rule\n\n```\n";
            summary += &report(&res.best.prog);
            summary += "```\n";
            fs::write(format!("{out}/summary.md"), &summary).unwrap();
            print!("{summary}");
            std::io::stdout().flush().ok();
        }
        _ => {
            eprintln!(
                "usage: autoplast baselines | sweep | eval --prog FILE | dump [--split train|test --out FILE] | search [--seed N --budget N --pop N --threads N --batch N --out DIR]\n\
                 task:   --task v3 | --regime collision|overload|noisyq|collision3|longgap|full|overload48|rewrite8|rewrite14|clustered|clustered8   --task-seed N  --train-episodes N  --query-gap N\n\
                 space:  --no-op A,B  --extra-ops  --recip  --evolve-readout  --persist-m N (1..4)  --persist-v N (0..4)  --persist-init identity  --no-split-edge\n\
                 search: --tune-consts K  --algo random  --val-log  --level-acc A --level-long L"
            );
        }
    }
}

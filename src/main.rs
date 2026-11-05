mod evolve;
mod program;
mod rng;
mod task;

use program::{baselines, Program, Regs};
use std::fs;
use std::io::Write;
use task::{evaluate, Task, TaskCfg};

const TRAIN_TASK_SEED: u64 = 1;

/// `--task v3` (any command): train on the v2 episodes plus 48 long episodes (T = 64, at most
/// 8 distinct keys), so that growth factors a > 1 are punished. Default is the v2 task.
static TASK_V3: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

fn train_cfg() -> TaskCfg {
    let mut c = TaskCfg::search_default(TRAIN_TASK_SEED);
    if TASK_V3.load(std::sync::atomic::Ordering::Relaxed) {
        c.long_episodes = 48;
        c.long_t = 64;
        c.long_max_keys = 8;
    }
    c
}

fn task_name() -> &'static str {
    if TASK_V3.load(std::sync::atomic::Ordering::Relaxed) { "v3" } else { "v2" }
}

/// Held-out evaluation suites: fresh episodes and embeddings, plus shifted sizes the rule
/// never saw during search (rules are dimension-agnostic programs, so they run unchanged).
fn test_suites() -> Vec<(&'static str, TaskCfg)> {
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

fn baseline_table() -> String {
    let train = train_cfg();
    let suites = test_suites();
    let mut s = String::from("| rule | train acc | ");
    s += &suites.iter().map(|(n, _)| *n).collect::<Vec<_>>().join(" | ");
    s += " |\n|---|---|";
    s += &"---|".repeat(suites.len());
    s += "\n";
    for (name, p) in baselines() {
        let tr = eval_on(&p, &train);
        s += &format!("| {name} | {:.3} |", tr.acc);
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
        "{}\n\nEffective program ({} instructions):\n{}\n\ntrain acc {:.3}\n",
        eff.formula(),
        eff.instrs.len(),
        eff.listing(),
        train.acc
    );
    for (name, cfg) in test_suites() {
        let sc = eval_on(prog, &cfg);
        s += &format!("{name}: acc {:.3}  margin {:.3}\n", sc.acc, sc.margin);
    }
    s
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let cmd = args.get(1).map(String::as_str).unwrap_or("help");
    if arg(&args, "--task", String::from("v2")) == "v3" {
        TASK_V3.store(true, std::sync::atomic::Ordering::Relaxed);
    }
    // alphabet-sensitivity switches (queue item 3a); without them the alphabet is unchanged
    let no_ops: Vec<program::Op> = arg(&args, "--no-op", String::new())
        .split(',')
        .filter(|s| !s.is_empty())
        .map(|s| program::Op::from_name(s).expect("unknown op in --no-op"))
        .collect();
    let extra = args.iter().any(|a| a == "--extra-ops");
    if !no_ops.is_empty() || extra {
        program::set_alphabet(&no_ops, extra);
    }
    let alphabet = format!(
        "{} ops{}{}",
        program::active_ops().len(),
        if no_ops.is_empty() { String::new() } else { format!(", without {}", no_ops.iter().map(|o| o.name()).collect::<Vec<_>>().join(",")) },
        if extra { ", with extra ops" } else { "" }
    );
    match cmd {
        "baselines" => {
            println!("{}", baseline_table());
            for (name, p) in baselines() {
                println!("{name}: {}", p.formula());
            }
        }
        "sweep" => {
            // Fair baselines: tune the known family S' = a·S(I - e·kkᵀ) + w·v kᵀ on the TRAIN
            // task, report held-out tests. Tied (w = e, a = 1) is DeltaNet; tied with free a
            // is Gated DeltaNet; untied is the family the search landed in.
            let train = train_cfg();
            let task = Task::new(train);
            let mut regs = Regs::new(task.cfg.d);
            let mk = |a: f32, e: f32, w: f32| {
                let l = [
                    format!("Const 0 0 0 {e}"),
                    "Outer 1 0 0".to_string(),
                    "MatScale 1 0 1".to_string(),
                    "MatMul 2 0 1".to_string(),
                    "MatSub 0 0 2".to_string(),
                    format!("Const 1 0 0 {a}"),
                    "MatScale 0 1 0".to_string(),
                    "Outer 3 1 0".to_string(),
                    format!("Const 2 0 0 {w}"),
                    "MatScale 3 2 3".to_string(),
                    "MatAdd 0 0 3".to_string(),
                ];
                program::prog(&l.iter().map(|x| x.as_str()).collect::<Vec<_>>())
            };
            let alphas = [0.85f32, 0.9, 0.95, 0.97, 0.99, 1.0, 1.01, 1.03, 1.05, 1.1, 1.15, 1.2];
            let grid: Vec<f32> = (1..=20).map(|i| i as f32 * 0.05).collect();
            let mut best: Vec<(&str, f32, (f32, f32, f32))> =
                vec![("DeltaNet (a=1, w=e)", -1.0, (0., 0., 0.)), ("Gated DeltaNet (w=e)", -1.0, (0., 0., 0.)), ("untied a, e, w", -1.0, (0., 0., 0.))];
            for &a in &alphas {
                for &e in &grid {
                    for &w in &grid {
                        let p = mk(a, e, w);
                        let sc = evaluate(&p.effective(), &task, &mut regs).acc;
                        let tied = (w - e).abs() < 1e-6;
                        let fams = [tied && (a - 1.0).abs() < 1e-6, tied, true];
                        for (i, ok) in fams.iter().enumerate() {
                            if *ok && sc > best[i].1 {
                                best[i] = (best[i].0, sc, (a, e, w));
                            }
                        }
                    }
                }
            }
            let suites = test_suites();
            println!("| family (tuned on train) | a | e | w | train | {} |", suites.iter().map(|x| x.0).collect::<Vec<_>>().join(" | "));
            for (name, tr, (a, e, w)) in best {
                let p = mk(a, e, w);
                let row: Vec<String> = suites.iter().map(|(_, c)| format!("{:.3}", eval_on(&p, c).acc)).collect();
                println!("| {name} | {a} | {e:.2} | {w:.2} | {tr:.3} | {} |", row.join(" | "));
            }
        }
        "eval" => {
            let path: String = arg(&args, "--prog", String::new());
            let prog = Program::from_json(&fs::read_to_string(&path).expect("read prog"))
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
            let res = evolve::search(&cfg, &task, milestones, &mut log);
            fs::write(format!("{out}/best.json"), res.best.prog.effective().to_json()).unwrap();
            let mut summary = format!(
                "# Search seed {}\n\ntask: {}  alphabet: {}  add-node mutation: {}  candidates: {}  real evaluations (after cache): {}  time: {:.0}s  pop: {}  tournament: {}\n\n",
                cfg.seed,
                task_name(),
                alphabet,
                if program::SPLIT_EDGE.load(std::sync::atomic::Ordering::Relaxed) { "on" } else { "off" },
                res.evals, res.real_evals, res.seconds, cfg.pop, cfg.tournament
            );
            summary += "## Milestones (first candidate count where best train acc reached the reference rule)\n\n";
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
            eprintln!("usage: autoplast baselines | search [--task v3 --no-op A,B --extra-ops --seed N --budget N --pop N --threads N --batch N --no-split-edge --out DIR] | sweep | eval --prog FILE");
        }
    }
}

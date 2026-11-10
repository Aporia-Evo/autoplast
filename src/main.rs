mod classify;
mod evolve;
mod program;
mod reference;
mod rng;
mod task;

use program::{baselines, Program, Regs};
use std::fs;
use std::io::Write;
use std::sync::atomic::Ordering::Relaxed;
use task::{evaluate, Task, TaskCfg};

/// Held-out evaluation suites: fresh episodes and embeddings. The first five are the v1/v2
/// suites (all at load T/d = 0.75). The rest are the headroom regimes, which shift load,
/// episode length, rewrite pressure and key similarity.
fn test_suites() -> Vec<(&'static str, TaskCfg)> {
    let b = TaskCfg::search_default;
    let big = |name: &str, seed: u64| TaskCfg { n_episodes: 256, ..TaskCfg::regime(name, seed).unwrap() };
    vec![
        ("test d16 T12 ow0.3", TaskCfg { n_episodes: 512, ..b(2) }),
        ("test d16 T12 ow0.0", TaskCfg { n_episodes: 512, p_overwrite: 0.0, ..b(3) }),
        ("test d16 T12 ow0.6", TaskCfg { n_episodes: 512, p_overwrite: 0.6, ..b(4) }),
        ("test d32 T24 ow0.3", TaskCfg { d: 32, n_keys: 128, n_vals: 128, t_writes: 24, n_episodes: 256, ..b(5) }),
        ("test d8 T6 ow0.3", TaskCfg { d: 8, n_keys: 32, n_vals: 32, t_writes: 6, n_episodes: 512, ..b(6) }),
        ("full T24", big("full", 11)),
        ("overload T48", big("overload", 12)),
        ("rewrite8 T96", big("rewrite8", 13)),
        ("rewrite14 T96", big("rewrite14", 14)),
        ("clustered T12", TaskCfg { n_episodes: 512, ..big("clustered", 15) }),
        ("clustered8 T48", big("clustered8", 16)),
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

/// Search-space switches shared by all commands.
fn apply_space_flags(args: &[String]) {
    if has(args, "--no-split-edge") {
        program::SPLIT_EDGE.store(false, Relaxed);
    }
    if has(args, "--no-recip") {
        program::USE_RECIP.store(false, Relaxed);
    }
    program::PERSIST_M.store(arg(args, "--persist-m", 1usize).clamp(1, program::NM), Relaxed);
    program::PERSIST_V.store(arg(args, "--persist-v", 0usize).min(program::NV - 2), Relaxed);
}

/// Train task: regime, task seed and number of episodes from the command line.
/// Defaults (base, 1, 96) are the v2 task.
fn train_cfg(args: &[String]) -> (String, TaskCfg) {
    let name: String = arg(args, "--regime", "base".to_string());
    let seed: u64 = arg(args, "--task-seed", 1);
    let cfg = TaskCfg::regime(&name, seed).unwrap_or_else(|| {
        eprintln!("unknown regime {name}; known: {}", task::REGIMES.join(", "));
        std::process::exit(2)
    });
    (name, TaskCfg { n_episodes: arg(args, "--train-episodes", cfg.n_episodes), ..cfg })
}

/// Episodes the structural test takes its memory states from: same regime as the train task,
/// other embeddings and episodes.
fn classify_task(train: &TaskCfg) -> Task {
    Task::new(TaskCfg { n_episodes: 32, seed: train.seed + 1000, ..train.clone() })
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

fn baseline_table(train: &TaskCfg) -> String {
    let suites = test_suites();
    let ctask = classify_task(train);
    let mut s = String::from("| rule | structural class | train acc | ");
    s += &suites.iter().map(|(n, _)| *n).collect::<Vec<_>>().join(" | ");
    s += " |\n|---|---|---|";
    s += &"---|".repeat(suites.len());
    s += "\n";
    for (name, p) in baselines() {
        let tr = eval_on(&p, train);
        s += &format!("| {name} | {} | {:.3} |", classify::classify(&p, &ctask).family, tr.acc);
        for (_, cfg) in &suites {
            s += &format!(" {:.3} |", eval_on(&p, cfg).acc);
        }
        s += "\n";
    }
    s
}

fn report(prog: &Program, train: &TaskCfg) -> String {
    let eff = prog.effective();
    let tr = eval_on(prog, train);
    let mut s = format!(
        "{}\n\nEffective program ({} instructions):\n{}\n\nstructure: {}\n\ntrain acc {:.3} ±{:.3}\n",
        eff.formula(),
        eff.instrs.len(),
        eff.listing(),
        classify::classify(prog, &classify_task(train)).describe(),
        tr.acc,
        tr.se()
    );
    for (name, cfg) in test_suites() {
        let sc = eval_on(prog, &cfg);
        s += &format!("{name}: acc {:.3} ±{:.3}  margin {:.3}\n", sc.acc, sc.se(), sc.margin);
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
    let (regime, train) = train_cfg(args);
    let task = Task::new(train.clone());
    let mut regs = Regs::new(task.cfg.d);
    let suites = test_suites();
    let alphas = [0.7f32, 0.75, 0.8, 0.85, 0.9, 0.95, 0.98, 1.0, 1.02, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3];
    let steps = |n: usize| (1..=n).map(|i| i as f32 * 0.05).collect::<Vec<f32>>();
    let one = [1.0f32];
    println!(
        "regime {regime}, tuned on {} train episodes (task seed {}), commit {}\n",
        train.n_episodes,
        train.seed,
        git_commit(args)
    );
    println!("| family (tuned on train) | parameters | train | {} |", suites.iter().map(|x| x.0).collect::<Vec<_>>().join(" | "));
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
    apply_space_flags(&args);
    match cmd {
        "baselines" => {
            println!("{}", baseline_table(&train_cfg(&args).1));
            for (name, p) in baselines() {
                println!("{name}: {}", p.formula());
            }
        }
        "sweep" => sweep(&args),
        "eval" => {
            let path: String = arg(&args, "--prog", String::new());
            let text = fs::read_to_string(&path).expect("read prog");
            // the state budget a rule was found with is part of the rule
            let (pm, pv) = Program::json_budget(&text);
            program::PERSIST_M.store(pm, Relaxed);
            program::PERSIST_V.store(pv, Relaxed);
            let prog = Program::from_json(&text).expect("parse prog");
            println!("{}", report(&prog, &train_cfg(&args).1));
        }
        "search" => {
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
            let (regime, tcfg) = train_cfg(&args);
            let task = Task::new(tcfg.clone());
            let ctask = classify_task(&tcfg);
            let mut regs = Regs::new(task.cfg.d);
            let milestones: Vec<(String, f32)> = baselines()
                .into_iter()
                .skip(1)
                .map(|(n, p)| (n.to_string(), evaluate(&p.effective(), &task, &mut regs).acc))
                .collect();
            let mut log = fs::File::create(format!("{out}/log.csv")).unwrap();
            let family_of = |p: &Program| classify::classify(p, &ctask).family;
            let res = evolve::search(&cfg, &task, milestones, &family_of, &mut log);
            fs::write(format!("{out}/best.json"), res.best.prog.effective().to_json()).unwrap();
            let on = |b: bool| if b { "on" } else { "off" };
            let mut summary = format!(
                "# Search seed {}\n\ncommit: {}  regime: {regime}  task seed: {}  train episodes: {}\n\
                 add-node mutation: {}  reciprocal op: {}  persistent registers: {} matrix, {} vector\n\
                 candidates: {}  real evaluations (after cache): {}  time: {:.0}s  pop: {}  tournament: {}  batch: {}\n\n",
                cfg.seed,
                git_commit(&args),
                tcfg.seed,
                tcfg.n_episodes,
                on(program::SPLIT_EDGE.load(Relaxed)),
                on(program::USE_RECIP.load(Relaxed)),
                program::PERSIST_M.load(Relaxed),
                program::PERSIST_V.load(Relaxed),
                res.evals,
                res.real_evals,
                res.seconds,
                cfg.pop,
                cfg.tournament,
                cfg.batch
            );
            summary += "## Structural rediscovery (first candidate count at which the best rule belongs to a family)\n\n";
            for (fam, at) in &res.families {
                summary += &format!("* {fam}: {at} candidates\n");
            }
            summary += "\n## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)\n\n";
            for m in &res.milestones {
                summary += &format!(
                    "- {} (acc {:.3}): {}\n",
                    m.name,
                    m.acc,
                    m.hit_at.map_or("not reached".into(), |e| format!("{e} candidates"))
                );
            }
            summary += "\n## Best rule\n\n```\n";
            summary += &report(&res.best.prog, &tcfg);
            summary += "```\n";
            fs::write(format!("{out}/summary.md"), &summary).unwrap();
            print!("{summary}");
            std::io::stdout().flush().ok();
        }
        _ => {
            eprintln!(
                "usage: autoplast baselines | sweep | eval --prog FILE | search [--seed N --budget N --pop N --threads N --batch N --out DIR]\n\
                 task:   --regime {{{}}}  --task-seed N  --train-episodes N\n\
                 space:  --no-split-edge  --no-recip  --persist-m N (1..4)  --persist-v N (0..4)",
                task::REGIMES.join("|")
            );
        }
    }
}

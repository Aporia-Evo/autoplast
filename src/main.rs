mod evolve;
mod program;
mod rng;
mod task;

use program::{baselines, Program, Regs};
use std::fs;
use std::io::Write;
use task::{evaluate, Task, TaskCfg};

const TRAIN_TASK_SEED: u64 = 1;

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
    let train = TaskCfg::search_default(TRAIN_TASK_SEED);
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
    let train = eval_on(prog, &TaskCfg::search_default(TRAIN_TASK_SEED));
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
    match cmd {
        "baselines" => {
            println!("{}", baseline_table());
            for (name, p) in baselines() {
                println!("{name}: {}", p.formula());
            }
        }
        "eval" => {
            let path: String = arg(&args, "--prog", String::new());
            let prog = Program::from_json(&fs::read_to_string(&path).expect("read prog"))
                .expect("parse prog");
            println!("{}", report(&prog));
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
            let task = Task::new(TaskCfg::search_default(TRAIN_TASK_SEED));
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
                "# Search seed {}\n\ncandidates: {}  real evaluations (after cache): {}  time: {:.0}s  pop: {}  tournament: {}\n\n",
                cfg.seed, res.evals, res.real_evals, res.seconds, cfg.pop, cfg.tournament
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
            eprintln!("usage: rule-discovery baselines | search [--seed N --budget N --pop N --out DIR] | eval --prog FILE");
        }
    }
}

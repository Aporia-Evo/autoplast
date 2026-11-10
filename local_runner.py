"""Run the Rust search over many seeds on the local machine, a few processes at a time.

    python local_runner.py --seeds 1-16 --budget 1500000 --tag v2
    python local_runner.py --seeds 1-16 --budget 1500000 --tag v2-noaddnode --no-split-edge

Local counterpart of modal_runner.py (CPU work runs locally, see CLAUDE.md "Compute").
Results land in runs/<tag>/seed<N>/; runs/<tag>/aggregate.md has the same layout as the
Modal runner's, plus the wall time per seed. Seeds whose summary.md already exists are
skipped, so an interrupted run can be resumed with the same command.
If runs/<tag>/PAUSE exists, the runner exits at once without starting any seed (used to hold
a queued run until it is released by deleting the file).

    python local_runner.py --seeds 1-8 --tag r8-m2 --task-seed-from-seed --extra="--regime rewrite8 --train-episodes 192 --persist-m 2 --recip"

--extra is passed to `autoplast search` unchanged (write it as --extra="--flag value").
aggregate.md is written by aggregate.py (structural families first, accuracy levels second);
tags run before 10 Nov 2026 keep the aggregate.md they were committed with.
"""

import argparse
import concurrent.futures as cf
import pathlib
import re
import subprocess
import time

import aggregate as agg

ROOT = pathlib.Path(__file__).parent
TASK = "v2"
EXTRA_ARGS = []
TASK_SEED_FROM_SEED = False
COMMIT = "unknown"
EXE = ROOT / "target" / "release" / ("autoplast.exe" if (ROOT / "target/release/autoplast.exe").exists() else "autoplast")


def run_seed(seed, budget, tag, threads, no_split_edge):
    out = ROOT / "runs" / tag / f"seed{seed}"
    if (out / "summary.md").exists():
        return seed, None, "skipped (summary exists)"
    out.mkdir(parents=True, exist_ok=True)
    cmd = [str(EXE), "search", "--seed", str(seed), "--budget", str(budget),
           "--threads", str(threads), "--batch", str(16 * threads),
           "--log-every", "50000", "--out", str(out)]
    if no_split_edge:
        cmd.append("--no-split-edge")
    if TASK != "v2":
        cmd += ["--task", TASK]
    cmd += EXTRA_ARGS
    if TASK_SEED_FROM_SEED:
        cmd += ["--task-seed", str(seed)]
    cmd += ["--commit", COMMIT]
    t0 = time.time()
    with open(out / "stdout.txt", "w") as so, open(out / "stderr.txt", "w") as se:
        rc = subprocess.run(cmd, stdout=so, stderr=se).returncode
    wall = time.time() - t0
    (out / "wall_seconds.txt").write_text(f"{wall:.1f}\n")
    return seed, wall, f"exit {rc}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="1-4")
    ap.add_argument("--budget", type=int, default=1_500_000)
    ap.add_argument("--tag", default="v2")
    ap.add_argument("--parallel", "--jobs", type=int, default=2)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--no-split-edge", action="store_true")
    ap.add_argument("--task", default="v2")
    ap.add_argument("--no-op", default="")
    ap.add_argument("--extra-ops", action="store_true")
    ap.add_argument("--evolve-readout", action="store_true")
    ap.add_argument("--regime", default="")
    ap.add_argument("--recip", action="store_true")
    ap.add_argument("--task-seed-from-seed", action="store_true", help="pass --task-seed equal to the search seed")
    ap.add_argument("--extra", default="", help="passed to `autoplast search` unchanged; write it as --extra=\"--flag value\"")
    a = ap.parse_args()
    global TASK, EXTRA_ARGS, TASK_SEED_FROM_SEED, COMMIT
    TASK_SEED_FROM_SEED = a.task_seed_from_seed
    try:
        COMMIT = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or "unknown"
        if subprocess.run(["git", "status", "--porcelain", "--", "src", "Cargo.toml"], cwd=ROOT, capture_output=True, text=True).stdout.strip():
            COMMIT += "-dirty"
            print("WARNING: uncommitted changes in src/; results will be marked -dirty", flush=True)
    except OSError:
        pass  # git not available (sandbox): pass the commit through --extra="--commit <hash>"
    TASK = a.task
    EXTRA_ARGS = ((["--no-op", a.no_op] if a.no_op else []) + (["--extra-ops"] if a.extra_ops else [])
                  + (["--evolve-readout"] if a.evolve_readout else []) + (["--regime", a.regime] if a.regime else [])
                  + (["--recip"] if a.recip else []) + a.extra.split())
    lo, hi = (int(x) for x in a.seeds.split("-"))
    if (ROOT / "runs" / a.tag / "PAUSE").exists():
        print(f"runs/{a.tag}/PAUSE exists: not starting. Delete it to run.", flush=True)
        return
    t0 = time.time()
    print(f"{hi - lo + 1} seeds, {a.parallel} at a time x {a.threads} threads, budget {a.budget}", flush=True)
    with cf.ThreadPoolExecutor(a.parallel) as ex:
        futs = [ex.submit(run_seed, s, a.budget, a.tag, a.threads, a.no_split_edge) for s in range(lo, hi + 1)]
        for f in cf.as_completed(futs):
            seed, wall, status = f.result()
            print(f"seed {seed}: {status}" + (f", {wall:.0f} s" if wall else "") + f" (elapsed {time.time() - t0:.0f} s)", flush=True)
    print(agg.write(ROOT / "runs" / a.tag))
    print(f"total wall {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()

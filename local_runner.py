"""Run the search over many seeds on one machine (workstation or SSH host), several at a time.

    python local_runner.py --seeds 1-16 --budget 1500000 --tag v3 --jobs 2 --threads 8
    python local_runner.py --seeds 1-16 --budget 1500000 --tag v3-noaddnode --jobs 2 --threads 8 --extra="--no-split-edge"
    python local_runner.py --seeds 1-8 --tag r8-m1 --jobs 2 --threads 8 --task-seed-from-seed \
        --extra="--regime rewrite8 --train-episodes 192"

jobs x threads should not exceed the physical cores. Seeds that already have a summary.md are
skipped, so an interrupted tag can be resumed and split across machines (copy runs/<tag>/
together afterwards and run `python aggregate.py runs/<tag>`). Results depend on --batch, so
it is fixed here to the value modal_runner.py uses (128): a tag is comparable across machines.
"""

import argparse
import pathlib
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

import aggregate

ROOT = pathlib.Path(__file__).parent
BATCH = 128

ap = argparse.ArgumentParser()
ap.add_argument("--seeds", default="1-4")
ap.add_argument("--budget", type=int, default=1_500_000)
ap.add_argument("--tag", required=True)
ap.add_argument("--jobs", type=int, default=2)
ap.add_argument("--threads", type=int, default=8)
ap.add_argument("--task-seed-from-seed", action="store_true", help="pass --task-seed equal to the search seed")
ap.add_argument("--extra", default="", help="passed to `autoplast search` unchanged; write it as --extra=\"--flag value\"")
args = ap.parse_args()

subprocess.run(["cargo", "build", "--release"], cwd=ROOT, check=True)
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or "unknown"
dirty = subprocess.run(["git", "status", "--porcelain", "--", "src", "Cargo.toml"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
if dirty:
    commit += "-dirty"
    print("WARNING: uncommitted changes in src/; results will be marked -dirty")
lo, hi = (int(x) for x in args.seeds.split("-"))
base = ROOT / "runs" / args.tag


def run(seed: int):
    out = base / f"seed{seed}"
    if (out / "summary.md").exists():
        return seed, 0.0, "skipped"
    cmd = [str(ROOT / "target/release/autoplast"), "search", "--seed", str(seed), "--budget", str(args.budget),
           "--threads", str(args.threads), "--batch", str(BATCH), "--log-every", "50000",
           "--out", str(out), "--commit", commit] + args.extra.split()
    if args.task_seed_from_seed:
        cmd += ["--task-seed", str(seed)]
    t0 = time.time()
    r = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    return seed, time.time() - t0, "ok" if r.returncode == 0 else f"FAILED: {r.stderr[-300:]}"


t0 = time.time()
with ThreadPoolExecutor(args.jobs) as pool:
    for seed, secs, status in pool.map(run, range(lo, hi + 1)):
        print(f"seed {seed}: {status} ({secs / 60:.1f} min)", flush=True)
print(f"total wall time {(time.time() - t0) / 60:.1f} min\n")
print(aggregate.write(base))

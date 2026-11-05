"""Run the Rust search over many seeds on the local machine, a few processes at a time.

    python local_runner.py --seeds 1-16 --budget 1500000 --tag v2
    python local_runner.py --seeds 1-16 --budget 1500000 --tag v2-noaddnode --no-split-edge

Local counterpart of modal_runner.py (CPU work runs locally, see CLAUDE.md "Compute").
Results land in runs/<tag>/seed<N>/; runs/<tag>/aggregate.md has the same layout as the
Modal runner's, plus the wall time per seed. Seeds whose summary.md already exists are
skipped, so an interrupted run can be resumed with the same command.
If runs/<tag>/PAUSE exists, the runner exits at once without starting any seed (used to hold
a queued run until it is released by deleting the file).
"""

import argparse
import concurrent.futures as cf
import pathlib
import re
import subprocess
import time

ROOT = pathlib.Path(__file__).parent
TASK = "v2"
EXTRA_ARGS = []
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
    t0 = time.time()
    with open(out / "stdout.txt", "w") as so, open(out / "stderr.txt", "w") as se:
        rc = subprocess.run(cmd, stdout=so, stderr=se).returncode
    wall = time.time() - t0
    (out / "wall_seconds.txt").write_text(f"{wall:.1f}\n")
    return seed, wall, f"exit {rc}"


def parse_milestones(summary):
    hits = {}
    for name, val in re.findall(r"^- (.+?) \(acc [0-9.]+\): (.+)$", summary, flags=re.M):
        m = re.match(r"(\d+) candidates", val)
        hits[name] = int(m.group(1)) if m else None
    return hits


def aggregate(lo, hi, budget, tag, no_split_edge):
    base = ROOT / "runs" / tag
    rows, names = [], None
    for seed in range(lo, hi + 1):
        f = base / f"seed{seed}" / "summary.md"
        if not f.exists():
            continue
        s = f.read_text(encoding="utf-8")
        hits = parse_milestones(s)
        names = names or list(hits)
        formula = next((l for l in s.splitlines() if l.startswith("S' =")), "")
        w = base / f"seed{seed}" / "wall_seconds.txt"
        wall = float(w.read_text()) if w.exists() else None
        rows.append((seed, hits, formula, wall))
    if not rows:
        return ""
    lines = [f"# {tag}: {len(rows)} seeds, budget {budget}, task {TASK}{' ' + ' '.join(EXTRA_ARGS) if EXTRA_ARGS else ''}, add-node {'off' if no_split_edge else 'on'}, local", ""]
    lines.append("| seed | " + " | ".join(names) + " | wall s | best rule |")
    lines.append("|---|" + "---|" * (len(names) + 2))
    for seed, hits, formula, wall in rows:
        cells = [f"{hits[n]:,}" if hits[n] else "no" for n in names]
        ws = f"{wall:.0f}" if wall is not None else ""
        lines.append(f"| {seed} | " + " | ".join(cells) + f" | {ws} | `{formula[:120]}` |")
    lines.append("")
    for n in names:
        reached = sorted(h[n] for _, h, _, _ in rows if h[n])
        med = reached[len(reached) // 2] if reached else None
        lines.append(f"- {n}: reached by {len(reached)}/{len(rows)} seeds"
                     + (f", median {med:,} candidates" if med else ""))
    text = "\n".join(lines) + "\n"
    (base / "aggregate.md").write_text(text, encoding="utf-8")
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="1-4")
    ap.add_argument("--budget", type=int, default=1_500_000)
    ap.add_argument("--tag", default="v2")
    ap.add_argument("--parallel", type=int, default=2)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--no-split-edge", action="store_true")
    ap.add_argument("--task", default="v2")
    ap.add_argument("--no-op", default="")
    ap.add_argument("--extra-ops", action="store_true")
    ap.add_argument("--evolve-readout", action="store_true")
    ap.add_argument("--regime", default="")
    a = ap.parse_args()
    global TASK, EXTRA_ARGS
    TASK = a.task
    EXTRA_ARGS = ((["--no-op", a.no_op] if a.no_op else []) + (["--extra-ops"] if a.extra_ops else [])
                  + (["--evolve-readout"] if a.evolve_readout else []) + (["--regime", a.regime] if a.regime else []))
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
    print(aggregate(lo, hi, a.budget, a.tag, a.no_split_edge))
    print(f"total wall {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()

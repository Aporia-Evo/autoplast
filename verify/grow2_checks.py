"""Checks fixed for growth-loop v2 rules at 0.85 or above (README, "Growth loop, second version").

    python verify/grow2_checks.py runs/grow2/armB2_task5/best.json ...

For each rule:
1. Rust `eval` on the run's own task seed (train, collision3 test, T64/T128 K8).
2. 12 fresh draws of collision3 (task seeds 101 to 112, 512 train episodes), paired against
   tuned DeltaNet (e = 0.5) and hand-written tuned Kalman delta (delta 0.01, q 0.003), as in
   `verify/d_checks.py`. Hand-written rules are references only (CLAUDE.md rule 6).
3. JAX on the collision3 test dump: float32 at Normalize epsilon 1e-6, float64 at 1e-9, and
   `verify/eps_scale.py` (ratio of max|S| at epsilon 1e-3 and 1e-6; near 1000 = scale trick).
"""
import json
import pathlib
import re
import statistics as st
import subprocess
import sys

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "verify"))
from d_checks import KALMAN, SEEDS, acc, paired, save  # noqa: E402
from c1_checks import delta  # noqa: E402

EXE = str(ROOT / "target/release/autoplast")
SPACE = ["--regime", "collision3", "--recip", "--persist-m", "3", "--persist-init", "identity"]


def task_seed(path):
    return int(re.search(r"task(\d+)", path).group(1))


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT).stdout


if __name__ == "__main__":
    paths = sys.argv[1:]
    out = ROOT / "runs/grow2/checks"
    out.mkdir(parents=True, exist_ok=True)
    dump = out / "test_dump.json"
    if not dump.exists():
        run([EXE, "dump", "--split", "test", "--out", str(dump)] + SPACE + ["--task-seed", "1"])
    base = [acc(save(delta(1.0, 0.5), "d.json"), s) for s in SEEDS]
    kal = [acc(KALMAN[1], s) for s in SEEDS]
    print(f"fresh draws: tuned DeltaNet {st.mean(base):.3f}, tuned Kalman delta {st.mean(kal):.3f}\n")
    for p in paths:
        print(f"## {p}\n")
        rep = run([EXE, "eval", "--prog", p] + SPACE + ["--task-seed", str(task_seed(p))])
        print("```\n" + rep.strip() + "\n```")
        r = [acc(p, s) for s in SEEDS]
        print(f"fresh draws: {paired(r, base)} against DeltaNet; {paired(r, kal)} against Kalman delta")
        j32 = run(["python3", "verify/verify.py", "--task-json", str(dump), p])
        j64 = run(["python3", "verify/verify.py", "--x64", "--norm-eps", "1e-9", "--task-json", str(dump), p])
        es = run(["python3", "verify/eps_scale.py", "--task-json", str(dump), p])
        pick = lambda s: [l for l in s.splitlines() if p in l or "acc" in l.lower()][-3:]
        print("JAX float32 eps 1e-6:", *pick(j32), sep="\n  ")
        print("JAX float64 eps 1e-9:", *pick(j64), sep="\n  ")
        print("eps scale:", es.strip(), "\n", flush=True)

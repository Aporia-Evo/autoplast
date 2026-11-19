"""d-kalman seed 9 on clustered8, a regime it was never searched on (README, "clustered8").

    python verify/c8_checks.py

Kalman delta written in the search space (`verify/probe_path_kalman.py`, β = 1, c = 1) is tuned
on the clustered8 train task (task seed 1) over δ and q; the evolved rule keeps the constants it
was found with on collision3. Then 12 fresh draws (task seeds 101 to 112, 512 episodes), paired.
Hand-written programs are references only (CLAUDE.md rule 6).
"""
import itertools
import json
import pathlib
import re
import statistics as st
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "verify"))
import probe_path_kalman as P  # noqa: E402
from c1_checks import delta  # noqa: E402

EXE = ROOT / "target/release/autoplast"
TMP = pathlib.Path(tempfile.mkdtemp())


def save(prog, name):
    p = TMP / name
    p.write_text(json.dumps(prog))
    return str(p)


def acc(path, seed=1, n=None, test=False):
    cmd = [str(EXE), "eval", "--prog", path, "--regime", "clustered8", "--recip", "--task-seed", str(seed)]
    if n:
        cmd += ["--train-episodes", str(n)]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    if test:
        return float(re.search(r"test regime clustered8: acc ([0-9.]+)", out).group(1))
    return float(re.search(r"train acc ([0-9.]+)", out).group(1))


if __name__ == "__main__":
    grid = list(itertools.product([0.003, 0.01, 0.03, 0.1, 0.3, 1.0], [0.0, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0]))
    kal = max(grid, key=lambda g: acc(save(P.prog(beta=1.0, delta=g[0], c=1.0, q=g[1]), "k.json")))
    kpath = save(P.prog(beta=1.0, delta=kal[0], c=1.0, q=kal[1]), "kbest.json")
    e_best = max([0.2, 0.3, 0.35, 0.4, 0.5, 0.7, 1.0], key=lambda e: acc(save(delta(1.0, e), "d.json")))
    dpath = save(delta(1.0, e_best), "dbest.json")
    rules = [("tuned DeltaNet (e=%s)" % e_best, dpath), ("Kalman delta in the space (δ=%s, q=%s)" % kal, kpath),
             ("d-kalman seed 9, as found on collision3", str(ROOT / "runs/d-kalman/seed9/best.json"))]
    print("| rule | clustered8 test (task seed 1) | mean over 12 fresh draws | gain over Kalman delta ± s.e., draws won |\n|---|---|---|---|")
    kd = [acc(kpath, s, 512) for s in range(101, 113)]
    for name, p in rules:
        r = [acc(p, s, 512) for s in range(101, 113)]
        d = [x - y for x, y in zip(r, kd)]
        print(f"| {name} | {acc(p, test=True):.3f} | {st.mean(r):.3f} | {st.mean(d):+.3f} ± {st.stdev(d) / len(d) ** 0.5:.3f}, {sum(x > 0 for x in d)}/12 |", flush=True)

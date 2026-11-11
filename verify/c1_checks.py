"""Checks on the package-C rules (runs/c-m2), all with the Rust binary on fresh task draws.

    python verify/c1_checks.py draws      # 12 fresh draws of collision3, paired against tuned DeltaNet
    python verify/c1_checks.py closed     # closed form of seed 2 and ablation of its read-side erase
    python verify/c1_checks.py gap        # control: extra unqueried writes before the queries

Accuracy is that of `autoplast eval --regime collision3 --task-seed N --train-episodes 512`
(256 short and 256 long episodes), task seeds 101 to 112. Hand-written programs here are
references and ablations only (CLAUDE.md rule 6).
"""

import json
import pathlib
import re
import statistics as st
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "verify"))
from probe_two_state import program as probe  # noqa: E402

EXE = ROOT / "target/release/autoplast"
SEEDS = range(101, 113)
TMP = pathlib.Path(tempfile.mkdtemp())


def ins(op, out, a=0, b=0, c=0.0):
    return {"op": op, "out": out, "a": a, "b": b, "c": c}


def delta(a, e):
    """S' = a·S(I − e·kkᵀ) + e·v kᵀ"""
    return {"instrs": [ins("Const", 0, c=e), ins("MatVec", 2, 0, 0), ins("Outer", 1, 2, 0), ins("MatScale", 1, 0, 1),
                       ins("MatSub", 0, 0, 1), ins("Const", 1, c=a), ins("MatScale", 0, 1, 0), ins("Outer", 3, 1, 0),
                       ins("MatScale", 3, 0, 3), ins("MatAdd", 0, 0, 3)]}


def closed(r, e=0.490, rho=0.990):
    """Seed 2 of c-m2 in closed form: P' = rho·(P + v kᵀ)(I − e·kkᵀ), S' = (P + v kᵀ)(I − r·kkᵀ)."""
    return {"persist_m": 2, "persist_v": 0, "instrs": [
        ins("Outer", 2, 1, 0), ins("MatAdd", 2, 1, 2), ins("MatVec", 2, 2, 0), ins("Outer", 3, 2, 0),
        ins("Const", 0, c=r), ins("MatScale", 0, 0, 3), ins("MatSub", 0, 2, 0),
        ins("Const", 1, c=e), ins("MatScale", 3, 1, 3), ins("MatSub", 1, 2, 3), ins("Const", 2, c=rho), ins("MatScale", 1, 2, 1)]}


def save(prog, name):
    p = TMP / name
    p.write_text(json.dumps(prog))
    return str(p)


def acc(path, seed, gap=0):
    out = subprocess.run([str(EXE), "eval", "--prog", path, "--regime", "collision3", "--task-seed", str(seed),
                          "--train-episodes", "512", "--query-gap", str(gap)], capture_output=True, text=True).stdout
    return float(re.search(r"train acc ([0-9.]+)", out).group(1))


def paired(r, base):
    d = [x - y for x, y in zip(r, base)]
    return f"{st.mean(r):.3f} ({st.mean(d):+.3f} ± {st.stdev(d) / len(d) ** 0.5:.3f}, {sum(x > 0 for x in d)}/{len(d)})"


RULES = [("hand probe", save(probe(0.9, 0.3, 0.85), "probe.json")),
         ("c-m2 seed 2", str(ROOT / "runs/c-m2/seed2/best.json")),
         ("c-m2 seed 9", str(ROOT / "runs/c-m2/seed9/best.json")),
         ("c-m2 seed 6", str(ROOT / "runs/c-m2/seed6/best.json"))]

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "draws"
    if what == "draws":
        base = [acc(save(delta(1.0, 0.5), "d.json"), s) for s in SEEDS]
        rows = [("tuned Gated DeltaNet (a=1.01, e=0.5)", save(delta(1.01, 0.5), "g.json"))] + RULES + [
            ("c-m2 seed 1 (second state unused)", str(ROOT / "runs/c-m2/seed1/best.json")),
            ("5a-A seed 2 (best one-state rule of 5a)", str(ROOT / "runs/5a-A/seed2/best.json"))]
        print(f"| rule | mean (paired gain over tuned DeltaNet ± s.e., draws won) |\n|---|---|\n| tuned DeltaNet (e=0.5) | {st.mean(base):.3f} |")
        for name, p in rows:
            print(f"| {name} | {paired([acc(p, s) for s in SEEDS], base)} |", flush=True)
    elif what == "closed":
        print("| read-side erase r | mean over 12 draws |\n|---|---|")
        for r in [0.0, 0.49, 0.7, 0.85, 0.956, 1.0]:
            print(f"| {r} | {st.mean(acc(save(closed(r), 'c.json'), s) for s in SEEDS):.3f} |", flush=True)
    elif what == "gap":
        print("| extra unqueried writes | DeltaNet, best e on these draws | " + " | ".join(n for n, _ in RULES) + " |")
        print("|---|---|" + "---|" * len(RULES))
        for gap in [0, 1, 2, 4]:
            best = max(([e, [acc(save(delta(1.0, e), "d.json"), s, gap) for s in SEEDS]] for e in [0.4, 0.5, 0.6, 0.7]), key=lambda x: st.mean(x[1]))
            cells = [paired([acc(p, s, gap) for s in SEEDS], best[1]) for _, p in RULES]
            print(f"| {gap} | {st.mean(best[1]):.3f} (e={best[0]}) | " + " | ".join(cells) + " |", flush=True)

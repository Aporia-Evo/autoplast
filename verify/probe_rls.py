"""Hand-written reference: recursive least squares with a forgetting factor, written in the
search space with a second state that starts at the identity (`--persist-init identity`) and
the scalar reciprocal (`--recip`). Reference only (CLAUDE.md rule 6): never a candidate or seed.

    g  = P k / (delta + kᵀP k)
    S' = S + (v − S k) gᵀ
    P' = rho · (P − g (P k)ᵀ)            P₀ = I

rho = 1 and delta = 1 is plain RLS; rho > 1 forgets (rho = 1/λ). 14 instructions.

Second family, the Kalman delta rule, needs the identity at every step. It is held in a third
persistent register that the rule never writes (`--persist-m 3`), 15 instructions:

    P' = P − g (P k)ᵀ + q · I

    python verify/probe_rls.py [regime]          # both grids, default collision3
"""

import itertools
import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).parent.parent
EXE = ROOT / "target/release/autoplast"


def program(delta, rho):
    def ins(op, out, a=0, b=0, c=0.0):
        return {"op": op, "out": out, "a": a, "b": b, "c": c}

    return {
        "persist_m": 2,
        "persist_v": 0,
        "persist_identity": 1,
        "instrs": [
            ins("MatVec", 2, 1, 0),  # V2 = P k
            ins("Dot", 0, 0, 2),  # s0 = kᵀP k
            ins("Const", 1, c=delta),
            ins("SAdd", 0, 0, 1),
            ins("Recip", 0, 0),  # s0 = 1 / (delta + kᵀP k)
            ins("VecScale", 3, 0, 2),  # V3 = g
            ins("MatVec", 4, 0, 0),  # V4 = S k
            ins("VecSub", 5, 1, 4),  # V5 = v − S k
            ins("Outer", 2, 5, 3),
            ins("MatAdd", 0, 0, 2),  # S' = S + (v − S k) gᵀ
            ins("Outer", 3, 3, 2),  # g (P k)ᵀ
            ins("MatSub", 1, 1, 3),
            ins("Const", 2, c=rho),
            ins("MatScale", 1, 2, 1),  # P' = rho (P − g (P k)ᵀ)
        ],
    }


def kalman(delta, q):
    def ins(op, out, a=0, b=0, c=0.0):
        return {"op": op, "out": out, "a": a, "b": b, "c": c}

    return {
        "persist_m": 3,
        "persist_v": 0,
        "persist_identity": 1,
        "instrs": [
            ins("MatVec", 2, 1, 0),
            ins("Dot", 0, 0, 2),
            ins("Const", 1, c=delta),
            ins("SAdd", 0, 0, 1),
            ins("Recip", 0, 0),
            ins("VecScale", 3, 0, 2),  # V3 = g
            ins("MatVec", 4, 0, 0),
            ins("VecSub", 5, 1, 4),
            ins("Outer", 3, 5, 3),
            ins("MatAdd", 0, 0, 3),  # S' = S + (v − S k) gᵀ
            ins("Outer", 3, 3, 2),
            ins("MatSub", 1, 1, 3),  # P − g (P k)ᵀ
            ins("Const", 2, c=q),
            ins("MatScale", 3, 2, 2),  # q · I, with I in M2
            ins("MatAdd", 1, 1, 3),
        ],
    }


def grid(family, settings, regime):
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp) / "p.json"
        for a, b in settings:
            path.write_text(json.dumps(family(a, b)))
            out = subprocess.run([str(EXE), "eval", "--prog", str(path), "--regime", regime], capture_output=True, text=True).stdout
            acc = lambda key: float(re.search(r"acc ([0-9.]+)", next(l for l in out.splitlines() if l.startswith(key))).group(1))
            rows.append((a, b, acc("train acc"), acc(f"test regime {regime}"), acc("test d16 T64 K8"), acc("test d16 T128 K8")))
    return rows


if __name__ == "__main__":
    regime = sys.argv[1] if len(sys.argv) > 1 else "collision3"
    for title, names, family, settings in [
        ("RLS with forgetting, two states", "delta | rho", program,
         itertools.product([0.01, 0.03, 0.1, 0.3, 1.0], [1.0, 1.02, 1.05, 1.1, 1.2, 1.4, 1.7, 2.0])),
        ("Kalman delta, identity in a third register", "delta | q", kalman,
         itertools.product([0.01, 0.03, 0.1, 0.3, 1.0], [0.003, 0.01, 0.02, 0.03, 0.1, 0.3, 1.0, 3.0])),
    ]:
        rows = grid(family, settings, regime)
        print(f"\n### {title}: best 6 by train\n\n| {names} | train | test {regime} | T64 K8 | T128 K8 |\n|---|---|---|---|---|---|")
        for r in sorted(rows, key=lambda r: -r[2])[:6]:
            print("| " + " | ".join(str(x) for x in r) + " |")
        ok = sorted((r for r in rows if r[5] >= 0.838), key=lambda r: -r[2])[:3]
        print("\nbest by train with T128 K8 >= 0.838:" + (" none" if not ok else ""))
        for r in ok:
            print("| " + " | ".join(str(x) for x in r) + " |")

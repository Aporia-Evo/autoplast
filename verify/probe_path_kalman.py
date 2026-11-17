"""Fitness landscape between the delta rule and the Kalman delta rule, in the search space of
packages D and E (collision3, `--persist-m 3 --persist-init identity --recip`).

Hand-written programs, references only (CLAUDE.md rule 6). Each family below is one more
piece of the Kalman delta rule added to the delta rule; the best setting of its constants is
reported with the train accuracy the search sees.

    python verify/probe_path_kalman.py

Registers: M0 = S, M1 = P (persistent, starts at I), M2 = I (persistent, never written),
V0 = k, V1 = v.
"""

import itertools
import json
import pathlib
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).parent.parent
EXE = ROOT / "target/release/autoplast"


def ins(op, out, a=0, b=0, c=0.0):
    return {"op": op, "out": out, "a": a, "b": b, "c": c}


def prog(beta=1.0, delta=0.01, c=1.0, q=0.0, normalise=True, p_update=True, q_term=True):
    """S' = S + β (v − S k) gᵀ,  g = P k / (δ + kᵀ P k)  (or g = P k without normalise),
    P' = P − c·g (P k)ᵀ + q·I."""
    p = [ins("MatVec", 2, 1, 0)]  # V2 = P k
    if normalise:
        p += [ins("Dot", 0, 0, 2), ins("Const", 1, c=delta), ins("SAdd", 0, 0, 1), ins("Recip", 0, 0), ins("VecScale", 3, 0, 2)]
    else:
        p += [ins("Const", 0, c=1.0), ins("VecScale", 3, 0, 2)]
    p += [ins("MatVec", 4, 0, 0), ins("VecSub", 5, 1, 4), ins("Const", 3, c=beta), ins("VecScale", 5, 3, 5),
          ins("Outer", 3, 5, 3), ins("MatAdd", 0, 0, 3)]
    if p_update:
        p += [ins("Outer", 3, 3, 2), ins("Const", 2, c=c), ins("MatScale", 3, 2, 3), ins("MatSub", 1, 1, 3)]
    if q_term:
        p += [ins("Const", 2, c=q), ins("MatScale", 3, 2, 2), ins("MatAdd", 1, 1, 3)]
    return {"persist_m": 3, "persist_v": 0, "persist_identity": 1, "instrs": p}


TMP = pathlib.Path(tempfile.mkdtemp())


def ev(args):
    i, p = args
    f = TMP / f"{i}.json"
    f.write_text(json.dumps(p))
    out = subprocess.run([str(EXE), "eval", "--prog", str(f), "--regime", "collision3"], capture_output=True, text=True).stdout
    g = lambda k: float(re.search(re.escape(k) + r".*?acc ([0-9.]+)", out).group(1))
    return float(re.search(r"train acc ([0-9.]+)", out).group(1)), g("test regime collision3"), g("test d16 T128 K8 ow0.3"), len(p["instrs"])


def best(name, grid, make):
    with ThreadPoolExecutor(4) as ex:
        rs = list(ex.map(ev, enumerate(make(*x) for x in grid)))
    k = max(range(len(rs)), key=lambda i: rs[i][0])
    print(f"| {name} | {grid[k]} | {rs[k][0]:.3f} | {rs[k][1]:.3f} | {rs[k][2]:.3f} | {rs[k][3]} |", flush=True)


if __name__ == "__main__":
    B, D = [0.3, 0.5, 0.7, 0.9, 1.0], [0.003, 0.01, 0.03, 0.1, 0.3, 1.0]
    print("| step | best constants | train | test collision3 | T128 K8 | instructions |\n|---|---|---|---|---|---|")
    best("A delta rule", [(b,) for b in B], lambda b: prog(beta=b, normalise=False, p_update=False, q_term=False))
    best("B gain k/(δ + kᵀPk), P = I fixed", list(itertools.product(B, D)), lambda b, d: prog(beta=b, delta=d, p_update=False, q_term=False))
    best("C B + P' = P + qI only", list(itertools.product([1.0], D, [0.001, 0.01, 0.1, 1.0])), lambda b, d, q: prog(beta=b, delta=d, q=q, p_update=False))
    for c in [0.02, 0.05, 0.1, 0.2, 0.5]:
        best(f"D' g = Pk unnormalised, P' = P − {c}·(Pk)(Pk)ᵀ", [(b,) for b in [0.3, 0.5, 0.7, 1.0]], lambda b, c=c: prog(beta=b, c=c, normalise=False, q_term=False))
    for c in [0.05, 0.2, 0.5, 1.0]:
        best(f"D B + P' = P − {c}·g(Pk)ᵀ, no q", list(itertools.product([0.5, 1.0], D)), lambda b, d, c=c: prog(beta=b, delta=d, c=c, q_term=False))
    for c in [0.05, 0.2, 0.5, 1.0]:
        best(f"E B + P' = P − {c}·g(Pk)ᵀ + qI", list(itertools.product([1.0], [0.01, 0.1], [0.003, 0.01, 0.03, 0.1])), lambda b, d, q, c=c: prog(beta=b, delta=d, c=c, q=q))

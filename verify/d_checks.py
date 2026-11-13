"""Checks on the package-D rules (runs/d-kalman) with the Rust binary on fresh task draws.

    python verify/d_checks.py draws     # 12 fresh draws of collision3, paired against tuned DeltaNet
    python verify/d_checks.py closed    # closed form of seed 9 and its ablations
    python verify/d_checks.py gap       # control: extra unqueried writes before the queries

Accuracy as in verify/c1_checks.py: `autoplast eval --regime collision3 --task-seed N
--train-episodes 512`, task seeds 101 to 112. Hand-written programs are references and
ablations only (CLAUDE.md rule 6).
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
from c1_checks import delta, ins  # noqa: E402
from probe_rls import kalman  # noqa: E402

EXE = ROOT / "target/release/autoplast"
SEEDS = range(101, 113)
TMP = pathlib.Path(tempfile.mkdtemp())


def closed9(c=6.0, rho=0.80, exact=False, sub_p=True, squash=True, faithful=False):
    """Seed 9 of d-kalman in closed form (P1, P2 start as the identity):
        u   = norm(P1ᵀ k)                     the part of k not yet covered by earlier keys
        P1' = P1 − (P1 k) uᵀ                  (exact=True: P1 − u uᵀ, a true projector update)
        Y   = P2 + c · norm(tanh v) uᵀ        (squash=False: c · v uᵀ)
        P2' = rho · Y
        S'  = Y − P1'                         (sub_p=False: S' = Y)
    """
    prog = [ins("Transpose", 3, 1), ins("MatVec", 2, 3, 0)]
    if faithful:
        # as found: the residual is scaled by 0.25 before Normalize (x / (|x| + 1e-6)), so a
        # residual near 1e-6 gives a short u, and P1 k is scaled by <u, u>. Together they make
        # the write vanish when the key is already fully covered.
        prog += [ins("Const", 2, c=0.25), ins("VecScale", 2, 2, 2), ins("Normalize", 2, 2), ins("Dot", 3, 2, 2),
                 ins("VecScale", 3, 3, 0), ins("MatVec", 3, 1, 3), ins("Outer", 3, 3, 2)]
    else:
        prog += [ins("Normalize", 2, 2)]
        prog += [ins("Outer", 3, 2, 2)] if exact else [ins("MatVec", 3, 1, 0), ins("Outer", 3, 3, 2)]
    prog += [ins("Tanh", 4, 1), ins("Normalize", 4, 4)] if squash else [ins("VecAdd", 4, 1, 5)]
    prog += [ins("Const", 0, c=c), ins("VecScale", 4, 0, 4), ins("Outer", 0, 4, 2), ins("MatAdd", 0, 2, 0),
             ins("Const", 1, c=rho), ins("MatScale", 2, 1, 0), ins("MatSub", 1, 1, 3)]
    if sub_p:
        prog.append(ins("MatSub", 0, 0, 1))
    return {"persist_m": 3, "persist_v": 0, "persist_identity": 1, "instrs": prog}


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


FOUND = [(f"d-kalman seed {s}", str(ROOT / f"runs/d-kalman/seed{s}/best.json")) for s in (9, 7, 2, 15)]
KALMAN = ("Kalman delta, hand-written (δ=0.01, q=0.003)", save(kalman(0.01, 0.003), "k.json"))

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "draws"
    if what == "draws":
        base = [acc(save(delta(1.0, 0.5), "d.json"), s) for s in SEEDS]
        print(f"| rule | mean (paired gain over tuned DeltaNet ± s.e., draws won) |\n|---|---|\n| tuned DeltaNet (e=0.5) | {st.mean(base):.3f} |")
        for name, p in FOUND + [("c-m2 seed 2 (best rule of C1)", str(ROOT / "runs/c-m2/seed2/best.json")), KALMAN]:
            print(f"| {name} | {paired([acc(p, s) for s in SEEDS], base)} |", flush=True)
    elif what == "closed":
        variants = [("seed 9 as found", str(ROOT / "runs/d-kalman/seed9/best.json")),
                    ("closed form with the 0.25 scale and <u,u> as found", save(closed9(faithful=True), "a0.json")),
                    ("closed form with the 0.25 scale, without −P1' in S'", save(closed9(faithful=True, sub_p=False), "a1.json")),
                    ("closed form (c=6, rho=0.80), residual normalised without the scale", save(closed9(), "a.json")),
                    ("closed form without −P1' in S'", save(closed9(sub_p=False), "b.json")),
                    ("closed form with plain v instead of norm(tanh v)", save(closed9(squash=False), "c.json")),
                    ("closed form with exact projector update P1 − u uᵀ", save(closed9(exact=True), "e.json")),
                    ("closed form, rho=1.0 (no decay)", save(closed9(rho=1.0), "f.json")),
                    ("closed form, rho=0.9", save(closed9(rho=0.9), "g.json")),
                    ("closed form, rho=0.6", save(closed9(rho=0.6), "h.json")),
                    ("closed form, c=1", save(closed9(c=1.0), "i.json")),
                    ("closed form, c=20", save(closed9(c=20.0), "j.json"))]
        print("| variant | mean over 12 draws |\n|---|---|")
        for name, p in variants:
            print(f"| {name} | {st.mean(acc(p, s) for s in SEEDS):.3f} |", flush=True)
    elif what == "gap":
        rules = FOUND[:2] + [KALMAN]
        print("| extra unqueried writes | DeltaNet, best e on these draws | " + " | ".join(n for n, _ in rules) + " |")
        print("|---|---|" + "---|" * len(rules))
        for gap in [0, 1, 2, 4]:
            best = max(([e, [acc(save(delta(1.0, e), "d.json"), s, gap) for s in SEEDS]] for e in [0.4, 0.5, 0.6, 0.7]), key=lambda x: st.mean(x[1]))
            cells = [paired([acc(p, s, gap) for s in SEEDS], best[1]) for _, p in rules]
            print(f"| {gap} | {st.mean(best[1]):.3f} (e={best[0]}) | " + " | ".join(cells) + " |", flush=True)

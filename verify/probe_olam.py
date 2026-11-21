"""Hand-written reference (CLAUDE.md rule 6: never a candidate, seed or mutation): RLS covariance
update with a separate regulariser in the memory write, which turns the RLS average into a
replacement for repeated keys (recursive optimal linear associative memory, Kohonen 1977; the
pseudo-inverse limit is Greville 1960).

    P' = P − (P k)(P k)ᵀ / (deltaP + kᵀP k)          P₀ = I
    S' = S + (v − S k)(P k)ᵀ / (eps + kᵀP k)

With eps = deltaP this is plain RLS (`verify/probe_rls.py`, rho = 1). With eps → 0 the write
gain is the dual vector of k in the metric of P: S k = v exactly after the write, and other
stored keys are disturbed only through the regulariser deltaP. 16 instructions,
`--persist-m 2 --persist-init identity --recip`.

    python verify/probe_olam.py [regime]
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


def program(delta_p, eps):
    def ins(op, out, a=0, b=0, c=0.0):
        return {"op": op, "out": out, "a": a, "b": b, "c": c}

    return {"persist_m": 2, "persist_v": 0, "persist_identity": 1, "instrs": [
        ins("MatVec", 2, 1, 0),      # V2 = P k
        ins("Dot", 0, 0, 2),         # s0 = kᵀP k
        ins("Const", 1, c=eps),
        ins("SAdd", 1, 0, 1),
        ins("Recip", 1, 1),          # s1 = 1 / (eps + kᵀP k)
        ins("VecScale", 3, 1, 2),    # V3 = write gain
        ins("MatVec", 4, 0, 0),      # V4 = S k
        ins("VecSub", 5, 1, 4),      # V5 = v − S k
        ins("Outer", 2, 5, 3),
        ins("MatAdd", 0, 0, 2),      # S' = S + (v − S k) gᵀ
        ins("Const", 2, c=delta_p),
        ins("SAdd", 2, 0, 2),
        ins("Recip", 2, 2),          # s2 = 1 / (deltaP + kᵀP k)
        ins("VecScale", 3, 2, 2),
        ins("Outer", 2, 3, 2),       # (P k)(P k)ᵀ / (deltaP + kᵀP k)
        ins("MatSub", 1, 1, 2),      # P'
    ]}


def run(prog, args):
    with tempfile.TemporaryDirectory() as tmp:
        p = pathlib.Path(tmp) / "p.json"
        p.write_text(json.dumps(prog))
        return subprocess.run([str(EXE)] + args(p), capture_output=True, text=True).stdout


if __name__ == "__main__":
    regime = sys.argv[1] if len(sys.argv) > 1 else "collision3"
    flags = ["--regime", regime, "--recip", "--persist-m", "2", "--persist-init", "identity"]
    rows = []
    for dp, eps in itertools.product([0.01, 0.03, 0.1, 0.3, 1.0, 3.0], [0.0, 0.001, 0.01, 0.03, 0.1, 0.3]):
        out = run(program(dp, eps), lambda p: ["eval", "--prog", str(p)] + flags)
        acc = lambda key: float(re.search(r"acc ([0-9.]+)", next(l for l in out.splitlines() if l.startswith(key))).group(1))
        rows.append((dp, eps, acc("train acc"), acc(f"test regime {regime}"), acc("test d16 T64 K8"), acc("test d16 T128 K8")))
    print(f"\n### RLS covariance, separate write regulariser: best 8 by train ({regime})\n")
    print("| deltaP | eps | train | test | T64 K8 | T128 K8 |\n|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: -r[2])[:8]:
        print("| " + " | ".join(str(x) for x in r) + " |")
    print("\neps = deltaP (plain RLS) for comparison:")
    for r in rows:
        if r[0] == r[1]:
            print("| " + " | ".join(str(x) for x in r) + " |")

"""Hand-written probe: is there anything above tuned DeltaNet on collision3 once a rule may
keep a second d x d state? Reference only (CLAUDE.md rule 6): never a candidate, never a seed.

    S' = S + beta * (v - S k) (k - c * G k)^T        G' = rho * (G + k k^T)

G is a decayed sum of key outer products, kept in the persistent register M1; the write key is
pushed away from recently written keys. 14 instructions of the default 19-op alphabet, run by
the Rust binary with the state budget of the program file (persist_m = 2).

    python verify/probe_two_state.py            # grid on --regime collision3
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


def program(beta, c, rho):
    def ins(op, out, a=0, b=0, cc=0.0):
        return {"op": op, "out": out, "a": a, "b": b, "c": cc}

    return {
        "persist_m": 2,
        "persist_v": 0,
        "instrs": [
            ins("MatVec", 2, 1, 0),  # V2 = G k
            ins("Const", 0, cc=c),
            ins("VecScale", 2, 0, 2),
            ins("VecSub", 3, 0, 2),  # V3 = k - c G k
            ins("MatVec", 4, 0, 0),  # V4 = S k
            ins("VecSub", 5, 1, 4),  # V5 = v - S k
            ins("Const", 1, cc=beta),
            ins("VecScale", 5, 1, 5),
            ins("Outer", 2, 5, 3),
            ins("MatAdd", 0, 0, 2),  # S' = S + beta (v - S k)(k - c G k)^T
            ins("Outer", 3, 0, 0),
            ins("MatAdd", 1, 1, 3),
            ins("Const", 2, cc=rho),
            ins("MatScale", 1, 2, 1),  # G' = rho (G + k k^T)
        ],
    }


if __name__ == "__main__":
    regime = sys.argv[1] if len(sys.argv) > 1 else "collision3"
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp) / "p.json"
        grid = itertools.product([0.5, 0.7, 0.9], [0.0, 0.1, 0.2, 0.3, 0.45, 0.6], [0.3, 0.5, 0.7, 0.85])
        for beta, c, rho in grid:
            path.write_text(json.dumps(program(beta, c, rho)))
            out = subprocess.run([str(EXE), "eval", "--prog", str(path), "--regime", regime], capture_output=True, text=True).stdout
            acc = lambda key: float(re.search(r"acc ([0-9.]+)", next(l for l in out.splitlines() if l.startswith(key))).group(1))
            rows.append((beta, c, rho, acc("train acc"), acc(f"test regime {regime}"), acc("test d16 T128 K8")))
    print(f"| beta | c | rho | train | test {regime} | T128 K8 |\n|---|---|---|---|---|---|")
    plain = max((r for r in rows if r[1] == 0.0), key=lambda r: r[3])
    print("| " + " | ".join(str(x) for x in plain) + " |   (c = 0: plain delta rule, best by train)")
    for r in sorted(rows, key=lambda r: -r[3])[:5]:
        print("| " + " | ".join(str(x) for x in r) + " |")

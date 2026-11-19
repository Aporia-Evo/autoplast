"""Reference probe (CLAUDE.md rule 6): is clustered8 solved by an obvious hand-made fix, running
key centring plus the delta rule? One persistent vector m (`--persist-v 1`), written in the space:
    m' = m + (1 − ρ)(k − m),   k̃ = k − m',   S' = S + β (v − S k) k̃ᵀ / (δ + k̃ᵀ k)
    python verify/probe_centering.py
"""
import itertools
import json
import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).parent.parent
EXE = ROOT / "target/release/autoplast"
TMP = pathlib.Path(tempfile.mkdtemp())


def ins(op, out, a=0, b=0, c=0.0):
    return {"op": op, "out": out, "a": a, "b": b, "c": c}


def centred(rho, beta, delta):
    p = [ins("Const", 0, c=1.0 - rho), ins("VecSub", 3, 0, 2), ins("VecScale", 3, 0, 3), ins("VecAdd", 2, 2, 3),
         ins("VecSub", 3, 0, 2), ins("MatVec", 4, 0, 0), ins("VecSub", 4, 1, 4), ins("Dot", 1, 3, 0),
         ins("Const", 2, c=delta), ins("SAdd", 1, 1, 2), ins("Recip", 1, 1), ins("Const", 3, c=beta),
         ins("SMul", 1, 1, 3), ins("VecScale", 4, 1, 4), ins("Outer", 1, 4, 3), ins("MatAdd", 0, 0, 1)]
    return {"persist_m": 1, "persist_v": 1, "persist_identity": 0, "instrs": p}


def ev(prog, regime):
    f = TMP / "p.json"
    f.write_text(json.dumps(prog))
    out = subprocess.run([str(EXE), "eval", "--prog", str(f), "--regime", regime, "--recip"], capture_output=True, text=True).stdout
    g = lambda k: float(re.search(re.escape(k) + r": acc ([0-9.]+)", out).group(1))
    return float(re.search(r"train acc ([0-9.]+)", out).group(1)), g(f"test regime {regime}"), g("test d16 T128 K8 ow0.3")


if __name__ == "__main__":
    for regime in ["clustered8", "collision3", "clustered"]:
        best = max(((ev(centred(r, b, d), regime), (r, b, d)) for r, b, d in itertools.product([0.5, 0.8, 0.9, 0.95, 0.99, 1.0], [0.5, 1.0], [0.01, 0.1])),
                   key=lambda x: x[0][0])
        print(f"{regime}: centred delta rule, best on train (ρ, β, δ) = {best[1]}: train {best[0][0]:.3f}, test {best[0][1]:.3f}, T128 K8 {best[0][2]:.3f}", flush=True)

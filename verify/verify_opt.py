"""Independent re-check of testbed 2 (README, "Testbed 2: optimizer update rules") in numpy,
float64: re-implements the register machine and the episode loop, reads the exact Rust data
(`autoplast dump --task opt --split test --suite N`), and prints the mean objective and the
fraction of diverged episodes per program. Nothing is shared with the Rust code except the
dump, so the numbers must match `autoplast evalmany --task opt` to rounding.

    python verify/verify_opt.py --task-json suite.json rule.json [more.json ...]
"""
import json
import sys

import numpy as np

NM, NV, NS = 4, 6, 4
NORM_EPS = float(sys.argv[sys.argv.index("--norm-eps") + 1]) if "--norm-eps" in sys.argv else 1e-6
FT = np.float32 if "--f32" in sys.argv else np.float64


def step(instrs, m, vec):
    s = [FT(0.0)] * NS
    for ins in instrs:
        op, o, a, b, c = ins["op"], ins["out"], ins["a"], ins["b"], ins["c"]
        if op == "Outer":
            m[o] = np.outer(vec[a], vec[b])
        elif op == "MatAdd":
            m[o] = m[a] + m[b]
        elif op == "MatSub":
            m[o] = m[a] - m[b]
        elif op == "MatScale":
            m[o] = s[a] * m[b]
        elif op == "Transpose":
            m[o] = m[a].T.copy()
        elif op == "MatMul":
            m[o] = m[a] @ m[b]
        elif op == "MatVec":
            vec[o] = m[a] @ vec[b]
        elif op == "VecAdd":
            vec[o] = vec[a] + vec[b]
        elif op == "VecSub":
            vec[o] = vec[a] - vec[b]
        elif op == "VecScale":
            vec[o] = s[a] * vec[b]
        elif op == "Hadamard":
            vec[o] = vec[a] * vec[b]
        elif op == "Normalize":
            vec[o] = vec[a] / (np.linalg.norm(vec[a]) + NORM_EPS)
        elif op == "Tanh":
            vec[o] = np.tanh(vec[a])
        elif op == "Dot":
            s[o] = FT(vec[a] @ vec[b])
        elif op == "Const":
            s[o] = FT(c)
        elif op == "SAdd":
            s[o] = s[a] + s[b]
        elif op == "SMul":
            s[o] = s[a] * s[b]
        elif op == "Sigmoid":
            s[o] = FT(1.0 / (1.0 + np.exp(-s[a])))
        elif op == "Norm":
            s[o] = FT(np.linalg.norm(vec[a]))
        elif op == "Recip":
            s[o] = s[a] / (s[a] * s[a] + FT(1e-6))
        elif op == "VecRecip":
            vec[o] = vec[a] / (vec[a] * vec[a] + FT(1e-6))
        elif op == "VecSqrt":
            vec[o] = np.sqrt(np.abs(vec[a]))
        else:
            raise ValueError(op)


def episode_objective(prog, ep, d, T):
    instrs, pm, pv = prog["instrs"], prog.get("persist_m", 1), prog.get("persist_v", 0)
    w = np.array(ep["w0"], dtype=FT)
    wstar = np.array(ep["wstar"], dtype=FT)
    scale = FT(ep["scale"])
    if ep["kind"] == "quad":
        A = np.array(ep["a"], dtype=FT).reshape(d, d)
        noise = np.array(ep["noise"], dtype=FT).reshape(T, d)
        loss = lambda w: 0.5 * float((w - wstar) @ A.astype(np.float64) @ (w - wstar))
        grad = lambda w, t: scale * (A @ (w - wstar) + noise[t])
    else:
        X = np.array(ep["x"], dtype=FT).reshape(-1, d)
        y = np.array(ep["y"], dtype=FT)
        B = np.array(ep["batch"]).reshape(T, -1)
        loss = lambda w: float(np.sum((X.astype(np.float64) @ w - y) ** 2) / (2 * len(y)))
        grad = lambda w, t: scale * (X[B[t]].T @ (X[B[t]] @ w - y[B[t]])) / FT(B.shape[1])
    f0 = loss(w)
    m = [np.zeros((d, d), dtype=FT) for _ in range(NM)]
    vec = [np.zeros(d, dtype=FT) for _ in range(NV)]
    for t in range(T):
        g = grad(w, t)
        for i in range(pm, NM):
            m[i] = np.zeros((d, d), dtype=FT)
        vec[0], vec[1] = w.copy(), g
        for i in range(2 + pv, NV):
            vec[i] = np.zeros(d, dtype=FT)
        with np.errstate(all="ignore"):
            step(instrs, m, vec)
        w = vec[0].astype(FT)
        if not (np.all(np.isfinite(w)) and np.all(np.abs(w) < 1e4)):
            return 3.0, True
    return float(np.clip(np.log10(loss(w) / f0), -10.0, 3.0)), False


if __name__ == "__main__":
    task = json.load(open(sys.argv[sys.argv.index("--task-json") + 1]))
    d, T = task["d"], task["t"]
    for path in [a for a in sys.argv[1:] if a.endswith(".json") and a != sys.argv[sys.argv.index("--task-json") + 1]]:
        prog = json.load(open(path))
        res = [episode_objective(prog, ep, d, T) for ep in task["episodes"]]
        obj = sum(r[0] for r in res) / len(res)
        div = sum(r[1] for r in res) / len(res)
        print(f"{path}: objective {obj:.6f} diverged {div:.6f}")

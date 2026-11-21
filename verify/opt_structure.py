"""Structural test of testbed 2 (README, "Testbed 2: optimizer update rules"). A rule is run on
the episodes of a dump; each member of the ladder (SGD, momentum, RMSProp, Adam), with its
constants fitted to the rule's own per-step updates Δw on the same gradient sequences, is scored by
R² over all steps and coordinates. The rule is assigned to the simplest member with R² ≥ 0.95,
otherwise "unclassified". Accuracy levels alone are not rediscovery.

The step size η enters linearly and is fitted by least squares; β, β₁, β₂ by grid. Ladder forms
(as in verify/probe_opt.py, VecRecip semantics x / (x² + 1e-6)):
    SGD       Δw = −η g
    momentum  m = β m + g;                         Δw = −η m
    RMSProp   v = β₂ v + (1 − β₂) g²;              Δw = −η g ⊙ r(√v)
    Adam      m = β₁ m + (1 − β₁) g;  v as above;  Δw = −η m ⊙ r(√v)

    python verify/opt_structure.py --task-json train.json rule.json [more.json ...]
"""
import json
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import verify_opt as V  # noqa: E402

BETAS = [0.0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
BETA2 = [0.5, 0.7, 0.9, 0.95, 0.99, 0.999]
r = lambda x: x / (x * x + 1e-6)


def trajectories(prog, task, n_ep=64):
    """Per episode: gradients (T×d) and updates Δw (T×d) of the rule, up to divergence."""
    d, T = task["d"], task["t"]
    out = []
    for ep in task["episodes"][:n_ep]:
        instrs, pm, pv = prog["instrs"], prog.get("persist_m", 1), prog.get("persist_v", 0)
        w = np.array(ep["w0"])
        wstar = np.array(ep["wstar"])
        if ep["kind"] == "quad":
            A = np.array(ep["a"]).reshape(d, d)
            noise = np.array(ep["noise"]).reshape(T, d)
            grad = lambda w, t: ep["scale"] * (A @ (w - wstar) + noise[t])
        else:
            X = np.array(ep["x"]).reshape(-1, d)
            y = np.array(ep["y"])
            B = np.array(ep["batch"]).reshape(T, -1)
            grad = lambda w, t: ep["scale"] * (X[B[t]].T @ (X[B[t]] @ w - y[B[t]])) / B.shape[1]
        m = [np.zeros((d, d)) for _ in range(V.NM)]
        vec = [np.zeros(d) for _ in range(V.NV)]
        G, D = [], []
        for t in range(T):
            g = grad(w, t)
            for i in range(pm, V.NM):
                m[i] = np.zeros((d, d))
            vec[0], vec[1] = w.copy(), g
            for i in range(2 + pv, V.NV):
                vec[i] = np.zeros(d)
            with np.errstate(all="ignore"):
                V.step(instrs, m, vec)
            w2 = vec[0].copy()
            if not (np.all(np.isfinite(w2)) and np.all(np.abs(w2) < 1e4)):
                break
            G.append(g)
            D.append(w2 - w)
            w = w2
        if G:
            out.append((np.array(G), np.array(D)))
    return out


def directions(kind, G, b1, b2):
    T, d = G.shape
    m, v, out = np.zeros(d), np.zeros(d), np.zeros((T, d))
    for t in range(T):
        g = G[t]
        if kind == "SGD":
            out[t] = g
        elif kind == "momentum":
            m = b1 * m + g
            out[t] = m
        elif kind == "RMSProp":
            v = b2 * v + (1 - b2) * g * g
            out[t] = g * r(np.sqrt(v))
        else:
            m = b1 * m + (1 - b1) * g
            v = b2 * v + (1 - b2) * g * g
            out[t] = m * r(np.sqrt(v))
    return out


def fit(kind, trajs):
    best = (-np.inf, None)
    grid1 = BETAS if kind in ("momentum", "Adam") else [0.0]
    grid2 = BETA2 if kind in ("RMSProp", "Adam") else [0.0]
    D = np.concatenate([dw for _, dw in trajs]).ravel()
    sst = float(np.sum((D - D.mean()) ** 2)) or 1.0
    for b1 in grid1:
        for b2 in grid2:
            X = np.concatenate([directions(kind, G, b1, b2) for G, _ in trajs]).ravel()
            eta = -float(X @ D) / max(float(X @ X), 1e-30)
            r2 = 1.0 - float(np.sum((D + eta * X) ** 2)) / sst
            if r2 > best[0]:
                best = (r2, (eta, b1, b2))
    return best


def classify(prog, task):
    trajs = trajectories(prog, task)
    if not trajs:
        return "diverged", {}
    scores = {k: fit(k, trajs) for k in ("SGD", "momentum", "RMSProp", "Adam")}
    for k in ("SGD", "momentum", "RMSProp", "Adam"):
        if scores[k][0] >= 0.95:
            return k, scores
    return "unclassified", scores


if __name__ == "__main__":
    tj = sys.argv[sys.argv.index("--task-json") + 1]
    task = json.load(open(tj))
    for path in [a for a in sys.argv[1:] if a.endswith(".json") and a != tj]:
        cls, sc = classify(json.load(open(path)), task)
        detail = "  ".join(f"{k} R²={v[0]:.3f} (η={v[1][0]:.3g}, β={v[1][1]:g}, β₂={v[1][2]:g})" for k, v in sc.items())
        print(f"{path}: {cls}   {detail}")

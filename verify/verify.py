"""Independent re-check of a discovered rule in JAX.

Nothing here is shared with the Rust search: the interpreter is re-implemented, episodes and
embeddings come from a different RNG. If the Rust result is real, accuracy here should match
it within sampling noise.

It also decomposes the rule's update into interpretable terms by least squares:
    S' ≈ a·S + b·(v kᵀ) + c·((S k) kᵀ)
Linear attention is (a, b, c) = (1, 1, 0); the delta rule with step β is (1, β, -β).
R² says how much of the rule's behaviour these three terms explain.

usage: python verify/verify.py runs/seed1/best.json [more.json ...]
       python verify/verify.py --task-json task.json runs/seed1/best.json ...
         (exact Rust data from `autoplast dump`; same episodes, so JAX must match Rust to rounding)
"""

import json
import sys

import jax
import jax.numpy as jnp
import numpy as np

NM, NV, NS = 4, 6, 4


def build_step(instrs, read=False):
    """Return step(S, k, v) -> S' for a write program, or, with read=True, read(S, q) -> o for
    an evolved readout program (M0 = S, V0 = q, V1 = S q on entry, output V1)."""

    def step(S, k, v):
        d = S.shape[0]
        m = [S] + [jnp.zeros((d, d)) for _ in range(NM - 1)]
        vec = [k, v] + [jnp.zeros(d) for _ in range(NV - 2)]
        s = [jnp.float32(0.0)] * NS
        for ins in instrs:
            op, o, a, b, c = ins["op"], ins["out"], ins["a"], ins["b"], ins["c"]
            if op == "Outer":
                m[o] = jnp.outer(vec[a], vec[b])
            elif op == "MatAdd":
                m[o] = m[a] + m[b]
            elif op == "MatSub":
                m[o] = m[a] - m[b]
            elif op == "MatScale":
                m[o] = s[a] * m[b]
            elif op == "Transpose":
                m[o] = m[a].T
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
                vec[o] = vec[a] / (jnp.linalg.norm(vec[a]) + 1e-6)
            elif op == "Tanh":
                vec[o] = jnp.tanh(vec[a])
            elif op == "Dot":
                s[o] = vec[a] @ vec[b]
            elif op == "Const":
                s[o] = jnp.float32(c)
            elif op == "SAdd":
                s[o] = s[a] + s[b]
            elif op == "SMul":
                s[o] = s[a] * s[b]
            elif op == "Sigmoid":
                s[o] = jax.nn.sigmoid(s[a])
            elif op == "Norm":
                s[o] = jnp.linalg.norm(vec[a])
            # optional extras (--extra-ops in the Rust search)
            elif op == "VecAbs":
                vec[o] = jnp.abs(vec[a])
            elif op == "VecRelu":
                vec[o] = jnp.maximum(vec[a], 0.0)
            elif op == "VecMax":
                vec[o] = jnp.maximum(vec[a], vec[b])
            elif op == "VecSigmoid":
                vec[o] = jax.nn.sigmoid(vec[a])
            elif op == "MatHadamard":
                m[o] = m[a] * m[b]
            elif op == "MatTanh":
                m[o] = jnp.tanh(m[a])
            elif op == "RowSum":
                vec[o] = m[a].sum(axis=1)
            elif op == "VecSum":
                s[o] = vec[a].sum()
            elif op == "SSub":
                s[o] = s[a] - s[b]
            elif op == "SAbs":
                s[o] = jnp.abs(s[a])
            else:
                raise ValueError(op)
        return vec[1] if read else m[0]

    if read:
        return lambda S, q: step(S, q, S @ q)
    return step


def make_task(rng, d, n_keys, n_vals, T, p_ow, n_ep, max_keys=None, clusters=None, cluster_cos=None):
    def unit(n):
        x = rng.standard_normal((n, d)).astype(np.float32)
        return x / np.linalg.norm(x, axis=1, keepdims=True)

    if clusters:
        # stage-2 collision regime: key i = normalize(sqrt(c)*centre[i % C] + sqrt(1-c)*u_i)
        centres, noise = unit(clusters), unit(n_keys)
        keys = np.sqrt(cluster_cos) * centres[np.arange(n_keys) % clusters] + np.sqrt(1 - cluster_cos) * noise
        keys = (keys / np.linalg.norm(keys, axis=1, keepdims=True)).astype(np.float32)
    else:
        keys = unit(n_keys)
    vals = unit(n_vals)
    W = np.zeros((n_ep, T, 2), dtype=np.int32)
    Q = np.zeros((n_ep, T, 2), dtype=np.int32)  # padded queries
    Qmask = np.zeros((n_ep, T), dtype=bool)
    for e in range(n_ep):
        used, latest = [], {}
        for t in range(T):
            if t > 0 and (rng.random() < p_ow or (max_keys is not None and len(used) >= max_keys)):
                kid = used[rng.integers(len(used))]
            else:
                kid = rng.choice([x for x in range(n_keys) if x not in used])
                used.append(kid)
            vid = rng.integers(n_vals)
            W[e, t] = (kid, vid)
            latest[kid] = vid
        for i, kid in enumerate(used):
            Q[e, i] = (kid, latest[kid])
            Qmask[e, i] = True
    return jnp.array(keys), jnp.array(vals), jnp.array(W), jnp.array(Q), jnp.array(Qmask)


def accuracy(step, task, read=None):
    acc, div, _, _ = accuracy_counts(step, task, read)
    return acc, div


def accuracy_counts(step, task, read=None):
    """Like accuracy, but also returns (correct, total). task may carry a 6th element QV
    (n_ep, T, d) with explicit query vectors (Rust qvecs); otherwise queries are the keys."""
    keys, vals, W, Q, Qmask = task[:5]
    QV = task[5] if len(task) > 5 else None
    d = keys.shape[1]

    def episode(w, q, qm, qv):
        def body(carry, kv):
            S, mx = carry
            S = step(S, keys[kv[0]], vals[kv[1]])
            bad = jnp.where(jnp.all(jnp.isfinite(S)), jnp.max(jnp.abs(S)), jnp.inf)
            return (S, jnp.maximum(mx, bad)), None

        (S, mx), _ = jax.lax.scan(body, (jnp.zeros((d, d)), jnp.float32(0.0)), w)
        qk = keys[q[:, 0]] if qv is None else qv
        o = (S @ qk.T).T if read is None else jax.vmap(lambda x: read(S, x))(qk)  # (T, d)
        scores = o @ vals.T
        pred = jnp.argmax(scores, axis=1)
        ok = (pred == q[:, 1]) & (jnp.linalg.norm(o, axis=1) > 1e-6) & jnp.all(jnp.isfinite(o), axis=1)
        return jnp.sum(ok & qm), jnp.sum(qm), mx

    if QV is None:
        c, n, mx = jax.jit(jax.vmap(lambda w, q, qm: episode(w, q, qm, None)))(W, Q, Qmask)
    else:
        c, n, mx = jax.jit(jax.vmap(episode))(W, Q, Qmask, QV)
    # diverged: some episode exceeds the Rust guard (|S| > 1e4 or non-finite), where Rust
    # scores the whole suite 0. Accuracy here is computed without that guard.
    return float(c.sum() / n.sum()), bool(jnp.any(mx > 1e4)), int(c.sum()), int(n.sum())


def load_task_json(path):
    """Read an `autoplast dump` JSON (exact Rust embeddings and episodes). Episodes are grouped
    by write length so that no padding enters S; returns a list of task tuples."""
    j = json.load(open(path))
    d = j["d"]
    keys = np.array(j["keys"], dtype=np.float32).reshape(-1, d)
    vals = np.array(j["vals"], dtype=np.float32).reshape(-1, d)
    groups = {}
    for e in j["episodes"]:
        groups.setdefault(len(e["w"]), []).append(e)
    tasks = []
    for T, eps in sorted(groups.items()):
        nq = max(len(e["q"]) for e in eps)
        W = np.array([e["w"] for e in eps], dtype=np.int32)
        Q = np.zeros((len(eps), nq, 2), dtype=np.int32)
        Qm = np.zeros((len(eps), nq), dtype=bool)
        has_qv = any(len(e["qv"]) for e in eps)
        QV = np.zeros((len(eps), nq, d), dtype=np.float32)
        for i, e in enumerate(eps):
            Q[i, : len(e["q"])] = e["q"]
            Qm[i, : len(e["q"])] = True
            if has_qv:
                QV[i, : len(e["q"])] = np.array(e["qv"], dtype=np.float32).reshape(-1, d)
        t = (jnp.array(keys), jnp.array(vals), jnp.array(W), jnp.array(Q), jnp.array(Qm))
        tasks.append(t + ((jnp.array(QV),) if has_qv else ()))
    return tasks


def report_json(name, instrs, tasks, read_instrs=None):
    step = build_step(instrs)
    read = build_step(read_instrs, read=True) if read_instrs is not None else None
    c = n = 0
    div = False
    for t in tasks:
        _, dv, ci, ni = accuracy_counts(step, t, read)
        c, n, div = c + ci, n + ni, div or dv
    print(f"{name}: acc {c / n:.4f} ({c}/{n})" + ("  [diverged: Rust guard would score 0]" if div else ""))
    return c / n, div


def decompose(step, d=16, n=4000, seed=0):
    rng = np.random.default_rng(seed)
    S = rng.standard_normal((n, d, d)).astype(np.float32) * 0.3
    k = rng.standard_normal((n, d)).astype(np.float32)
    k /= np.linalg.norm(k, axis=1, keepdims=True)
    v = rng.standard_normal((n, d)).astype(np.float32)
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    Sn = np.asarray(jax.jit(jax.vmap(step))(jnp.array(S), jnp.array(k), jnp.array(v)))
    Sk = np.einsum("nij,nj->ni", S, k)
    X = np.stack(
        [S.reshape(n, -1), np.einsum("ni,nj->nij", v, k).reshape(n, -1), np.einsum("ni,nj->nij", Sk, k).reshape(n, -1)],
        axis=-1,
    ).reshape(-1, 3)
    y = Sn.reshape(-1)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    r2 = 1 - np.sum((y - X @ coef) ** 2) / np.sum((y - y.mean()) ** 2)
    return coef, r2


SUITES = [
    ("test d16 T12 ow0.3", dict(d=16, n_keys=64, n_vals=64, T=12, p_ow=0.3, n_ep=512)),
    ("test d16 T12 ow0.0", dict(d=16, n_keys=64, n_vals=64, T=12, p_ow=0.0, n_ep=512)),
    ("test d16 T12 ow0.6", dict(d=16, n_keys=64, n_vals=64, T=12, p_ow=0.6, n_ep=512)),
    ("test d32 T24 ow0.3", dict(d=32, n_keys=128, n_vals=128, T=24, p_ow=0.3, n_ep=256)),
    ("test d16 T64 K8 ow0.3", dict(d=16, n_keys=64, n_vals=64, T=64, p_ow=0.3, n_ep=256, max_keys=8)),
    ("test d16 T128 K8 ow0.3", dict(d=16, n_keys=64, n_vals=64, T=128, p_ow=0.3, n_ep=128, max_keys=8)),
    # stage-2 collision keys (8 centres, within-cluster cosine 0.85), as in --regime collision3
    ("test collision d16 T12 ow0.3", dict(d=16, n_keys=64, n_vals=64, T=12, p_ow=0.3, n_ep=512, clusters=8, cluster_cos=0.85)),
    ("test collision d16 T64 K8 ow0.3", dict(d=16, n_keys=64, n_vals=64, T=64, p_ow=0.3, n_ep=256, max_keys=8, clusters=8, cluster_cos=0.85)),
]

REFERENCES = {
    "linear attention": [
        {"op": "Outer", "out": 1, "a": 1, "b": 0, "c": 0},
        {"op": "MatAdd", "out": 0, "a": 0, "b": 1, "c": 0},
    ],
    "delta rule (beta=0.5)": [
        {"op": "MatVec", "out": 2, "a": 0, "b": 0, "c": 0},
        {"op": "VecSub", "out": 3, "a": 1, "b": 2, "c": 0},
        {"op": "Outer", "out": 1, "a": 3, "b": 0, "c": 0},
        {"op": "Const", "out": 0, "a": 0, "b": 0, "c": 0.5},
        {"op": "MatScale", "out": 1, "a": 0, "b": 1, "c": 0},
        {"op": "MatAdd", "out": 0, "a": 0, "b": 1, "c": 0},
    ],
}


def report(name, instrs, rng_seed=12345, read_instrs=None):
    step = build_step(instrs)
    read = build_step(read_instrs, read=True) if read_instrs is not None else None
    rng = np.random.default_rng(rng_seed)
    accs = {sname: accuracy(step, make_task(rng, **cfg), read) for sname, cfg in SUITES}
    coef, r2 = decompose(step)
    print(f"\n## {name}")
    for sname, (a, div) in accs.items():
        print(f"  {sname}: acc {a:.3f}" + ("  [diverged: Rust guard would score 0]" if div else ""))
    print(f"  S' ≈ {coef[0]:+.3f}·S {coef[1]:+.3f}·(v kᵀ) {coef[2]:+.3f}·((S k) kᵀ)   R² = {r2:.4f}")


if __name__ == "__main__":
    if "--task-json" in sys.argv:
        # exact Rust data: python verify/verify.py --task-json task.json prog.json ...
        i = sys.argv.index("--task-json")
        tasks = load_task_json(sys.argv[i + 1])
        paths = sys.argv[1:i] + sys.argv[i + 2 :]
        for name, instrs in REFERENCES.items():
            report_json(f"reference: {name}", instrs, tasks)
        for path in paths:
            prog = json.load(open(path))
            report_json(path, prog["instrs"], tasks, read_instrs=prog.get("read"))
        sys.exit(0)
    for name, instrs in REFERENCES.items():
        report(f"reference: {name}", instrs)
    for path in sys.argv[1:]:
        prog = json.load(open(path))
        report(path, prog["instrs"], read_instrs=prog.get("read"))

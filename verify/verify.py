"""Independent re-check of a discovered rule in JAX.

Nothing here is shared with the Rust search: the interpreter is re-implemented, episodes and
embeddings come from a different RNG. If the Rust result is real, accuracy here should match
it within sampling noise; every accuracy is printed with its 95% binomial interval.

It also repeats the structural test of src/classify.rs on memory states taken from real
episodes (not random matrices): least squares of the update on four terms,
    S' ≈ a·S + b·(v kᵀ) + c·((S k) kᵀ) + g·((vᵀS k)·v kᵀ)
with R² over the part of the update that is not the carry a·S. Linear attention is
(1, b, 0, 0); the delta rule with step e is (1, w, -e, 0); the Kronecker delta rule has g < 0.

usage: python verify/verify.py runs/seed1/best.json [more.json ...]
"""

import json
import sys

import jax
import jax.numpy as jnp
import numpy as np

NM, NV, NS = 4, 6, 4


def build_step(instrs, pm=1, pv=0):
    """step(state, k, v) -> state. state = (persistent matrices [S, ...], persistent vectors)."""

    def step(state, k, v):
        mats, vecs = state
        d = k.shape[0]
        m = list(mats) + [jnp.zeros((d, d)) for _ in range(NM - pm)]
        vec = [k, v] + list(vecs) + [jnp.zeros(d) for _ in range(NV - 2 - pv)]
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
            elif op == "Recip":
                s[o] = s[a] / (s[a] * s[a] + 1e-6)
            else:
                raise ValueError(op)
        return (tuple(m[:pm]), tuple(vec[2 : 2 + pv]))

    def init(d):
        return (tuple(jnp.zeros((d, d)) for _ in range(pm)), tuple(jnp.zeros(d) for _ in range(pv)))

    return step, init


def make_task(rng, d, n_keys, n_vals, T, p_ow, n_ep, pool=0, cluster=0.0):
    def unit(x):
        return (x / np.linalg.norm(x, axis=-1, keepdims=True)).astype(np.float32)

    keys = unit(rng.standard_normal((n_keys, d)))
    if cluster > 0:
        keys = unit(unit(rng.standard_normal(d)) + cluster * keys)
    vals = unit(rng.standard_normal((n_vals, d)))
    W = np.zeros((n_ep, T, 2), dtype=np.int32)
    Q = np.zeros((n_ep, T, 2), dtype=np.int32)  # padded queries
    Qmask = np.zeros((n_ep, T), dtype=bool)
    for e in range(n_ep):
        used, latest = [], {}
        for t in range(T):
            full = pool > 0 and len(used) >= pool
            if t > 0 and (full or rng.random() < p_ow):
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


def accuracy(rule, task):
    """Returns (accuracy, number of queries)."""
    step, init = rule
    keys, vals, W, Q, Qmask = task
    d = keys.shape[1]

    def episode(w, q, qm):
        def body(state, kv):
            return step(state, keys[kv[0]], vals[kv[1]]), None

        state, _ = jax.lax.scan(body, init(d), w)
        S = state[0][0]
        o = (S @ keys[q[:, 0]].T).T  # (T, d)
        pred = jnp.argmax(o @ vals.T, axis=1)
        norm = jnp.linalg.norm(o, axis=1)
        ok = (pred == q[:, 1]) & (norm > 1e-6) & jnp.isfinite(norm)
        return jnp.sum(ok & qm), jnp.sum(qm)

    c, n = jax.jit(jax.vmap(episode))(W, Q, Qmask)
    return float(c.sum() / n.sum()), int(n.sum())


def decompose(rule, rng, n_ep=32, **cfg):
    """Structural fit on states the rule itself produces on real episodes."""
    step, init = rule
    keys, vals, W, _, _ = make_task(rng, n_ep=n_ep, **cfg)
    d = keys.shape[1]

    def episode(w):
        def body(state, kv):
            new = step(state, keys[kv[0]], vals[kv[1]])
            return new, (state[0][0], new[0][0])

        _, (before, after) = jax.lax.scan(body, init(d), w)
        return before, after

    S, Sn = (np.asarray(x, dtype=np.float64).reshape(-1, d, d) for x in jax.jit(jax.vmap(episode))(W))
    k = np.asarray(keys)[np.asarray(W)[..., 0]].reshape(-1, d).astype(np.float64)
    v = np.asarray(vals)[np.asarray(W)[..., 1]].reshape(-1, d).astype(np.float64)
    ok = np.isfinite(Sn).all(axis=(1, 2))
    S, Sn, k, v = S[ok], Sn[ok], k[ok], v[ok]
    Sk = np.einsum("nij,nj->ni", S, k)
    vk = np.einsum("ni,nj->nij", v, k)
    terms = [S, vk, np.einsum("ni,nj->nij", Sk, k), np.einsum("n,nij->nij", np.einsum("ni,ni->n", v, Sk), vk)]
    X = np.stack([t.reshape(-1) for t in terms], axis=-1)
    y = Sn.reshape(-1)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    carry = np.sum((y - coef[0] * X[:, 0]) ** 2)
    r2 = 1.0 if carry < 1e-9 * max(np.sum(y**2), 1e-30) else 1 - np.sum((y - X @ coef) ** 2) / carry
    return coef, r2


BASE = dict(d=16, n_keys=64, n_vals=64, T=12, p_ow=0.3)
SUITES = [
    ("test d16 T12 ow0.3", dict(BASE, n_ep=512)),
    ("test d16 T12 ow0.0", dict(BASE, p_ow=0.0, n_ep=512)),
    ("test d16 T12 ow0.6", dict(BASE, p_ow=0.6, n_ep=512)),
    ("test d32 T24 ow0.3", dict(d=32, n_keys=128, n_vals=128, T=24, p_ow=0.3, n_ep=256)),
    ("test d8 T6 ow0.3", dict(d=8, n_keys=32, n_vals=32, T=6, p_ow=0.3, n_ep=512)),
    ("full T24", dict(BASE, T=24, n_ep=256)),
    ("overload T48", dict(BASE, T=48, n_ep=256)),
    ("rewrite8 T96", dict(BASE, T=96, pool=8, n_ep=256)),
    ("rewrite14 T96", dict(BASE, T=96, pool=14, n_ep=256)),
    ("clustered T12", dict(BASE, cluster=0.5, n_ep=512)),
    ("clustered8 T48", dict(BASE, T=48, pool=8, cluster=0.5, n_ep=256)),
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


def report(name, prog, rng_seed=12345):
    rule = build_step(prog["instrs"], prog.get("persist_m", 1), prog.get("persist_v", 0))
    rng = np.random.default_rng(rng_seed)
    print(f"\n## {name}")
    for sname, cfg in SUITES:
        a, n = accuracy(rule, make_task(rng, **cfg))
        print(f"  {sname}: acc {a:.3f} ±{1.96 * (a * (1 - a) / n) ** 0.5:.3f}")
    coef, r2 = decompose(rule, rng, **BASE)
    print(
        f"  on real states: S' ≈ {coef[0]:+.3f}·S {coef[1]:+.3f}·(v kᵀ) {coef[2]:+.3f}·((S k) kᵀ) "
        f"{coef[3]:+.3f}·((vᵀS k) v kᵀ)   R² = {r2:.4f}"
    )


if __name__ == "__main__":
    for name, instrs in REFERENCES.items():
        report(f"reference: {name}", {"instrs": instrs})
    for path in sys.argv[1:]:
        report(path, json.load(open(path)))

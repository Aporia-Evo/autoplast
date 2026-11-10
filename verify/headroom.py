"""Headroom probe (review only, NOT part of the search): how far is tuned Gated DeltaNet from
what a linear readout o = S q can reach at all, per regime?

Families are tuned on 200 train episodes and reported on 1000 fresh episodes with fresh
embeddings. Reference points: batch ridge on the latest (key, value) pairs (ceiling for a linear
readout), online RLS, and a delta error with a Kalman gain (both keep a second d x d state P).
'selfprec' is a hand-written probe that stays inside autoplast's op set and state budget:
    S' = a*S + b*(v - S k)(k - c*S^T S k)^T
It is only there to answer "is there anything above Gated DeltaNet in the space".
"""
import itertools
import sys

import numpy as np


def unit(x):
    return x / np.linalg.norm(x, axis=-1, keepdims=True)


def make(rng, d, n_keys, n_vals, T, p_ow, E, cluster=0.0, pool=None):
    if cluster > 0:
        c = unit(rng.standard_normal(d))
        keys = unit(c + cluster * unit(rng.standard_normal((n_keys, d))))
    else:
        keys = unit(rng.standard_normal((n_keys, d)))
    vals = unit(rng.standard_normal((n_vals, d)))
    K = np.zeros((E, T), int)
    V = rng.integers(n_vals, size=(E, T))
    for e in range(E):
        used = []
        for t in range(T):
            full = pool is not None and len(used) >= pool
            if t > 0 and (full or rng.random() < p_ow):
                k = used[rng.integers(len(used))]
            else:
                k = rng.choice([x for x in range(n_keys) if x not in used])
                used.append(k)
            K[e, t] = k
    last = np.zeros((E, T), bool)
    for e in range(E):
        seen = set()
        for t in range(T - 1, -1, -1):
            if K[e, t] not in seen:
                seen.add(K[e, t])
                last[e, t] = True
    return dict(keys=keys, vals=vals, K=K, V=V, last=last, d=d)


def readout_acc(S, task, rng=None, qnoise=0.0):
    keys, vals, K, V, last = (task[x] for x in ("keys", "vals", "K", "V", "last"))
    q = keys[K]  # E,T,d
    if qnoise > 0:
        q = unit(q + qnoise * unit(rng.standard_normal(q.shape)))
    o = np.einsum("eij,etj->eti", S, q)
    sc = o @ vals.T
    ok = (sc.argmax(-1) == V) & (np.linalg.norm(o, axis=-1) > 1e-6)
    return (ok & last).sum() / last.sum()


def run_rule(step, task):
    E, T = task["K"].shape
    d = task["d"]
    S = np.zeros((E, d, d))
    for t in range(T):
        S = step(S, task["keys"][task["K"][:, t]], task["vals"][task["V"][:, t]])
        if not np.isfinite(S).all() or np.abs(S).max() > 1e6:
            return None
    return S


def gdn(a, b):
    def step(S, k, v):
        Sk = np.einsum("eij,ej->ei", S, k)
        return a * (S + b * np.einsum("ei,ej->eij", v - Sk, k))
    return step


def selfprec(a, b, c):
    def step(S, k, v):
        Sk = np.einsum("eij,ej->ei", S, k)
        StSk = np.einsum("eji,ej->ei", S, Sk)
        return a * S + b * np.einsum("ei,ej->eij", v - Sk, k - c * StSk)
    return step


def la(S, k, v):
    return S + np.einsum("ei,ej->eij", v, k)


def rls(lam, task):
    E, T = task["K"].shape
    d = task["d"]
    S = np.zeros((E, d, d))
    P = np.tile(np.eye(d) / lam, (E, 1, 1))
    for t in range(T):
        k = task["keys"][task["K"][:, t]]
        v = task["vals"][task["V"][:, t]]
        Pk = np.einsum("eij,ej->ei", P, k)
        g = Pk / (1 + np.einsum("ei,ei->e", k, Pk))[:, None]
        S = S + np.einsum("ei,ej->eij", v - np.einsum("eij,ej->ei", S, k), g)
        P = P - np.einsum("ei,ej->eij", g, Pk)
    return S


def kalman(lam, q, task):
    E, T = task["K"].shape
    d = task["d"]
    S = np.zeros((E, d, d))
    P = np.tile(np.eye(d) / lam, (E, 1, 1))
    for t in range(T):
        k = task["keys"][task["K"][:, t]]
        v = task["vals"][task["V"][:, t]]
        Pk = np.einsum("eij,ej->ei", P, k)
        g = Pk / (1 + np.einsum("ei,ei->e", k, Pk))[:, None]
        S = S + np.einsum("ei,ej->eij", v - np.einsum("eij,ej->ei", S, k), g)
        P = P - np.einsum("ei,ej->eij", g, Pk) + q * np.eye(d)
    return S


def ridge(lam, task):
    E, T = task["K"].shape
    d = task["d"]
    S = np.zeros((E, d, d))
    for e in range(E):
        m = task["last"][e]
        Km = task["keys"][task["K"][e, m]]
        Vm = task["vals"][task["V"][e, m]]
        S[e] = Vm.T @ np.linalg.solve(Km @ Km.T + lam * np.eye(len(Km)), Km)
    return S


def tune(family, grid, train):
    best = (-1, None)
    for p in grid:
        S = run_rule(family(*p), train)
        if S is None:
            continue
        acc = readout_acc(S, train)
        if acc > best[0]:
            best = (acc, p)
    return best


REGIMES = {
    "base d16 T12 ow0.3": dict(d=16, n_keys=64, n_vals=64, T=12, p_ow=0.3),
    "full load d16 T24 ow0.3": dict(d=16, n_keys=64, n_vals=64, T=24, p_ow=0.3),
    "overload d16 T48 ow0.3": dict(d=16, n_keys=64, n_vals=64, T=48, p_ow=0.3),
    "long, 8 keys rewritten, T96": dict(d=16, n_keys=64, n_vals=64, T=96, p_ow=0.3, pool=8),
    "long, 14 keys rewritten, T96": dict(d=16, n_keys=64, n_vals=64, T=96, p_ow=0.3, pool=14),
    "clustered cos~0.8, T12": dict(d=16, n_keys=64, n_vals=64, T=12, p_ow=0.3, cluster=0.5),
    "clustered cos~0.8, 8 keys, T48": dict(d=16, n_keys=64, n_vals=64, T=48, p_ow=0.3, cluster=0.5, pool=8),
}

A = [0.8, 0.9, 0.95, 0.98, 1.0, 1.02, 1.05, 1.1, 1.15]
B = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
C = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]
LAM = [1e-3, 1e-2, 3e-2, 0.1, 0.3, 1.0]

if __name__ == "__main__":
    only = sys.argv[1:] or list(REGIMES)
    print("| regime | lin.att | DeltaNet | Gated DeltaNet | selfprec probe | RLS (2 states) | Kalman delta (2 states) | ridge ceiling |")
    print("|---|---|---|---|---|---|---|---|")
    for name in only:
        cfg = REGIMES[name]
        train = make(np.random.default_rng(1), E=200, **cfg)
        test = make(np.random.default_rng(2), E=1000, **cfg)
        cells = [f"{readout_acc(run_rule(la, test), test):.3f}"]
        for fam, grid in [
            (gdn, [(1.0, b) for b in B]),
            (gdn, list(itertools.product(A, B))),
            (selfprec, list(itertools.product(A, B, C))),
        ]:
            _, p = tune(fam, grid, train)
            S = run_rule(fam(*p), test)
            acc = readout_acc(S, test) if S is not None else float("nan")
            cells.append(f"{acc:.3f} {p}")
        kgrid = list(itertools.product([1e-3, 1e-2, 0.1, 1.0], [0.0, 0.01, 0.1, 1.0, 10.0, 100.0]))
        cols = [(lambda l, t: rls(l, t), [(l,) for l in LAM]), (lambda l, q, t: kalman(l, q, t), kgrid),
                (lambda l, t: ridge(l, t), [(l,) for l in LAM])]
        for fn, grid in cols:
            p = max(grid, key=lambda p: readout_acc(fn(*p, train), train))
            cells.append(f"{readout_acc(fn(*p, test), test):.3f} {p}")
        print(f"| {name} | " + " | ".join(cells) + " |", flush=True)

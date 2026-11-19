"""Closed-loop growth test (README, "Closed-loop growth test"): grow a program from the empty one
by ranking residual branches with adjoints and verifying the best with the Rust fitness.

    python verify/grow.py --arm A|B [--task-seed 1] [--rounds 20] [--out DIR]

Space of packages D and E: S = M0, persistent M1, M2 starting at I, the 20 ops with Recip,
MAX_LEN 24, collision3 train task. JAX gives the adjoints and polishes constants; every score
that decides anything is the Rust train fitness (`autoplast evalmany`).
"""

import itertools
import json
import os
import pathlib
import subprocess
import sys
import time

import jax
import jax.numpy as jnp
import numpy as np

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "verify"))
import verify as V  # noqa: E402

EXE = str(ROOT / "target/release/autoplast")
NM, NV, NS, PM = 4, 6, 4, 3
MAX_LEN = 24
TAU = 10.0
EPS = [sg * e for e in (0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0) for sg in (1, -1)]
MSIG = {"Outer": "VV", "MatAdd": "MM", "MatSub": "MM", "MatScale": "SM", "Transpose": "M", "MatMul": "MM"}
VSIG = {"MatVec": "MV", "VecAdd": "VV", "VecSub": "VV", "VecScale": "SV", "Hadamard": "VV", "Normalize": "V", "Tanh": "V"}
SSIG = {"Dot": "VV", "SAdd": "SS", "SMul": "SS", "Sigmoid": "S", "Norm": "V", "Recip": "S"}


def arg(name, default):
    return type(default)(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


ARM = arg("--arm", "A")
TASK_SEED = arg("--task-seed", 1)
ROUNDS = arg("--rounds", 20)
BEAM = arg("--beam", 1)
COMPACT = "--compact" in sys.argv
V2 = BEAM > 1 or COMPACT
OUT = pathlib.Path(arg("--out", str(ROOT / ("runs/grow2" if V2 else "runs/grow") / f"arm{ARM}{'2' if V2 else ''}_task{TASK_SEED}")))
N_GRAD = 0  # forward-backward passes: one per adjoint computation, one per polish step
FLAGS = ["--regime", "collision3", "--recip", "--persist-m", "3", "--persist-init", "identity", "--task-seed", str(TASK_SEED)]
N_RUST = 0


def ins(op, out, a=0, b=0, c=0.0):
    return {"op": op, "out": int(out), "a": int(a), "b": int(b), "c": float(c)}


def sig(op):
    for t, d in (("M", MSIG), ("V", VSIG), ("S", SSIG)):
        if op in d:
            return t, d[op]
    if op == "Const":
        return "S", ""
    raise ValueError(op)


# ---------------- Rust scoring ----------------

def rust_fit(progs, split="train"):
    global N_RUST
    f = OUT / "_batch.jsonl"
    f.write_text("\n".join(json.dumps({"persist_m": PM, "persist_v": 0, "persist_identity": 1, "instrs": p}) for p in progs) + "\n")
    out = subprocess.run([EXE, "evalmany", "--in", str(f), "--threads", str(os.cpu_count()), "--split", split] + FLAGS,
                         capture_output=True, text=True, check=True).stdout.split("\n")
    N_RUST += len(progs)
    return [tuple(map(float, l.split())) for l in out if l.strip()]


def rust_report(prog):
    f = OUT / "_one.json"
    f.write_text(json.dumps({"persist_m": PM, "persist_v": 0, "persist_identity": 1, "instrs": prog}))
    return subprocess.run([EXE, "eval", "--prog", str(f)] + FLAGS, capture_output=True, text=True).stdout


# ---------------- liveness (as in src/program.rs) ----------------

def live_sets(prog):
    """Live registers before each position 0..L (L = end), with M0 and the persistent registers
    read by the next step live at the end (fixpoint, as live_persistent)."""
    out_m = {0}
    while True:
        lives = [None] * (len(prog) + 1)
        lm, lv, ls = set(out_m), set(), set()
        lives[len(prog)] = (set(lm), set(lv), set(ls))
        for p in range(len(prog) - 1, -1, -1):
            i = prog[p]
            t, ins_t = sig(i["op"])
            reg = {"M": lm, "V": lv, "S": ls}[t]
            if i["out"] in reg:
                reg.discard(i["out"])
                for slot, it in zip("ab", ins_t):
                    {"M": lm, "V": lv, "S": ls}[it].add(i[slot])
            lives[p] = (set(lm), set(lv), set(ls))
        new = out_m | {r for r in lm if 0 < r < PM}
        if new == out_m:
            return lives, lm  # lm: live at the start of the step (read from the previous step)
        out_m = new


# ---------------- JAX interpreter with hooks at every position ----------------

def exec1(i, m, v, s):
    op, o, a, b, c = i["op"], i["out"], i["a"], i["b"], i["c"]
    if op == "Outer": m[o] = jnp.outer(v[a], v[b])
    elif op == "MatAdd": m[o] = m[a] + m[b]
    elif op == "MatSub": m[o] = m[a] - m[b]
    elif op == "MatScale": m[o] = s[a] * m[b]
    elif op == "Transpose": m[o] = m[a].T
    elif op == "MatMul": m[o] = m[a] @ m[b]
    elif op == "MatVec": v[o] = m[a] @ v[b]
    elif op == "VecAdd": v[o] = v[a] + v[b]
    elif op == "VecSub": v[o] = v[a] - v[b]
    elif op == "VecScale": v[o] = s[a] * v[b]
    elif op == "Hadamard": v[o] = v[a] * v[b]
    elif op == "Normalize": v[o] = v[a] / (jnp.linalg.norm(v[a]) + 1e-6)
    elif op == "Tanh": v[o] = jnp.tanh(v[a])
    elif op == "Dot": s[o] = v[a] @ v[b]
    elif op == "Const": s[o] = c
    elif op == "SAdd": s[o] = s[a] + s[b]
    elif op == "SMul": s[o] = s[a] * s[b]
    elif op == "Sigmoid": s[o] = jax.nn.sigmoid(s[a])
    elif op == "Norm": s[o] = jnp.linalg.norm(v[a])
    elif op == "Recip": s[o] = s[a] / (s[a] * s[a] + 1e-6)
    else: raise ValueError(op)


def make_step(prog, consts=None):
    L = len(prog)

    def step(state, k, v_, hm, hv, hs):
        d = k.shape[0]
        m = [state[0], state[1], state[2], jnp.zeros((d, d))]
        v = [k, v_] + [jnp.zeros(d)] * (NV - 2)
        s = [jnp.float32(0.0)] * NS
        snaps = []
        ci = 0
        for p in range(L + 1):
            m = [m[r] + hm[p, r] for r in range(NM)]
            v = [v[r] + hv[p, r] for r in range(NV)]
            s = [s[r] + hs[p, r] for r in range(NS)]
            snaps.append((jnp.stack(m), jnp.stack(v), jnp.stack(s)))
            if p < L:
                i = prog[p]
                if i["op"] == "Const" and consts is not None:
                    i = dict(i, c=consts[ci])
                if prog[p]["op"] == "Const":
                    ci += 1
                exec1(i, m, v, s)
        return (m[0], m[1], m[2]), tuple(jnp.stack(x) for x in zip(*snaps))

    return step


def group_loss(step, task, H, n_total):
    keys, vals, W, Q, Qm = task[:5]
    d = keys.shape[1]
    init = (jnp.zeros((d, d)), jnp.eye(d), jnp.eye(d))

    def episode(w, hm, hv, hs, q, qm):
        def body(st, x):
            kv, a, b, c = x
            return step(st, keys[kv[0]], vals[kv[1]], a, b, c)

        st, snaps = jax.lax.scan(body, init, (w, hm, hv, hs))
        o = keys[q[:, 0]] @ st[0].T
        o = o / jnp.sqrt(jnp.sum(o * o, axis=1, keepdims=True) + 1e-12)
        ce = -jax.nn.log_softmax(TAU * o @ vals.T)[jnp.arange(q.shape[0]), q[:, 1]]
        return jnp.sum(ce * qm), snaps

    ce, snaps = jax.vmap(episode)(W, *H, Q, Qm)
    return jnp.sum(ce) / n_total, snaps


def adjoints(prog, tasks):
    """Loss, and per group: adjoints at every site and register snapshots at every position."""
    global N_GRAD
    N_GRAD += 1
    L = len(prog)
    n = sum(int(t[4].sum()) for t in tasks)
    step = make_step(prog)
    loss, out = 0.0, []
    for t in tasks:
        E, T = t[2].shape[:2]
        d = t[0].shape[1]
        H = (jnp.zeros((E, T, L + 1, NM, d, d)), jnp.zeros((E, T, L + 1, NV, d)), jnp.zeros((E, T, L + 1, NS)))
        (l, snaps), g = jax.value_and_grad(lambda H: group_loss(step, t, H, n), has_aux=True)(H)
        loss += float(l)
        out.append(([np.asarray(x) for x in g], [np.asarray(x) for x in snaps]))
    return loss, out


def polish(prog, tasks, steps=60, lr=0.05):
    """Adam on all Const values (scaled by their size) for the smooth loss."""
    cidx = [p for p, i in enumerate(prog) if i["op"] == "Const"]
    if not cidx:
        return prog
    c0 = jnp.array([prog[p]["c"] for p in cidx], dtype=jnp.float32)
    scale = jnp.maximum(jnp.abs(c0), 0.01)
    n = sum(int(t[4].sum()) for t in tasks)
    L = len(prog)

    def loss(theta):
        step = make_step(prog, consts=list(c0 + scale * theta))
        tot = 0.0
        for t in tasks:
            E, T = t[2].shape[:2]
            d = t[0].shape[1]
            H = (jnp.zeros((E, T, L + 1, NM, d, d)), jnp.zeros((E, T, L + 1, NV, d)), jnp.zeros((E, T, L + 1, NS)))
            tot = tot + group_loss(step, t, H, n)[0]
        return tot

    global N_GRAD
    N_GRAD += steps
    vg = jax.jit(jax.value_and_grad(loss))
    th, mo, ve = jnp.zeros_like(c0), jnp.zeros_like(c0), jnp.zeros_like(c0)
    for it in range(1, steps + 1):
        _, g = vg(th)
        g = jnp.nan_to_num(g)
        mo = 0.9 * mo + 0.1 * g
        ve = 0.999 * ve + 0.001 * g * g
        th = th - lr * (mo / (1 - 0.9 ** it)) / (jnp.sqrt(ve / (1 - 0.999 ** it)) + 1e-8)
    new = [dict(i) for i in prog]
    for p, c in zip(cidx, np.asarray(c0 + scale * th)):
        new[p]["c"] = float(c)
    return new


# ---------------- candidates, scored by contraction with the adjoint ----------------
# expressions are trees: ("M", r) / ("V", r) / ("S", r) leaves, (op, child, child) nodes

def leaf_vals(snap):
    m, v, s = snap  # (E, T, 4, d, d), (E, T, 6, d), (E, T, 4)
    return m, v, s


def vec_exprs(m, v, s):
    """Vector expressions of depth <= 1 with values: list of (tree, value (E,T,d))."""
    out = [(("V", r), v[:, :, r]) for r in range(NV)]
    for a, b in itertools.product(range(NM), range(NV)):
        out.append((("MatVec", ("M", a), ("V", b)), np.einsum("etij,etj->eti", m[:, :, a], v[:, :, b])))
    for a, b in itertools.combinations(range(NV), 2):
        out.append((("VecAdd", ("V", a), ("V", b)), v[:, :, a] + v[:, :, b]))
        out.append((("Hadamard", ("V", a), ("V", b)), v[:, :, a] * v[:, :, b]))
    for a, b in itertools.permutations(range(NV), 2):
        out.append((("VecSub", ("V", a), ("V", b)), v[:, :, a] - v[:, :, b]))
    for a, b in itertools.product(range(NS), range(NV)):
        out.append((("VecScale", ("S", a), ("V", b)), s[:, :, a, None] * v[:, :, b]))
    for a in range(NV):
        out.append((("Normalize", ("V", a)), v[:, :, a] / (np.linalg.norm(v[:, :, a], axis=-1, keepdims=True) + 1e-6)))
        out.append((("Tanh", ("V", a)), np.tanh(v[:, :, a])))
    return [(t, x) for t, x in out if np.abs(x).max() > 1e-9]


def scal_exprs(v, s):
    out = [(("S", r), s[:, :, r]) for r in range(NS)]
    for a, b in itertools.combinations_with_replacement(range(NV), 2):
        out.append((("Dot", ("V", a), ("V", b)), np.einsum("eti,eti->et", v[:, :, a], v[:, :, b])))
    for a in range(NV):
        out.append((("Norm", ("V", a)), np.linalg.norm(v[:, :, a], axis=-1)))
    for a in range(NS):
        out.append((("Sigmoid", ("S", a)), 1 / (1 + np.exp(-s[:, :, a]))))
        out.append((("Recip", ("S", a)), s[:, :, a] / (s[:, :, a] ** 2 + 1e-6)))
    return [(t, x) for t, x in out if np.abs(x).max() > 1e-9]


def score_matrix_site(G, m, v, s):
    """Slope |<G,e>|/|e| for matrix expressions: outer products with one register factor, and
    register combinations, each optionally scaled per step by a scalar expression."""
    res = []
    ve = vec_exprs(m, v, s)
    regs = [(t, x) for t, x in ve if t[0] == "V"]
    for (ty, y) in ve:
        Gy = np.einsum("etij,etj->eti", G, y)       # for Outer(x, y): <G, x y^T> = x . G y
        Gty = np.einsum("etji,etj->eti", G, y)      # for Outer(y, x): <G, y x^T> = x . G^T y
        ny = np.einsum("eti,eti->et", y, y)
        for (tx, x) in regs:
            nx = np.einsum("eti,eti->et", x, x)
            nn = float((nx * ny).sum())
            if nn < 1e-18:
                continue
            res.append((abs(float(np.einsum("eti,eti->", x, Gy))) / nn ** 0.5, ("Outer", tx, ty)))
            if ty[0] != "V":
                res.append((abs(float(np.einsum("eti,eti->", x, Gty))) / nn ** 0.5, ("Outer", ty, tx)))
    base = [(("M", r), m[:, :, r]) for r in range(NM)]
    for a, b in itertools.permutations(range(NM), 2):
        base.append((("MatSub", ("M", a), ("M", b)), m[:, :, a] - m[:, :, b]))
        base.append((("MatMul", ("M", a), ("M", b)), np.einsum("etij,etjk->etik", m[:, :, a], m[:, :, b])))
    for a in range(NM):
        base.append((("Transpose", ("M", a)), np.swapaxes(m[:, :, a], -1, -2)))
        base.append((("MatMul", ("M", a), ("M", a)), np.einsum("etij,etjk->etik", m[:, :, a], m[:, :, a])))
    scal = [(None, None)] + scal_exprs(v, s)
    for tb, B in base:
        gb = np.einsum("etij,etij->et", G, B)
        nb = np.einsum("etij,etij->et", B, B)
        if float(nb.sum()) < 1e-18:
            continue
        for ts, x in scal:
            if ts is None:
                res.append((abs(float(gb.sum())) / float(nb.sum()) ** 0.5, tb))
            elif ts[0] == "S" or ts[0] in SSIG:
                nn = float((x * x * nb).sum())
                if nn > 1e-18:
                    res.append((abs(float((x * gb).sum())) / nn ** 0.5, ("MatScale", ts, tb)))
    return res


def score_vector_site(G, m, v, s):
    res = []
    ve = vec_exprs(m, v, s)
    cands = list(ve)
    for a in range(NM):
        for t, x in ve:
            if t[0] != "V" and t[0] != "MatVec":
                cands.append((("MatVec", ("M", a), t), np.einsum("etij,etj->eti", m[:, :, a], x)))
    for ts, x in scal_exprs(v, s):
        for r in range(NV):
            cands.append((("VecScale", ts, ("V", r)), x[..., None] * v[:, :, r]))
    for t, x in cands:
        nn = float((x * x).sum())
        if nn > 1e-18:
            res.append((abs(float((G * x).sum())) / nn ** 0.5, t))
    return res


def score_scalar_site(G, m, v, s):
    res = []
    se = scal_exprs(v, s)
    cands = list(se)
    for (ta, a), (tb, b) in itertools.combinations_with_replacement(se, 2):
        cands.append((("SMul", ta, tb), a * b))
    for t, x in cands:
        nn = float((x * x).sum())
        if nn > 1e-18:
            res.append((abs(float((G * x).sum())) / nn ** 0.5, t))
    return res


# ---------------- materialising a candidate into instructions ----------------

def node_type(t):
    if t[0] in ("M", "V", "S"):
        return t[0]
    return sig(t[0])[0]


def emit(tree, free, block):
    """Instructions computing tree into a free register; returns that register."""
    if tree[0] in ("M", "V", "S"):
        return tree[1]
    op = tree[0]
    args = [emit(c, free, block) for c in tree[1:]]
    ty = node_type(tree)
    if not free[ty]:
        raise RuntimeError("no free register")
    o = free[ty].pop(0)
    block.append(ins(op, o, *(args + [0, 0])[:2]))
    return o


def leaves(tree, acc=None):
    acc = set() if acc is None else acc
    if tree[0] in ("M", "V", "S"):
        acc.add((tree[0], tree[1]))
    else:
        for c in tree[1:]:
            leaves(c, acc)
    return acc


def materialise(prog, p, reg_ty, r, tree, eps):
    """Insert `u = tree; s = Const(eps); u = s*u; r = r + u` before position p. Temporaries are
    registers not needed at p, not r, and not read by the expression itself."""
    lives, _ = live_sets(prog)
    lm, lv, ls = lives[p]
    live = {"M": lm, "V": lv, "S": ls}
    used = leaves(tree)
    free = {t: [x for x in range({"M": NM, "V": NV, "S": NS}[t])
                if x not in live[t] and (t, x) not in used and not (t == reg_ty and x == r)] for t in "MVS"}
    block = []
    t = emit(tree, free, block)
    if block and block[-1]["out"] == t:
        u = t
    else:
        if not free[reg_ty]:
            raise RuntimeError("no free register")
        u = free[reg_ty].pop(0)
    if not free["S"]:
        raise RuntimeError("no free scalar")
    sreg = free["S"].pop(0)
    scale = {"M": "MatScale", "V": "VecScale", "S": "SMul"}[reg_ty]
    add = {"M": "MatAdd", "V": "VecAdd", "S": "SAdd"}[reg_ty]
    block += [ins("Const", sreg, c=eps), ins(scale, u, sreg, t), ins(add, r, r, u)]
    return prog[:p] + block + prog[p:]


def tap_and_write(prog, p, x, P, tree, eps):
    """Neutral tap x <- P x before position p, plus the write branch P <- P + eps * tree at the end."""
    new = materialise(prog, len(prog), "M", P, tree, eps)
    return new[:p] + [ins("MatVec", x, P, x)] + new[p:]


def name(t):
    if t[0] in ("M", "V", "S"):
        return f"{t[0]}{t[1]}"
    return f"{t[0]}(" + ",".join(name(c) for c in t[1:]) + ")"


# ---------------- the loop ----------------

def candidates(prog, tasks):
    loss, groups = adjoints(prog, tasks)
    L = len(prog)
    lives, live_in = live_sets(prog)
    cat = lambda xs: xs  # groups are scored separately and summed via the slope's parts
    found = []
    # a site is (position, type, register); scores are summed over the two episode groups by
    # concatenating along the episode axis after padding T (zeros contribute nothing)
    Tm = max(g[0][0].shape[1] for g in groups)

    def pad(x):
        if x.shape[1] == Tm:
            return x
        w = [(0, 0)] * x.ndim
        w[1] = (0, Tm - x.shape[1])
        return np.pad(x, w)

    G = [np.concatenate([pad(g[0][i]) for g in groups], 0) for i in range(3)]
    SN = [np.concatenate([pad(g[1][i]) for g in groups], 0) for i in range(3)]
    for p in range(L + 1):
        m, v, s = SN[0][:, :, p], SN[1][:, :, p], SN[2][:, :, p]
        lm, lv, ls = lives[p]
        sites = [("M", r) for r in range(NM) if (p < L and r in lm) or (p == L and r < PM)]
        sites += [("V", r) for r in range(NV) if p < L and r in lv]
        sites += [("S", r) for r in range(NS) if p < L and r in ls]
        for ty, r in sites:
            g = {"M": G[0][:, :, p, r], "V": G[1][:, :, p, r], "S": G[2][:, :, p, r]}[ty]
            gn = float((g * g).sum()) ** 0.5
            if gn < 1e-12:
                continue
            fn = {"M": score_matrix_site, "V": score_vector_site, "S": score_scalar_site}[ty]
            res = sorted(fn(g, m, v, s), key=lambda x: -x[0])
            kept, seen = 0, set()
            for sc, tree in res:
                key = round(sc, 7)
                if key in seen:
                    continue
                seen.add(key)
                found.append((sc, ("res", p, ty, r, tree)))
                kept += 1
                if kept == 3:
                    break
    if ARM == "B":
        mE, vE, sE = SN[0][:, :, L], SN[1][:, :, L], SN[2][:, :, L]
        for P in [r for r in range(1, PM) if r not in live_in]:
            for p in range(L):
                for x in sorted(lives[p][1]):
                    gx = G[1][:, :, p, x]
                    xs = SN[1][:, :, p, x]
                    # G_P(t) = sum_{tau > t} g_x(tau) x(tau)^T (within an episode)
                    outer = np.einsum("eti,etj->etij", gx, xs)
                    rc = np.flip(np.cumsum(np.flip(outer, 1), 1), 1)
                    GP = np.concatenate([rc[:, 1:], np.zeros_like(rc[:, :1])], 1)
                    if float((GP * GP).sum()) < 1e-18:
                        continue
                    res = sorted(score_matrix_site(GP, mE, vE, sE), key=lambda z: -z[0])
                    kept, seen = 0, set()
                    for sc, tree in res:
                        key = round(sc, 7)
                        if key in seen:
                            continue
                        seen.add(key)
                        found.append((sc, ("tap", p, x, P, tree)))
                        kept += 1
                        if kept == 3:
                            break
    found.sort(key=lambda z: -z[0])
    return loss, found


def build(prog, c, eps):
    if c[0] == "res":
        _, p, ty, r, tree = c
        return materialise(prog, p, ty, r, tree, eps)
    _, p, x, P, tree = c
    return tap_and_write(prog, p, x, P, tree, eps)


def describe(c):
    if c[0] == "res":
        _, p, ty, r, tree = c
        return f"at {p}: {ty}{r} += eps * {name(tree)}"
    _, p, x, P, tree = c
    return f"tap V{x} <- M{P} V{x} at {p}; M{P} += eps * {name(tree)} at end"


# ---------------- version 2: diverse beam and compaction ----------------

def effective(prog):
    lives, _ = live_sets(prog)
    return [i for p, i in enumerate(prog) if i["out"] in dict(zip("MVS", lives[p + 1]))[sig(i["op"])[0]]]


def skeleton(prog):
    return tuple((i["op"], i["out"], i["a"], i["b"]) for i in effective(prog))


def signature(c):
    if c[0] == "res":
        return ("res", c[2], c[3], c[4][0])
    return ("tap", c[2], c[3], c[4][0])


def expand(prog, tasks):
    """Children of one program: for each of the best 60 candidates, its best eps."""
    _, found = candidates(prog, tasks)
    trials = []
    for k, (sc, c) in enumerate(found[:60]):
        for e in EPS:
            try:
                q = build(prog, c, e)
            except RuntimeError:
                break
            if len(q) <= MAX_LEN:
                trials.append((k, q, c, e))
    if not trials:
        return []
    fits = rust_fit([q for _, q, _, _ in trials])
    best = {}
    for (k, q, c, e), f in zip(trials, fits):
        if k not in best or f[0] > best[k][0][0]:
            best[k] = (f, q, c, e)
    return list(best.values())


def reads(i, ty, r):
    _, ins_t = sig(i["op"])
    return any(it == ty and i[slot] == r for slot, it in zip("ab", ins_t))


def writes(i, ty, r):
    return sig(i["op"])[0] == ty and i["out"] == r


def readers(prog, ty, r, start):
    """Positions reading (ty, r) from start on until it is written; and whether the value
    survives to the end of the step and is needed there (M0, or a persistent register the next
    step reads)."""
    out = []
    for j in range(start, len(prog)):
        if reads(prog[j], ty, r):
            out.append(j)
        if writes(prog[j], ty, r):
            return out, False
    lm, lv, ls = live_sets(prog)[0][len(prog)]
    return out, r in {"M": lm, "V": lv, "S": ls}[ty]


def unit_folds(prog):
    for i, a in enumerate(prog):
        if a["op"] not in ("MatScale", "VecScale", "SMul"):
            continue
        ty = sig(a["op"])[0]
        u, t = a["out"], a["b"]
        users, out = readers(prog, ty, u, i + 1)
        if len(users) != 1 or out:
            continue
        j = users[0]
        b = prog[j]
        if b["op"] != {"M": "MatAdd", "V": "VecAdd", "S": "SAdd"}[ty] or b["a"] == b["b"]:
            continue
        if any(writes(prog[k], ty, t) for k in range(i + 1, j)):
            continue
        other = b["b"] if b["a"] == u else b["a"]
        q = [dict(x) for x in prog]
        q[j] = ins(b["op"], b["out"], other, t)
        del q[i]
        yield q
        if ty in "MV":
            q = [dict(x) for x in prog]
            q[j] = ins({"M": "MatSub", "V": "VecSub"}[ty], b["out"], other, t)
            del q[i]
            yield q


def self_folds(prog):
    for i, a in enumerate(prog):
        if a["op"] not in ("MatScale", "VecScale", "SMul"):
            continue
        ty = sig(a["op"])[0]
        sreg, r, u = a["a"], a["b"], a["out"]
        if u == r:
            continue
        users, out = readers(prog, ty, u, i + 1)
        if len(users) != 1 or out:
            continue
        j = users[0]
        b = prog[j]
        if b["op"] != {"M": "MatAdd", "V": "VecAdd", "S": "SAdd"}[ty] or b["out"] != r or {b["a"], b["b"]} != {r, u}:
            continue
        if any(writes(prog[k], ty, r) for k in range(i + 1, j)):
            continue
        k = max((k for k in range(i) if writes(prog[k], "S", sreg)), default=None)
        if k is None or prog[k]["op"] != "Const":
            continue
        su, _ = readers(prog, "S", sreg, k + 1)
        if su != [i]:
            continue
        q = [dict(x) for x in prog]
        q[k]["c"] = 1.0 + prog[k]["c"]
        q[i] = ins(a["op"], r, sreg, r)
        del q[j]
        yield q


def cse(prog):
    for j, b in enumerate(prog):
        for i in range(j):
            a = prog[i]
            if (a["op"], a["a"], a["b"]) != (b["op"], b["a"], b["b"]) or (a["op"] == "Const" and a["c"] != b["c"]):
                continue
            ty, ins_t = sig(a["op"])
            srcs = [(it, a[slot]) for slot, it in zip("ab", ins_t)]
            if any(writes(prog[k], t2, r2) for k in range(i, j) for t2, r2 in srcs):
                continue
            if any(writes(prog[k], ty, a["out"]) for k in range(i + 1, j)):
                continue
            q = [dict(x) for x in prog]
            if a["out"] != b["out"]:
                users, out = readers(prog, ty, b["out"], j + 1)
                end = next((k for k in range(j + 1, len(prog)) if writes(prog[k], ty, b["out"])), len(prog))
                if out or any(writes(prog[k], ty, a["out"]) for k in range(j + 1, end)):
                    continue
                for k in users:
                    for slot, it in zip("ab", sig(q[k]["op"])[1]):
                        if it == ty and q[k][slot] == b["out"]:
                            q[k][slot] = a["out"]
            del q[j]
            yield q
            break


def compact(prog, fit):
    for _ in range(40):
        vs = [prog[:i] + prog[i + 1:] for i in range(len(prog))]
        vs += list(unit_folds(prog)) + list(self_folds(prog)) + list(cse(prog))
        if not vs:
            break
        fs = rust_fit(vs)
        b = max(range(len(vs)), key=lambda k: (fs[k][0], -len(vs[k])))
        if fs[b][0] > fit[0] + 1e-9 or (fs[b][0] >= fit[0] - 1e-9 and len(vs[b]) < len(prog)):
            prog, fit = vs[b], fs[b]
        else:
            break
    return prog, fit


def main2(tasks):
    t0 = time.time()
    empty = []
    beam = [(rust_fit([empty])[0], empty, "start")]
    log = open(OUT / "log.md", "w")
    log.write(f"# grow v2, arm {ARM}, task seed {TASK_SEED}, beam {BEAM}, compaction {COMPACT}\n\n"
              "| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |\n"
              "|---|---|---|---|---|---|---|---|---|\n")
    for rnd in range(1, ROUNDS + 1):
        children = []
        for f, prog, _ in beam:
            children += expand(prog, tasks)
        pool = [(f, q, None, None) for f, q, _ in beam] + [(f, q, c, e) for f, q, c, e in children]
        pool.sort(key=lambda x: (-x[0][0], len(x[1])))
        new, skels, sigs = [], set(), set()
        for f, q, c, e in pool:
            sk = skeleton(q)
            if sk in skels:
                continue
            if c is not None:
                sg = signature(c)
                if sg in sigs:
                    continue
                sigs.add(sg)
            skels.add(sk)
            new.append((f, q, c, e))
            if len(new) == BEAM:
                break
        if all(c is None for _, _, c, _ in new):
            log.write(f"| {rnd} | stop: beam unchanged | | | | | {N_RUST} | {N_GRAD} | {time.time() - t0:.0f} |\n")
            break
        nb = []
        for f, q, c, e in new:
            if c is None:
                nb.append(next(b for b in beam if b[1] is q))
                continue
            txt = f"{describe(c)}, eps {e:+g}"
            pol = polish(q, tasks)
            pf = rust_fit([pol])[0]
            if pf[0] > f[0]:
                q, f = pol, pf
                txt += "; polished"
            if COMPACT:
                n0 = len(q)
                q, f = compact(q, f)
                if len(q) < n0:
                    txt += f"; compacted {n0}->{len(q)}"
            nb.append((f, q, txt))
        beam = sorted(nb, key=lambda b: -b[0][0])
        f, q, _ = beam[0]
        test = rust_fit([q], split="test")[0]
        desc = "; ".join(f"{b[0][1]:.3f}, {len(b[1])}, {b[2]}" for b in beam)
        log.write(f"| {rnd} | {f[0]:.4f} | {f[1]:.3f} | {test[1]:.3f} | {len(q)} | {desc} | {N_RUST} | {N_GRAD} | {time.time() - t0:.0f} |\n")
        log.flush()
        json.dump({"persist_m": PM, "persist_v": 0, "persist_identity": 1, "instrs": q}, open(OUT / "best.json", "w"))
    log.write("\n```\n" + rust_report(beam[0][1]) + "\n```\n")
    log.close()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    dump = OUT / "_train.json"
    subprocess.run([EXE, "dump", "--split", "train", "--out", str(dump)] + FLAGS, check=True)
    tasks = V.load_task_json(str(dump))
    if V2:
        main2(tasks)
        for f in ("_batch.jsonl", "_one.json", "_train.json"):
            (OUT / f).unlink(missing_ok=True)
        return
    prog = []
    cur = rust_fit([prog])[0]
    log = open(OUT / "log.md", "w")
    log.write(f"# grow arm {ARM}, task seed {TASK_SEED}\n\n| round | step | train fit | train acc | test acc | len | Rust evals | seconds |\n|---|---|---|---|---|---|---|---|\n")
    t0 = time.time()
    for rnd in range(1, ROUNDS + 1):
        loss, found = candidates(prog, tasks)
        trials = []
        for sc, c in found[:60]:
            for e in EPS:
                try:
                    q = build(prog, c, e)
                except RuntimeError:
                    break
                if len(q) <= MAX_LEN:
                    trials.append((q, c, e))
        if not trials:
            log.write(f"| {rnd} | stop: no candidate fits | | | | | {N_RUST} | {time.time() - t0:.0f} |\n")
            break
        fits = rust_fit([q for q, _, _ in trials])
        bi = max(range(len(trials)), key=lambda i: fits[i][0])
        if fits[bi][0] <= cur[0] + 1e-6:
            log.write(f"| {rnd} | stop: no candidate improves (best {fits[bi][0]:.4f} vs {cur[0]:.4f}) | | | | | {N_RUST} | {time.time() - t0:.0f} |\n")
            break
        prog, c, e = trials[bi]
        cur = fits[bi]
        step_txt = f"{describe(c)}, eps {e:+g}"
        pol = polish(prog, tasks)
        pf = rust_fit([pol])[0]
        if pf[0] > cur[0]:
            prog, cur = pol, pf
            step_txt += "; constants polished"
        test = rust_fit([prog], split="test")[0]
        log.write(f"| {rnd} | {step_txt} | {cur[0]:.4f} | {cur[1]:.3f} | {test[1]:.3f} | {len(prog)} | {N_RUST} | {time.time() - t0:.0f} |\n")
        log.flush()
        json.dump({"persist_m": PM, "persist_v": 0, "persist_identity": 1, "instrs": prog}, open(OUT / "best.json", "w"))
    log.write("\n```\n" + rust_report(prog) + "\n```\n")
    log.close()
    for f in ("_batch.jsonl", "_one.json", "_train.json"):
        (OUT / f).unlink(missing_ok=True)


if __name__ == "__main__":
    main()

"""Feasibility test of adjoint-guided growth (README, "Direction 2, fourth component considered").

    python verify/adjoint_probe.py TRAIN_DUMP.json [--tau 10]

TRAIN_DUMP.json: `autoplast dump --split train --regime collision3 --out TRAIN_DUMP.json`.

For a start program and a target register R (S = M0 or P = M1), one forward pass records all
registers at the end of every step, and one backward pass of a smooth loss gives the adjoint
G_t = dL/dR_t (through a zero hook added to R at the end of each step). Every expression of one
or two ops over those registers is scored by |cos(G, e)| over all steps and episodes, and the
rank of the next step of the measured path is reported. Start programs are hand-written
reference points (CLAUDE.md rule 6); nothing here is a search.
"""

import itertools
import json
import sys

import jax
import jax.numpy as jnp
import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import probe_path_kalman as P  # noqa: E402
import verify as V  # noqa: E402

NM, NV, NS = 4, 6, 4
TAU = float(sys.argv[sys.argv.index("--tau") + 1]) if "--tau" in sys.argv else 10.0


def ins(op, out, a=0, b=0, c=0.0):
    return {"op": op, "out": out, "a": a, "b": b, "c": c}


def exec_instrs(instrs, m, vec, s):
    for i in instrs:
        op, o, a, b, c = i["op"], i["out"], i["a"], i["b"], i["c"]
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


def make_step(instrs, target, resid=None):
    """State (S, P1, P2); P1, P2 persistent, start at I (space of D and E). At the end of the step
    the hook h (and, if given, eps * resid(registers)) is added to M[target]. Returns the new
    state and the registers at the end of the step, before the hook."""

    def step(state, k, v, h, eps=0.0):
        d = k.shape[0]
        m = [state[0], state[1], state[2], jnp.zeros((d, d))]
        vec = [k, v] + [jnp.zeros(d) for _ in range(NV - 2)]
        s = [jnp.float32(0.0)] * NS
        exec_instrs(instrs, m, vec, s)
        regs = (jnp.stack(m), jnp.stack(vec), jnp.stack(s))
        m[target] = m[target] + h
        if resid is not None:
            m[target] = m[target] + eps * resid(*regs)
        return (m[0], m[1], m[2]), regs

    return step


def run_group(step, task, hooks, eps=0.0):
    keys, vals, W, Q, Qm = task[:5]
    QV = task[5] if len(task) > 5 else None
    d = keys.shape[1]
    init = (jnp.zeros((d, d)), jnp.eye(d), jnp.eye(d))

    def episode(w, h, q, qm, qv):
        def body(st, x):
            kv, hh = x
            st, regs = step(st, keys[kv[0]], vals[kv[1]], hh, eps)
            return st, regs

        st, regs = jax.lax.scan(body, init, (w, h))
        S = st[0]
        qk = keys[q[:, 0]] if qv is None else qv
        o = qk @ S.T
        on = jnp.sqrt(jnp.sum(o * o, axis=1, keepdims=True) + 1e-12)
        o = o / on
        logits = TAU * o @ vals.T
        ce = -jax.nn.log_softmax(logits)[jnp.arange(q.shape[0]), q[:, 1]]
        ok = (jnp.argmax(o @ vals.T, axis=1) == q[:, 1]) & qm & (on[:, 0] > 1e-6)
        return jnp.sum(ce * qm), jnp.sum(qm), jnp.sum(ok), regs

    if QV is None:
        return jax.vmap(lambda w, h, q, qm: episode(w, h, q, qm, None))(W, hooks, Q, Qm)
    return jax.vmap(episode)(W, hooks, Q, Qm, QV)


def adjoint(step, tasks):
    """Mean loss, accuracy, adjoint fields G per group, register traces per group."""
    n = sum(int(t[4].sum()) for t in tasks)
    Gs, traces, tot_ce, tot_ok = [], [], 0.0, 0
    for t in tasks:
        d = t[0].shape[1]
        hooks = jnp.zeros(t[2].shape[:2] + (d, d))

        def loss(h, t=t):
            ce, _, ok, regs = run_group(step, t, h)
            return jnp.sum(ce) / n, (ok, regs)

        (l, (ok, regs)), g = jax.value_and_grad(loss, has_aux=True)(hooks)
        Gs.append(np.asarray(g, dtype=np.float32))
        traces.append(tuple(np.asarray(r, dtype=np.float32) for r in regs))
        tot_ce += float(l)
        tot_ok += int(jnp.sum(ok))
    return tot_ce, tot_ok / n, Gs, traces


def accuracy(step, tasks, eps):
    n = sum(int(t[4].sum()) for t in tasks)
    ok = 0
    for t in tasks:
        d = t[0].shape[1]
        _, _, c, _ = jax.jit(lambda t=t: run_group(step, t, jnp.zeros(t[2].shape[:2] + (d, d)), eps))()
        ok += int(jnp.sum(c))
    return ok / n


# ---- candidate expressions over the end-of-step registers (numpy on traces) ----
# trace m: (E, T, 4, d, d), v: (E, T, 6, d), s: (E, T, 4)

def vec_cands(m, v, s):
    out = {f"V{i}": v[:, :, i] for i in range(NV)}
    for a, b in itertools.product(range(NM), range(NV)):
        out[f"MatVec(M{a},V{b})"] = np.einsum("etij,etj->eti", m[:, :, a], v[:, :, b])
    for a, b in itertools.permutations(range(NV), 2):
        out[f"VecAdd(V{a},V{b})"] = v[:, :, a] + v[:, :, b] if a < b else None
        out[f"VecSub(V{a},V{b})"] = v[:, :, a] - v[:, :, b]
        out[f"Hadamard(V{a},V{b})"] = v[:, :, a] * v[:, :, b] if a < b else None
    for a, b in itertools.product(range(NS), range(NV)):
        out[f"VecScale(s{a},V{b})"] = s[:, :, a, None] * v[:, :, b]
    for a in range(NV):
        out[f"Normalize(V{a})"] = v[:, :, a] / (np.linalg.norm(v[:, :, a], axis=-1, keepdims=True) + 1e-6)
        out[f"Tanh(V{a})"] = np.tanh(v[:, :, a])
    return {k: x for k, x in out.items() if x is not None}


def scal_cands(v, s):
    out = {f"s{i}": s[:, :, i] for i in range(NS)}
    for a, b in itertools.combinations_with_replacement(range(NV), 2):
        out[f"Dot(V{a},V{b})"] = np.einsum("eti,eti->et", v[:, :, a], v[:, :, b])
    for a in range(NV):
        out[f"Norm(V{a})"] = np.linalg.norm(v[:, :, a], axis=-1)
    for a in range(NS):
        out[f"Sigmoid(s{a})"] = 1 / (1 + np.exp(-s[:, :, a]))
        out[f"Recip(s{a})"] = s[:, :, a] / (s[:, :, a] ** 2 + 1e-6)
    return out


def mat_cands(m, v, s):
    """Yield (name, value) for every one- and two-op matrix expression."""
    mats = {f"M{i}": m[:, :, i] for i in range(NM)}
    vc = vec_cands(m, v, s)
    vregs = {k: x for k, x in vc.items() if k.startswith("V") and len(k) == 2}
    sc = scal_cands(v, s)
    sregs = {k: x for k, x in sc.items() if k.startswith("s") and len(k) == 2}
    d1 = {}
    for (na, a), (nb, b) in itertools.product(vregs.items(), vregs.items()):
        d1[f"Outer({na},{nb})"] = np.einsum("eti,etj->etij", a, b)
    for (na, a), (nb, b) in itertools.product(mats.items(), mats.items()):
        d1[f"MatMul({na},{nb})"] = np.einsum("etij,etjk->etik", a, b)
        if na < nb:
            d1[f"MatAdd({na},{nb})"] = a + b
        if na != nb:
            d1[f"MatSub({na},{nb})"] = a - b
    for (ns_, x), (na, a) in itertools.product(sregs.items(), mats.items()):
        d1[f"MatScale({ns_},{na})"] = x[..., None, None] * a
    for na, a in mats.items():
        d1[f"Transpose({na})"] = np.swapaxes(a, -1, -2)
        d1[na] = a
    yield from d1.items()
    # two ops: one input of a one-op expression is itself a one-op expression
    for (nx, x), (nr, r) in itertools.product(vc.items(), vregs.items()):
        if nx not in vregs:
            yield f"Outer({nx},{nr})", np.einsum("eti,etj->etij", x, r)
            yield f"Outer({nr},{nx})", np.einsum("eti,etj->etij", r, x)
    for (ny, y), (na, a) in itertools.product(d1.items(), mats.items()):
        if ny not in mats:
            yield f"MatMul({na},{ny})", np.einsum("etij,etjk->etik", a, y)
            yield f"MatMul({ny},{na})", np.einsum("etij,etjk->etik", y, a)
    for (ns_, x), (ny, y) in itertools.product(sc.items(), d1.items()):
        if ns_ not in sregs or ny not in mats:
            yield f"MatScale({ns_},{ny})", x[..., None, None] * y


def rank(Gs, traces, target_fn, keep=150):
    """Score all candidates on every group. Exact duplicates (same values up to sign, by a random
    projection) are dropped while scoring; the best `keep` are then grouped into classes of the
    same direction (|cos| > 0.999 between candidates, sign ignored), the threshold used for the
    target. Returns the class list [(score, name, sign, |cos| with target)], the target's class
    rank (None if not among the best `keep`) and its raw rank among all distinct candidates."""
    rng = np.random.default_rng(0)
    gg = sum(float((G * G).sum()) for G in Gs)
    tgt = [target_fn(*tr) for tr in traces]
    tt = sum(float((x * x).sum()) for x in tgt)
    proj = [rng.standard_normal(G.shape).astype(np.float32) for G in Gs]
    seen, scored, top = {}, [], []
    for items in zip(*[mat_cands(*tr) for tr in traces]):
        name = items[0][0]
        es = [e for _, e in items]
        ee = sum(float((e * e).sum()) for e in es)
        if ee < 1e-18:
            continue
        fp = round(abs(sum(float((p * e).sum()) for p, e in zip(proj, es))) / ee ** 0.5, 5)
        if fp in seen:
            continue
        seen[fp] = name
        ge = sum(float((G * e).sum()) for G, e in zip(Gs, es))
        te = sum(float((x * e).sum()) for x, e in zip(tgt, es)) / (tt * ee) ** 0.5
        cos = ge / (gg * ee) ** 0.5
        scored.append((abs(cos), abs(te)))
        top.append((abs(cos), name, cos, abs(te), [e / ee ** 0.5 for e in es]))
        if len(top) > 4 * keep:
            top.sort(key=lambda x: -x[0])
            del top[keep:]
    top.sort(key=lambda x: -x[0])
    top = top[:keep]
    classes = []
    for sc, name, cos, tc, es in top:
        for c in classes:
            if abs(sum(float((a * b).sum()) for a, b in zip(c[4], es))) > 0.999:
                c[3] = max(c[3], tc)
                break
        else:
            classes.append([sc, name, cos, tc, es])
    trank = next((i + 1 for i, c in enumerate(classes) if c[3] > 0.999), None)
    traw = sorted(scored, key=lambda x: -x[0])
    raw = next((i + 1 for i, x in enumerate(traw) if x[1] > 0.999), None)
    return [c[:4] for c in classes], trank, raw, len(scored)


def e_fn(name):
    """Values of a candidate by name, for the line search (vectors from registers only)."""
    def f(m, v, s):
        return eval(name, {}, dict(
            Outer=lambda a, b: jnp.outer(a, b), MatMul=lambda a, b: a @ b, MatAdd=lambda a, b: a + b,
            MatSub=lambda a, b: a - b, MatScale=lambda x, a: x * a, Transpose=lambda a: a.T,
            MatVec=lambda a, b: a @ b, VecAdd=lambda a, b: a + b, VecSub=lambda a, b: a - b,
            VecScale=lambda x, a: x * a, Hadamard=lambda a, b: a * b,
            Normalize=lambda a: a / (jnp.linalg.norm(a) + 1e-6), Tanh=jnp.tanh,
            Dot=lambda a, b: a @ b, Norm=jnp.linalg.norm, Sigmoid=jax.nn.sigmoid,
            Recip=lambda x: x / (x * x + 1e-6),
            **{f"M{i}": m[i] for i in range(NM)}, **{f"V{i}": v[i] for i in range(NV)},
            **{f"s{i}": s[i] for i in range(NS)}))
    return f


EPS = [sgn * e for e in (0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0) for sgn in (1, -1)]


def best_eps(instrs, target, name, tasks):
    best = (-1.0, 0.0)
    for e in EPS:
        a = accuracy(make_step(instrs, target, e_fn(name)), tasks, e)
        if a > best[0]:
            best = (a, e)
    return best


LA = [ins("Outer", 3, 1, 0), ins("MatAdd", 0, 0, 3)]
TRANSITIONS = [
    ("T1 empty -> linear attention", [], 0, "Outer(V1,V0)", lambda m, v, s: np.einsum("eti,etj->etij", v[:, :, 1], v[:, :, 0])),
    ("T2 linear attention -> delta (erase along k)", LA, 0, "Outer(MatVec(M0,V0),V0)",
     lambda m, v, s: np.einsum("eti,etj->etij", np.einsum("etij,etj->eti", m[:, :, 0], v[:, :, 0]), v[:, :, 0])),
    ("T3 delta with key Pk, P fixed -> D' (P - c (Pk)(Pk)^T)", P.prog(beta=0.5, normalise=False, p_update=False, q_term=False)["instrs"], 1,
     "Outer(V2,V2)", lambda m, v, s: np.einsum("eti,etj->etij", v[:, :, 2], v[:, :, 2])),
    ("T4 normalised gain, P fixed -> D (P - c g (Pk)^T)", P.prog(beta=1.0, delta=0.01, p_update=False, q_term=False)["instrs"], 1,
     "Outer(V3,V2)", lambda m, v, s: np.einsum("eti,etj->etij", v[:, :, 3], v[:, :, 2])),
    ("T5 D at c = 1, no q -> E (+ q I)", P.prog(beta=1.0, delta=0.01, c=1.0, q_term=False)["instrs"], 1,
     "M2", lambda m, v, s: m[:, :, 2]),
]

if __name__ == "__main__":
    tasks = V.load_task_json(sys.argv[1])
    print(f"tau = {TAU}\n")
    for title, instrs, target, tname, tfn in TRANSITIONS:
        step = make_step(instrs, target)
        ce, acc0, Gs, traces = adjoint(step, tasks)
        classes, trank, raw, n = rank(Gs, traces, tfn)
        print(f"## {title}\nregister M{target}; start: train acc {acc0:.3f}, loss {ce:.4f}; {n} distinct candidates")
        tsc = next((c[0] for c in classes if c[3] > 0.999), None)
        print(f"target {tname}: class rank {trank}, raw rank {raw}" + (f", |cos| {tsc:.3f} (best {classes[0][0]:.3f})" if tsc else ""))
        for sc, name, cos, tc in classes[:5]:
            print(f"   {sc:.3f}  sign {'+' if cos > 0 else '-'}  {name}   (|cos| with target {tc:.2f})")
        if "--no-linesearch" not in sys.argv:
            for label, nm in [("best class", classes[0][1]), ("target", tname)]:
                try:
                    a, e = best_eps(instrs, target, nm, tasks)
                    print(f"   insert {label} {nm} with best eps {e:+g}: train acc {a:.3f} (start {acc0:.3f})")
                except Exception as ex:  # noqa: BLE001
                    print(f"   insert {label} {nm}: line search failed ({type(ex).__name__}: {ex})")
        print(flush=True)

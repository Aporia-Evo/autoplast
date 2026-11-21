"""Phase 0: Fair BPTT baseline tuning of all known memory-update families on the exact
Rust collision3 train dump (`v2/data/collision3_train_s1.json`).

Every family is tuned with the exact same MSE ||S q - v||^2 BPTT objective (multi-start Adam),
compiled into its exact autoplast JSON (<= 24 instructions, NM=4, NV=6, NS=4), and audited
through `v2/strict_eval.py` (Rust `autoplast eval`, JAX x64 + norm-eps 1e-9, v3 T=256 < 100
stability check, and 12 paired fresh draws with query_gap=0 and query_gap=4).
"""

from __future__ import annotations

import json
import pathlib
import sys
import time

import jax
import jax.numpy as jnp
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "verify"))
sys.path.insert(0, str(ROOT / "v2"))

import strict_eval as SE  # noqa: E402
import verify as V  # noqa: E402

TRAIN_DUMP = ROOT / "v2" / "data" / "collision3_train_s1.json"
OUT_DIR = ROOT / "v2" / "baselines_bptt"


def ins(op: str, out: int, a: int = 0, b: int = 0, c: float = 0.0) -> dict:
    return {"op": op, "out": out, "a": a, "b": b, "c": float(c)}


# --- Exact JAX batched step functions + matching autoplast JSON emitters ---

def step_decayed_la(st, k, v, p):
    a, b = p[0], p[1]
    return st.at[:, 0].set(a * st[:, 0] + b * (v[:, :, None] * k[:, None, :]))


def json_decayed_la(p):
    a, b = float(p[0]), float(p[1])
    return {"persist_m": 1, "persist_v": 0, "persist_identity": 0, "instrs": [
        ins("Const", 0, c=a), ins("MatScale", 0, 0, 0),
        ins("Outer", 1, 1, 0), ins("Const", 1, c=b), ins("MatScale", 1, 1, 1),
        ins("MatAdd", 0, 0, 1),
    ]}


def step_deltanet(st, k, v, p):
    e = p[0]
    S = st[:, 0]
    sk = jnp.einsum("bij,bj->bi", S, k)
    return st.at[:, 0].set(S + e * ((v - sk)[:, :, None] * k[:, None, :]))


def json_deltanet(p):
    e = float(p[0])
    return {"persist_m": 1, "persist_v": 0, "persist_identity": 0, "instrs": [
        ins("MatVec", 2, 0, 0), ins("VecSub", 3, 1, 2), ins("Outer", 1, 3, 0),
        ins("Const", 0, c=e), ins("MatScale", 1, 0, 1), ins("MatAdd", 0, 0, 1),
    ]}


def step_gated_deltanet(st, k, v, p):
    a, e = p[0], p[1]
    S = st[:, 0]
    sk = jnp.einsum("bij,bj->bi", S, k)
    Sn = a * (S - e * (sk[:, :, None] * k[:, None, :])) + e * (v[:, :, None] * k[:, None, :])
    return st.at[:, 0].set(Sn)


def json_gated_deltanet(p):
    a, e = float(p[0]), float(p[1])
    return {"persist_m": 1, "persist_v": 0, "persist_identity": 0, "instrs": [
        ins("Const", 0, c=e), ins("MatVec", 2, 0, 0), ins("Outer", 1, 2, 0),
        ins("MatScale", 1, 0, 1), ins("MatSub", 0, 0, 1), ins("Const", 1, c=a),
        ins("MatScale", 0, 1, 0), ins("Outer", 3, 1, 0), ins("MatScale", 3, 0, 3),
        ins("MatAdd", 0, 0, 3),
    ]}


def step_decoupled_ew(st, k, v, p):
    a, e, b = p[0], p[1], p[2]
    S = st[:, 0]
    sk = jnp.einsum("bij,bj->bi", S, k)
    Sn = a * S - e * (sk[:, :, None] * k[:, None, :]) + b * (v[:, :, None] * k[:, None, :])
    return st.at[:, 0].set(Sn)


def json_decoupled_ew(p):
    a, e, b = float(p[0]), float(p[1]), float(p[2])
    return {"persist_m": 1, "persist_v": 0, "persist_identity": 0, "instrs": [
        ins("MatVec", 2, 0, 0), ins("Outer", 1, 2, 0), ins("Const", 0, c=e),
        ins("MatScale", 1, 0, 1), ins("Const", 1, c=a), ins("MatScale", 0, 1, 0),
        ins("MatSub", 0, 0, 1), ins("Outer", 2, 1, 0), ins("Const", 2, c=b),
        ins("MatScale", 2, 2, 2), ins("MatAdd", 0, 0, 2),
    ]}


def step_kron_delta(st, k, v, p):
    a, beta, c = p[0], p[1], p[2]
    S = a * st[:, 0]
    sk = jnp.einsum("bij,bj->bi", S, k)
    dot = jnp.sum(v * sk, axis=-1)  # (B,)
    coeff = -beta * dot + c
    Sn = S + coeff[:, None, None] * (v[:, :, None] * k[:, None, :])
    return st.at[:, 0].set(Sn)


def json_kron_delta(p):
    a, beta, c = float(p[0]), float(p[1]), float(p[2])
    return {"persist_m": 1, "persist_v": 0, "persist_identity": 0, "instrs": [
        ins("Const", 3, c=a), ins("MatScale", 0, 3, 0),
        ins("MatVec", 2, 0, 0), ins("Dot", 0, 1, 2),
        ins("Const", 1, c=-beta), ins("SMul", 0, 0, 1),
        ins("Const", 2, c=c), ins("SAdd", 0, 0, 2),
        ins("Outer", 1, 1, 0), ins("MatScale", 1, 0, 1), ins("MatAdd", 0, 0, 1),
    ]}


def _recip(x, eps=1e-6):
    return x / (x * x + eps)


def step_rls_2p(st, k, v, p):
    delta, rho = p[0], p[1]
    S, P = st[:, 0], st[:, 1]
    pk = jnp.einsum("bij,bj->bi", P, k)
    denom = delta + jnp.sum(k * pk, axis=-1)
    g = _recip(denom)[:, None] * pk
    sk = jnp.einsum("bij,bj->bi", S, k)
    Sn = S + (v - sk)[:, :, None] * g[:, None, :]
    Pn = rho * (P - g[:, :, None] * pk[:, None, :])
    return jnp.stack([Sn, Pn], axis=1)


def json_rls_2p(p):
    delta, rho = float(p[0]), float(p[1])
    return {"persist_m": 2, "persist_v": 0, "persist_identity": 1, "instrs": [
        ins("MatVec", 2, 1, 0), ins("Dot", 0, 0, 2), ins("Const", 1, c=delta),
        ins("SAdd", 0, 0, 1), ins("Recip", 0, 0), ins("VecScale", 3, 0, 2),
        ins("MatVec", 4, 0, 0), ins("VecSub", 5, 1, 4), ins("Outer", 2, 5, 3),
        ins("MatAdd", 0, 0, 2), ins("Outer", 3, 3, 2), ins("MatSub", 1, 1, 3),
        ins("Const", 2, c=rho), ins("MatScale", 1, 2, 1),
    ]}


def step_rls_5p(st, k, v, p):
    a_s, beta, delta, rho, c = p[0], p[1], p[2], p[3], p[4]
    S, P = st[:, 0], st[:, 1]
    pk = jnp.einsum("bij,bj->bi", P, k)
    denom = delta + jnp.sum(k * pk, axis=-1)
    g = _recip(denom)[:, None] * pk
    sk = jnp.einsum("bij,bj->bi", S, k)
    Sn = a_s * S + beta * ((v - sk)[:, :, None] * g[:, None, :])
    Pn = rho * (P - c * (g[:, :, None] * pk[:, None, :]))
    return jnp.stack([Sn, Pn], axis=1)


def json_rls_5p(p):
    a_s, beta, delta, rho, c = (float(x) for x in p)
    return {"persist_m": 2, "persist_v": 0, "persist_identity": 1, "instrs": [
        ins("MatVec", 2, 1, 0), ins("Dot", 0, 0, 2), ins("Const", 1, c=delta),
        ins("SAdd", 0, 0, 1), ins("Recip", 0, 0), ins("VecScale", 3, 0, 2),
        ins("MatVec", 4, 0, 0), ins("VecSub", 5, 1, 4),
        ins("Const", 1, c=beta), ins("VecScale", 5, 1, 5),
        ins("Outer", 2, 5, 3), ins("Const", 1, c=a_s), ins("MatScale", 0, 1, 0),
        ins("MatAdd", 0, 0, 2),
        ins("Outer", 3, 3, 2), ins("Const", 1, c=c), ins("MatScale", 3, 1, 3),
        ins("MatSub", 1, 1, 3), ins("Const", 2, c=rho), ins("MatScale", 1, 2, 1),
    ]}


def step_kalman_2p(st, k, v, p):
    delta, q = p[0], p[1]
    S, P, I = st[:, 0], st[:, 1], st[:, 2]
    pk = jnp.einsum("bij,bj->bi", P, k)
    denom = delta + jnp.sum(k * pk, axis=-1)
    g = _recip(denom)[:, None] * pk
    sk = jnp.einsum("bij,bj->bi", S, k)
    Sn = S + (v - sk)[:, :, None] * g[:, None, :]
    Pn = P - g[:, :, None] * pk[:, None, :] + q * I
    return jnp.stack([Sn, Pn, I], axis=1)


def json_kalman_2p(p):
    delta, q = float(p[0]), float(p[1])
    return {"persist_m": 3, "persist_v": 0, "persist_identity": 1, "instrs": [
        ins("MatVec", 2, 1, 0), ins("Dot", 0, 0, 2), ins("Const", 1, c=delta),
        ins("SAdd", 0, 0, 1), ins("Recip", 0, 0), ins("VecScale", 3, 0, 2),
        ins("MatVec", 4, 0, 0), ins("VecSub", 5, 1, 4), ins("Outer", 3, 5, 3),
        ins("MatAdd", 0, 0, 3), ins("Outer", 3, 3, 2), ins("MatSub", 1, 1, 3),
        ins("Const", 2, c=q), ins("MatScale", 3, 2, 2), ins("MatAdd", 1, 1, 3),
    ]}


def step_kalman_6p(st, k, v, p):
    a_s, beta, delta, a_p, c, q = p[0], p[1], p[2], p[3], p[4], p[5]
    S, P, I = st[:, 0], st[:, 1], st[:, 2]
    pk = jnp.einsum("bij,bj->bi", P, k)
    denom = delta + jnp.sum(k * pk, axis=-1)
    g = _recip(denom)[:, None] * pk
    sk = jnp.einsum("bij,bj->bi", S, k)
    Sn = a_s * S + beta * ((v - sk)[:, :, None] * g[:, None, :])
    Pn = a_p * P - c * (g[:, :, None] * pk[:, None, :]) + q * I
    return jnp.stack([Sn, Pn, I], axis=1)


def json_kalman_6p(p):
    a_s, beta, delta, a_p, c, q = (float(x) for x in p)
    return {"persist_m": 3, "persist_v": 0, "persist_identity": 1, "instrs": [
        ins("MatVec", 2, 1, 0), ins("Dot", 0, 0, 2), ins("Const", 1, c=delta),
        ins("SAdd", 0, 0, 1), ins("Recip", 0, 0), ins("VecScale", 3, 0, 2),
        ins("MatVec", 4, 0, 0), ins("VecSub", 5, 1, 4),
        ins("Const", 1, c=beta), ins("VecScale", 5, 1, 5),
        ins("Outer", 3, 5, 3), ins("Const", 1, c=a_s), ins("MatScale", 0, 1, 0),
        ins("MatAdd", 0, 0, 3),
        ins("Outer", 3, 3, 2), ins("Const", 1, c=c), ins("MatScale", 3, 1, 3),
        ins("Const", 2, c=a_p), ins("MatScale", 1, 2, 1), ins("MatSub", 1, 1, 3),
        ins("Const", 3, c=q), ins("MatScale", 3, 3, 2), ins("MatAdd", 1, 1, 3),
    ]}


FAMILIES = [
    ("decayed_la", 1, False, step_decayed_la, json_decayed_la,
     [[0.9, 1.0], [0.8, 0.5], [0.95, 0.8]]),
    ("deltanet", 1, False, step_deltanet, json_deltanet,
     [[0.5], [0.8], [0.3]]),
    ("gated_deltanet", 1, False, step_gated_deltanet, json_gated_deltanet,
     [[1.0, 0.6], [0.95, 0.5], [0.99, 0.8]]),
    ("decoupled_ew", 1, False, step_decoupled_ew, json_decoupled_ew,
     [[1.0, 0.6, 0.6], [0.98, 0.8, 0.6], [0.95, 0.5, 0.8]]),
    ("kron_delta", 1, False, step_kron_delta, json_kron_delta,
     [[0.9, 0.7, 0.7], [0.95, 1.0, 1.0], [0.85, 0.5, 0.8]]),
    ("rls_2p", 2, True, step_rls_2p, json_rls_2p,
     [[0.1, 1.05], [0.03, 1.02], [0.3, 1.1], [0.01, 1.01]]),
    ("rls_5p", 2, True, step_rls_5p, json_rls_5p,
     [[1.0, 1.0, 0.1, 1.05, 1.0], [0.99, 0.9, 0.03, 1.02, 0.8], [0.98, 1.0, 0.05, 1.08, 0.9]]),
    ("kalman_2p", 3, True, step_kalman_2p, json_kalman_2p,
     [[0.01, 0.01], [0.01, 0.003], [0.05, 0.05], [0.1, 0.1]]),
    ("kalman_6p", 3, True, step_kalman_6p, json_kalman_6p,
     [[1.0, 1.0, 0.01, 1.0, 1.0, 0.01],
      [0.99, 1.0, 0.01, 0.98, 1.0, 0.05],
      [1.0, 0.95, 0.05, 0.95, 0.8, 0.1],
      [0.98, 1.05, 0.005, 0.99, 0.9, 0.02]]),
]


def eval_family_mse(step_fn, pm, ident, tasks, p, st_l2=1e-4):
    mse_sum = jnp.asarray(0.0, dtype=jnp.float64)
    tot_sum = jnp.asarray(0.0, dtype=jnp.float64)
    l2_sum = jnp.asarray(0.0, dtype=jnp.float64)
    for task in tasks:
        keys, vals, W, Q, Qmask = task[:5]
        keys, vals = keys.astype(jnp.float64), vals.astype(jnp.float64)
        B, d = W.shape[0], keys.shape[1]
        S0 = jnp.zeros((1, d, d), dtype=jnp.float64)
        if pm > 1:
            P0 = jnp.eye(d, dtype=jnp.float64) if ident else jnp.zeros((d, d), dtype=jnp.float64)
            st_one = jnp.concatenate([S0, jnp.broadcast_to(P0[None], (pm - 1, d, d))], axis=0)
        else:
            st_one = S0
        st0 = jnp.broadcast_to(st_one[None], (B, pm, d, d))
        Ks = keys[W[:, :, 0]].swapaxes(0, 1)
        Vs = vals[W[:, :, 1]].swapaxes(0, 1)

        def body(carry, kv):
            st, l2 = carry
            st = step_fn(st, kv[0], kv[1], p)
            return (st, l2 + jnp.mean(st * st)), None

        (st, l2_ep), _ = jax.lax.scan(body, (st0, jnp.asarray(0.0, dtype=jnp.float64)), (Ks, Vs))
        S = st[:, 0]
        qk = keys[Q[:, :, 0]]
        tv = vals[Q[:, :, 1]]
        o = jnp.einsum("bij,bqj->bqi", S, qk)
        sq = jnp.sum((o - tv) ** 2, axis=-1)
        mse_sum = mse_sum + jnp.sum(jnp.where(Qmask, sq, 0.0))
        tot_sum = tot_sum + jnp.sum(Qmask)
        l2_sum = l2_sum + l2_ep / max(W.shape[1], 1)
    mse = mse_sum / jnp.maximum(tot_sum, 1.0)
    return mse + st_l2 * (l2_sum / len(tasks)), mse


def tune_family(name, pm, ident, step_fn, inits, tasks, steps=500, lr_hi=2e-2):
    vg = jax.jit(jax.value_and_grad(lambda p: eval_family_mse(step_fn, pm, ident, tasks, p), has_aux=True))
    best_mse = float("inf")
    best_p = None
    for init in inits:
        p = jnp.asarray(init, dtype=jnp.float64)
        m = jnp.zeros_like(p)
        v = jnp.zeros_like(p)
        cur_best_p, cur_best_mse = p, float("inf")
        for s in range(steps):
            lr = lr_hi * (0.05 + 0.95 * 0.5 * (1.0 + np.cos(np.pi * s / max(steps - 1, 1))))
            (loss, mse), g = vg(p)
            fmse = float(mse)
            if np.isfinite(fmse) and fmse < cur_best_mse:
                cur_best_mse = fmse
                cur_best_p = p
            if not bool(jnp.all(jnp.isfinite(g))):
                p = cur_best_p
                m = jnp.zeros_like(p)
                v = jnp.zeros_like(p)
                lr *= 0.2
                continue
            gn = jnp.linalg.norm(g) + 1e-12
            g = g * jnp.minimum(1.0, 1.0 / gn)
            m = 0.9 * m + 0.1 * g
            v = 0.999 * v + 0.001 * (g * g)
            bc1, bc2 = 1.0 - 0.9 ** (s + 1), 1.0 - 0.999 ** (s + 1)
            p = p - lr * (m / bc1) / (jnp.sqrt(v / bc2) + 1e-8)
        if cur_best_mse < best_mse:
            best_mse = cur_best_mse
            best_p = np.asarray(cur_best_p, dtype=np.float64)
    return best_p, best_mse


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Note: strict_eval enables x64, so explicitly cast train dump arrays to float32 for BPTT.
    tasks = V.load_task_json(str(TRAIN_DUMP))
    print(f"Loaded exact Rust train dump: {TRAIN_DUMP} ({len(tasks)} write-length groups)", flush=True)

    rows = []
    for name, pm, ident, step_fn, json_fn, inits in FAMILIES:
        t0 = time.perf_counter()
        best_p, best_mse = tune_family(name, pm, ident, step_fn, inits, tasks)
        prog = json_fn(best_p)
        jpath = OUT_DIR / f"{name}.json"
        jpath.write_text(json.dumps(prog), encoding="utf-8")
        audit = SE.audit_program(str(jpath), run_draws=True)
        audit["family"] = name
        audit["params"] = [round(float(x), 5) for x in best_p]
        audit["train_mse"] = round(best_mse, 4)
        audit["tune_seconds"] = round(time.perf_counter() - t0, 1)
        rows.append(audit)
        print(
            f"  {name:15s} | len={audit['n_instrs']:2d} ok={audit['space_ok']} | "
            f"tr={audit['rust_train']:.3f} te={audit['rust_test_col3']:.3f} "
            f"(jax_e9={audit['jax_x64_e9']:.3f}) | T128={audit['rust_t128']:.3f} "
            f"T256_max={max(audit['t256_std_max'], audit['t256_col_max']):.2f} stab={audit['stable_lt100']} | "
            f"12draws={audit['draws_12_gap0_mean']:.3f} gap4={audit['draws_12_gap4_mean']:.3f} | "
            f"p={audit['params']}",
            flush=True,
        )

    (OUT_DIR / "baselines_summary.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    print("\n## Fair BPTT-Tuned Known Families (exact Rust collision3 train dump, task seed 1)")
    print("| family | instr | params (BPTT MSE) | train | test col3 | JAX x64 e-9 | T128 K8 | T256 max (<100) | 12 draws | gap=4 |")
    print("|---|---:|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        t256_mx = max(r["t256_std_max"], r["t256_col_max"])
        stab_str = f"{t256_mx:.2f} (ok)" if r["stable_lt100"] else f"{t256_mx:.2e} (FAIL)"
        print(
            f"| {r['family']} | {r['n_instrs']} | `{r['params']}` | {r['rust_train']:.3f} | "
            f"**{r['rust_test_col3']:.3f}** | {r['jax_x64_e9']:.3f} | {r['rust_t128']:.3f} | "
            f"{stab_str} | {r['draws_12_gap0_mean']:.3f} | {r['draws_12_gap4_mean']:.3f} |"
        )


if __name__ == "__main__":
    main()

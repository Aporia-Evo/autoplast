"""Unified strict audit for any autoplast JSON program (baselines and discovered rules alike).

Checks:
1. Exact search-space compliance: <= 24 instructions, registers in (NM=4, NV=6, NS=4),
   ops in the 20-op D/E/K alphabet, persist_m <= 3, persist_v == 0.
2. Exact Rust `autoplast eval --regime collision3` (all suites, including train & collision3 test).
3. Independent JAX verification on exact Rust dump `v2/data/collision3_test_s9.json`:
   float32 eps=1e-6 (agreement with Rust), float64 eps=1e-9, and eps_scale.py if delta > 0.02.
4. v3 stability bound: 64 episodes x 256 write steps (both standard K=8 and collision K=8)
   in float64; every entry of every persistent state must stay finite and < 100.
5. Optional 12 paired fresh draws (task seeds 101..112) and --query-gap 4 via Rust binary.

Usage:
  python v2/strict_eval.py path/to/prog.json [--draws]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import statistics as st
import subprocess
import sys

import jax
jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "verify"))
_had_x64 = "--x64" in sys.argv
if not _had_x64:
    sys.argv.append("--x64")
import verify as V  # noqa: E402
if not _had_x64:
    sys.argv.remove("--x64")

EXE = ROOT / "target" / "release" / ("autoplast.exe" if (ROOT / "target/release/autoplast.exe").exists() else "autoplast")
TEST_DUMP = ROOT / "v2" / "data" / "collision3_test_s9.json"

ALLOWED_OPS = {
    "Outer", "MatAdd", "MatSub", "MatScale", "Transpose", "MatMul",
    "MatVec", "VecAdd", "VecSub", "VecScale", "Hadamard", "Normalize", "Tanh",
    "Dot", "Const", "SAdd", "SMul", "Sigmoid", "Norm", "Recip",
}
OP_SIG = {
    "Outer": ("M", ("V", "V")), "MatAdd": ("M", ("M", "M")), "MatSub": ("M", ("M", "M")),
    "MatScale": ("M", ("S", "M")), "Transpose": ("M", ("M",)), "MatMul": ("M", ("M", "M")),
    "MatVec": ("V", ("M", "V")), "VecAdd": ("V", ("V", "V")), "VecSub": ("V", ("V", "V")),
    "VecScale": ("V", ("S", "V")), "Hadamard": ("V", ("V", "V")), "Normalize": ("V", ("V",)),
    "Tanh": ("V", ("V",)), "Dot": ("S", ("V", "V")), "Const": ("S", ()),
    "SAdd": ("S", ("S", "S")), "SMul": ("S", ("S", "S")), "Sigmoid": ("S", ("S",)),
    "Norm": ("S", ("V",)), "Recip": ("S", ("S",)),
}
REG_LIMIT = {"M": 4, "V": 6, "S": 4}


def check_space(prog: dict) -> tuple[bool, list[str]]:
    errs = []
    instrs = prog.get("instrs", [])
    if len(instrs) > 24:
        errs.append(f"len={len(instrs)} > 24")
    if prog.get("persist_m", 1) > 3:
        errs.append(f"persist_m={prog.get('persist_m')} > 3")
    if prog.get("persist_v", 0) != 0:
        errs.append(f"persist_v={prog.get('persist_v')} != 0")
    if prog.get("read") is not None:
        errs.append("evolved read program not allowed")
    for idx, ins in enumerate(instrs):
        op = ins["op"]
        if op not in ALLOWED_OPS:
            errs.append(f"instr {idx}: disallowed op {op}")
            continue
        ot, ins_t = OP_SIG[op]
        if not (0 <= ins["out"] < REG_LIMIT[ot]):
            errs.append(f"instr {idx}: out={ins['out']} out of range for {ot}")
        if len(ins_t) >= 1 and not (0 <= ins["a"] < REG_LIMIT[ins_t[0]]):
            errs.append(f"instr {idx}: a={ins['a']} out of range for {ins_t[0]}")
        if len(ins_t) >= 2 and not (0 <= ins["b"] < REG_LIMIT[ins_t[1]]):
            errs.append(f"instr {idx}: b={ins['b']} out of range for {ins_t[1]}")
    return len(errs) == 0, errs


def rust_eval(prog_path: str, regime: str = "collision3", task_seed: int | None = None,
              train_episodes: int | None = None, query_gap: int = 0) -> dict[str, float]:
    cmd = [str(EXE), "eval", "--prog", str(prog_path), "--regime", regime]
    if task_seed is not None:
        cmd += ["--task-seed", str(task_seed)]
    if train_episodes is not None:
        cmd += ["--train-episodes", str(train_episodes)]
    if query_gap > 0:
        cmd += ["--query-gap", str(query_gap)]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    res = {}
    for line in out.splitlines():
        m = re.match(r"^(train|test [^:]+):?\s+acc\s+([0-9.]+)", line)
        if m:
            res[m.group(1)] = float(m.group(2))
    return res


def jax_dump_check(prog: dict, dump_path: pathlib.Path, norm_eps: float) -> tuple[float, bool]:
    V.NORM_EPS = norm_eps
    tasks = V.load_task_json(str(dump_path))
    step = V.build_step(
        prog["instrs"],
        pm=prog.get("persist_m", 1),
        pv=prog.get("persist_v", 0),
        ident=bool(prog.get("persist_identity", 0)),
    )
    c = n = 0
    div = False
    for t in tasks:
        _, dv, ci, ni = V.accuracy_counts(step, t)
        c, n, div = c + ci, n + ni, div or dv
    return c / max(n, 1), div


def v3_stability_check(prog: dict, seed: int = 77777) -> dict[str, float | bool]:
    """v3 stability bound: 64 episodes x 256 write steps (K=8), all persistent entries < 100."""
    V.NORM_EPS = 1e-6
    pm = prog.get("persist_m", 1)
    pv = prog.get("persist_v", 0)
    ident = bool(prog.get("persist_identity", 0))
    step = V.build_step(prog["instrs"], pm=pm, pv=pv, ident=ident)
    init = getattr(step, "init", lambda d: jnp.zeros((d, d), dtype=jnp.float64))

    def max_entry(st):
        if pm > 1 or pv > 0:
            S, extra_m, extra_v = st
            mats = [S] + list(extra_m)
            vals = [jnp.where(jnp.all(jnp.isfinite(m)), jnp.max(jnp.abs(m)), jnp.inf) for m in mats]
            vals += [jnp.where(jnp.all(jnp.isfinite(v)), jnp.max(jnp.abs(v)), jnp.inf) for v in extra_v]
            return jnp.max(jnp.stack(vals))
        return jnp.where(jnp.all(jnp.isfinite(st)), jnp.max(jnp.abs(st)), jnp.inf)

    def run_cfg(cfg):
        rng = np.random.default_rng(seed)
        keys, vals, W, Q, Qm = V.make_task(rng, **cfg)
        d = keys.shape[1]

        def ep(w, q, qm):
            def body(carry, kv):
                st, mx = carry
                st = step(st, keys[kv[0]], vals[kv[1]])
                return (st, jnp.maximum(mx, max_entry(st))), None

            (st, mx), _ = jax.lax.scan(body, (init(d), jnp.float64(0.0)), w)
            S = st[0] if (pm > 1 or pv > 0) else st
            qk = keys[q[:, 0]]
            o = (S @ qk.T).T
            pred = jnp.argmax(o @ vals.T, axis=1)
            ok = (pred == q[:, 1]) & (jnp.linalg.norm(o, axis=1) > 1e-6) & jnp.all(jnp.isfinite(o), axis=1)
            return jnp.sum(ok & qm), jnp.sum(qm), mx

        c, n, mxs = jax.jit(jax.vmap(ep))(W, Q, Qm)
        return float(c.sum() / n.sum()), float(jnp.max(mxs))

    acc_std, mx_std = run_cfg(dict(d=16, n_keys=64, n_vals=64, T=256, p_ow=0.3, n_ep=64, max_keys=8))
    acc_col, mx_col = run_cfg(dict(d=16, n_keys=64, n_vals=64, T=256, p_ow=0.3, n_ep=64, max_keys=8, clusters=8, cluster_cos=0.85))
    mx = max(mx_std, mx_col)
    return {
        "t256_std_acc": acc_std,
        "t256_std_max": mx_std,
        "t256_col_acc": acc_col,
        "t256_col_max": mx_col,
        "stable_lt100": bool(np.isfinite(mx) and mx < 100.0),
    }


def audit_program(prog_path: str, run_draws: bool = False) -> dict:
    prog = json.loads(pathlib.Path(prog_path).read_text(encoding="utf-8"))
    space_ok, space_errs = check_space(prog)
    r = rust_eval(prog_path, regime="collision3")
    j_e6, j_div6 = jax_dump_check(prog, TEST_DUMP, norm_eps=1e-6)
    j_e9, j_div9 = jax_dump_check(prog, TEST_DUMP, norm_eps=1e-9)
    stab = v3_stability_check(prog)

    eps_ratio = None
    if abs(j_e6 - j_e9) > 0.02:
        out = subprocess.run(
            [sys.executable, str(ROOT / "verify" / "eps_scale.py"), "--task-json", str(TEST_DUMP), str(prog_path)],
            capture_output=True, text=True,
        ).stdout
        m = re.search(r"ratio\s+([0-9.eE+-]+)", out)
        if m:
            eps_ratio = float(m.group(1))

    p_res = pathlib.Path(prog_path).resolve()
    try:
        rel_path = p_res.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        rel_path = pathlib.Path(prog_path).as_posix()

    out = {
        "path": rel_path,
        "n_instrs": len(prog.get("instrs", [])),
        "persist_m": prog.get("persist_m", 1),
        "space_ok": space_ok,
        "space_errs": space_errs,
        "rust_train": r.get("train", 0.0),
        "rust_test_col3": r.get("test regime collision3", 0.0),
        "rust_d32": r.get("test d32 T24 ow0.3", 0.0),
        "rust_t64": r.get("test d16 T64 K8 ow0.3", 0.0),
        "rust_t128": r.get("test d16 T128 K8 ow0.3", 0.0),
        "jax_x64_e6": j_e6,
        "jax_x64_e9": j_e9,
        "jax_diff_rust": abs(j_e6 - r.get("test regime collision3", 0.0)),
        "eps_shift": abs(j_e6 - j_e9),
        "eps_ratio": eps_ratio,
        **stab,
    }
    if run_draws:
        d0 = [rust_eval(prog_path, "collision3", task_seed=s, train_episodes=512, query_gap=0)["train"] for s in range(101, 113)]
        d4 = [rust_eval(prog_path, "collision3", task_seed=s, train_episodes=512, query_gap=4)["train"] for s in range(101, 113)]
        out["draws_12_gap0"] = d0
        out["draws_12_gap0_mean"] = st.mean(d0)
        out["draws_12_gap4"] = d4
        out["draws_12_gap4_mean"] = st.mean(d4)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("progs", nargs="+")
    ap.add_argument("--draws", action="store_true")
    args = ap.parse_args()
    for p in args.progs:
        res = audit_program(p, run_draws=args.draws)
        print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()

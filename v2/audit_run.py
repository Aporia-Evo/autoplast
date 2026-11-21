"""Post-hoc hostile-reviewer audit for a completed v2 run directory.

Audits every seed's exported `best.json` via `v2/strict_eval.py`:
  - Exact search-space compliance (<= 24 instrs, NM=4, NV=6, NS=4, persist_m <= 3, 20 ops)
  - Exact Rust `autoplast eval --regime collision3` (with matching `--task-seed` for train)
  - Independent JAX float64 `norm_eps=1e-6` vs Rust and `norm_eps=1e-9` (+ eps_scale.py)
  - v3 stability bound across N draws (64 eps x 256 write steps, all persistent entries < 100)
  - 12 paired fresh draws (task seeds 101..112) at query_gap=0 and query_gap=4
  - Optional paired comparison against BPTT-tuned baselines (`v2/baselines_bptt/baselines_summary.json`).

Usage:
  python v2/audit_run.py v2/runs/frozen_memetic_v1/s501 [--train-task-seed 501] [--stab-draws 9] [--no-draws]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "v2"))

import strict_eval as SE  # noqa: E402


def is_valid_discovery(r: dict) -> tuple[bool, list[str]]:
    reasons = []
    if not r["space_ok"]:
        reasons.append(f"space:{','.join(r['space_errs'])}")
    if not r["stable_lt100"]:
        reasons.append(f"unstable(max={max(r['t256_std_max'], r['t256_col_max']):.2e})")
    if r["eps_shift"] > 0.02:
        reasons.append(f"eps_shift={r['eps_shift']:.3f}")
    if r["jax_diff_rust"] > 0.01:
        reasons.append(f"rust_jax_diff={r['jax_diff_rust']:.3f}")
    if r["rust_train"] - r["rust_test_col3"] > 0.03:
        reasons.append(f"overfit={r['rust_train'] - r['rust_test_col3']:.3f}")
    return len(reasons) == 0, reasons


def infer_train_task_seed(run_dir: pathlib.Path, seed_dir: pathlib.Path, explicit: int | None) -> int | None:
    if explicit is not None:
        return explicit
    sp = seed_dir / "summary.json"
    if sp.exists():
        try:
            meta = json.loads(sp.read_text(encoding="utf-8"))
            if isinstance(meta.get("task_seed"), int):
                return meta["task_seed"]
        except Exception:
            pass
    m = re.match(r"^s(\d+)$", run_dir.name)
    if m:
        return int(m.group(1))
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--no-draws", action="store_true")
    ap.add_argument("--train-task-seed", type=int, default=None)
    ap.add_argument("--stab-draws", type=int, default=9)
    args = ap.parse_args()

    run_dir = pathlib.Path(args.run_dir)
    seed_dirs = sorted(
        [d for d in run_dir.iterdir() if d.is_dir() and d.name.startswith("seed")],
        key=lambda d: int(d.name[4:]) if d.name[4:].isdigit() else 999999,
    )
    if not seed_dirs:
        print(f"No seed* directories found in {run_dir}")
        sys.exit(1)

    rows = []
    for sd in seed_dirs:
        jp = sd / "best.json"
        if not jp.exists():
            print(f"  {sd.name}: NO best.json (failed to compile)")
            rows.append({"seed": sd.name, "compiled": False, "valid": False, "reasons": ["no best.json"]})
            continue
        tts = infer_train_task_seed(run_dir, sd, args.train_task_seed)
        res = SE.audit_program(
            str(jp),
            run_draws=not args.no_draws,
            train_task_seed=tts,
            stab_draws=args.stab_draws,
        )
        ok, reasons = is_valid_discovery(res)
        res["seed"] = sd.name
        res["compiled"] = True
        res["valid"] = ok
        res["reasons"] = reasons
        rows.append(res)
        t256_mx = max(res["t256_std_max"], res["t256_col_max"])
        d_str = (
            f" 12d={res['draws_12_gap0_mean']:.3f} gap4={res['draws_12_gap4_mean']:.3f}"
            if "draws_12_gap0_mean" in res else ""
        )
        print(
            f"  {sd.name:6s} (ts={res['train_task_seed']}) | len={res['n_instrs']:2d} ok={str(res['space_ok']):5s} | "
            f"tr={res['rust_train']:.3f} te={res['rust_test_col3']:.3f} (e9={res['jax_x64_e9']:.3f}) | "
            f"d32={res['rust_d32']:.3f} T128={res['rust_t128']:.3f} T256({args.stab_draws}d)={t256_mx:.2f} |{d_str} | "
            f"VALID={ok} {reasons}",
            flush=True,
        )

    out_path = run_dir / "strict_audit.json"
    out_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    n_tot = len(rows)
    n_valid = sum(1 for r in rows if r.get("valid"))
    n_gt90 = sum(1 for r in rows if r.get("valid") and r["rust_test_col3"] > 0.90)
    print(f"\nSummary for {run_dir}: {n_valid}/{n_tot} strictly valid, {n_gt90}/{n_tot} valid & test_col3 > 0.90")

    bpath = ROOT / "v2" / "baselines_bptt" / "baselines_summary.json"
    if bpath.exists():
        bl = json.loads(bpath.read_text(encoding="utf-8"))
        stable_bl = [b for b in bl if b["stable_lt100"] and b["space_ok"]]
        if stable_bl:
            best_bl = max(stable_bl, key=lambda b: b["rust_test_col3"])
            print(
                f"Best stable BPTT baseline: {best_bl['family']} "
                f"(len={best_bl['n_instrs']}, test_col3={best_bl['rust_test_col3']:.3f}, "
                f"12draws={best_bl.get('draws_12_gap0_mean', 0):.3f})"
            )


if __name__ == "__main__":
    main()

"""Execute the pre-registered compute-fair 5-arm component ablation (`ablations_v31`, task seeds 701..708)
on frozen `Memetic MAP-Elites v3.1` at `--max-ep-evals 22000000`, then run strict post-hoc audits."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_V1_DIR = ROOT / "target" / "release"
V1_EXE = _V1_DIR / ("autoplast.exe" if (_V1_DIR / "autoplast.exe").exists() else "autoplast")
_V2_DIR = ROOT / "v2" / "memetic" / "target" / "release"
V2_EXE = _V2_DIR / ("autoplast_memetic.exe" if (_V2_DIR / "autoplast_memetic.exe").exists() else "autoplast_memetic")
PY = sys.executable

SEEDS = list(range(701, 709))  # 8 completely fresh unseen task seeds: 701..708
MAX_EP_EVALS = 22_000_000
DUMP_DIR = ROOT / "v2" / "data" / "seeds_701_708"
RUN_DIR = ROOT / "v2" / "runs" / "ablations_v31"

ARMS: dict[str, list[str]] = {
    "full": [],
    "no_const_tune": ["--no-const-tune"],
    "acc_fitness": ["--fitness", "acc"],
    "no_archive": ["--no-archive"],
    "basic_mut": ["--basic-mut"],
}


def ensure_dumps(task_seed: int) -> tuple[pathlib.Path, pathlib.Path]:
    DUMP_DIR.mkdir(parents=True, exist_ok=True)
    val_seed = 2000 + task_seed
    tr_path = DUMP_DIR / f"collision3_train_s{task_seed}.json"
    va_path = DUMP_DIR / f"collision3_val_s{val_seed}.json"
    if not tr_path.exists():
        subprocess.run(
            [
                str(V1_EXE), "dump",
                "--regime", "collision3",
                "--split", "train",
                "--task-seed", str(task_seed),
                "--out", str(tr_path),
            ],
            check=True,
        )
    if not va_path.exists():
        subprocess.run(
            [
                str(V1_EXE), "dump",
                "--regime", "collision3",
                "--split", "train",
                "--task-seed", str(val_seed),
                "--train-episodes", "192",
                "--out", str(va_path),
            ],
            check=True,
        )
    return tr_path, va_path


def run_one(arm: str, t: int, threads: int) -> tuple[str, int, str]:
    out_dir = RUN_DIR / arm / f"seed{t}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "meta.json").write_text(
        json.dumps(
            {"arm": arm, "task_seed": t, "val_task_seed": 2000 + t, "search_seed": t, "max_ep_evals": MAX_EP_EVALS},
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    if (out_dir / "best.json").exists() and (out_dir / "summary.json").exists():
        return arm, t, "skipped"
    tr, va = ensure_dumps(t)
    print(f"[START] {arm:13s} seed{t} (ts={t}, max_ep_evals={MAX_EP_EVALS}, threads={threads})", flush=True)
    cmd = [
        str(V2_EXE),
        "--seed", str(t),
        "--max-ep-evals", str(MAX_EP_EVALS),
        "--batch", "1024",
        "--threads", str(threads),
        "--st-l2", "0.015",
        "--train-dump", str(tr),
        "--val-dump", str(va),
        "--out", str(out_dir),
    ] + ARMS[arm]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    sm = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
    msg = (
        f"done in {sm['wall_seconds']:.1f}s | cands={sm['total_cands']} ep={sm['total_ep_evals']/1e6:.2f}M | "
        f"len={sm['n_instrs']} pm={sm['persist_m']} | tr={sm['train_acc']:.4f} val={sm['val_acc']:.4f} mx={sm['max_abs_state_val']:.2f}"
    )
    print(f"[DONE ] {arm:13s} seed{t}: {msg}", flush=True)
    return arm, t, msg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", nargs="*", default=None, choices=list(ARMS.keys()))
    ap.add_argument("--seeds", type=int, nargs="*", default=None)
    ap.add_argument("--parallel", type=int, default=2)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--no-audit", action="store_true")
    ap.add_argument("--audit-only", action="store_true")
    args = ap.parse_args()

    assert V1_EXE.exists(), f"Missing v1 binary: {V1_EXE}"
    assert V2_EXE.exists(), f"Missing frozen v3.1 binary: {V2_EXE}"
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    target_arms = args.arms if args.arms else list(ARMS.keys())
    target_seeds = args.seeds if args.seeds else SEEDS

    if not args.audit_only:
        for t in target_seeds:
            ensure_dumps(t)
        jobs = [(arm, t) for arm in target_arms for t in target_seeds]
        if args.parallel <= 1:
            for arm, t in jobs:
                run_one(arm, t, args.threads)
        else:
            with ThreadPoolExecutor(max_workers=args.parallel) as ex:
                futs = [ex.submit(run_one, arm, t, args.threads) for arm, t in jobs]
                for f in as_completed(futs):
                    f.result()

    if not args.no_audit:
        for arm in target_arms:
            arm_dir = RUN_DIR / arm
            print(f"\n================ STRICT AUDIT | arm={arm} ({arm_dir}) ================", flush=True)
            subprocess.run([PY, "-u", str(ROOT / "v2" / "audit_run.py"), str(arm_dir)], check=True)


if __name__ == "__main__":
    main()

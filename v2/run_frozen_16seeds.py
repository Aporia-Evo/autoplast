"""Execute the pre-registered 16-seed unseen-task evaluation (`frozen_16seeds`, task seeds 601..616)
using the strictly frozen `autoplast_memetic` binary, then run the full post-hoc strict audit."""

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

SEEDS = list(range(601, 617))  # 16 completely fresh unseen task seeds: 601..616
DUMP_DIR = ROOT / "v2" / "data" / "seeds_601_616"
RUN_DIR = ROOT / "v2" / "runs" / "frozen_16seeds"


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


def run_one_seed(t: int, threads: int) -> tuple[int, str]:
    out_dir = RUN_DIR / f"seed{t}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "meta.json").write_text(
        json.dumps({"task_seed": t, "val_task_seed": 2000 + t, "search_seed": t}, indent=2) + "\n",
        encoding="utf-8",
    )
    if (out_dir / "best.json").exists() and (out_dir / "summary.json").exists():
        return t, "skipped"
    tr, va = ensure_dumps(t)
    print(
        f"[START] seed{t} (task_seed={t}, val_seed={2000+t}, threads={threads})",
        flush=True,
    )
    subprocess.run(
        [
            str(V2_EXE),
            "--seed", str(t),
            "--max-cands", "300000",
            "--batch", "1024",
            "--threads", str(threads),
            "--st-l2", "0.015",
            "--train-dump", str(tr),
            "--val-dump", str(va),
            "--out", str(out_dir),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    sm = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
    msg = (
        f"done in {sm['wall_seconds']:.1f}s | len={sm['n_instrs']} pm={sm['persist_m']} | "
        f"tr={sm['train_acc']:.4f} val={sm['val_acc']:.4f} mx={sm['max_abs_state_val']:.2f} | "
        f"ep_evals={sm.get('total_ep_evals', 0)}"
    )
    print(f"[DONE ] seed{t}: {msg}", flush=True)
    return t, msg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="*", default=None, help="Subset of seeds (default: all 601..616)")
    ap.add_argument("--parallel", type=int, default=2, help="Concurrent seeds (v3.1 is thread-count bit-deterministic)")
    ap.add_argument("--threads", type=int, default=8, help="Threads per seed (default: 8 with --parallel 2)")
    ap.add_argument("--no-audit", action="store_true", help="Skip post-hoc audit step")
    ap.add_argument("--audit-only", action="store_true", help="Only run post-hoc strict audit")
    args = ap.parse_args()

    assert V1_EXE.exists(), f"Missing v1 binary: {V1_EXE}"
    assert V2_EXE.exists(), f"Missing frozen v2 binary: {V2_EXE}"
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    target_seeds = args.seeds if args.seeds else SEEDS
    if not args.audit_only:
        # Pre-generate dumps sequentially so v1 autoplast never contends on files
        for t in target_seeds:
            ensure_dumps(t)
        if args.parallel <= 1:
            for t in target_seeds:
                run_one_seed(t, args.threads)
        else:
            with ThreadPoolExecutor(max_workers=args.parallel) as ex:
                futs = [ex.submit(run_one_seed, t, args.threads) for t in target_seeds]
                for f in as_completed(futs):
                    f.result()

    if not args.no_audit:
        print("\n================ POST-HOC STRICT AUDIT (FROZEN 16 SEEDS v3.1: 601..616) ================", flush=True)
        subprocess.run(
            [PY, "-u", str(ROOT / "v2" / "audit_run.py"), str(RUN_DIR)],
            check=True,
        )


if __name__ == "__main__":
    main()

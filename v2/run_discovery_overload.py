"""Execute the pre-registered Experiment 2a (discovery on overload and overload48)
with the frozen Memetic MAP-Elites v3.1 (--no-const-tune) method at
--max-ep-evals 22000000 --batch 1024 --st-l2 0.015, and record the exact
`autoplast eval --prog best.json --regime R --task-seed t` output per seed.

Facts only: counting, fresh draws, JAX and the long probe are done in the repository.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import pathlib
import queue
import subprocess
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
_V1_DIR = ROOT / "target" / "release"
V1_EXE = _V1_DIR / ("autoplast.exe" if (_V1_DIR / "autoplast.exe").exists() else "autoplast")
_V2_DIR = ROOT / "v2" / "memetic" / "target" / "release"
V2_EXE = _V2_DIR / ("autoplast_memetic.exe" if (_V2_DIR / "autoplast_memetic.exe").exists() else "autoplast_memetic")

REGIMES = {
    "overload": list(range(1001, 1017)),
    "overload48": list(range(1101, 1117)),
}
MAX_EP_EVALS = 22_000_000
RUN_DIR = ROOT / "v2" / "runs" / "discovery_overload"
DUMP_DIR = RUN_DIR / "dumps"


def is_seed_done(regime: str, t: int) -> bool:
    sd = RUN_DIR / regime / f"seed{t}"
    return (
        (sd / "best.json").exists()
        and (sd / "summary.json").exists()
        and (sd / "eval.txt").exists()
    )


def ensure_dumps(regime: str, t: int) -> tuple[pathlib.Path, pathlib.Path]:
    DUMP_DIR.mkdir(parents=True, exist_ok=True)
    val_seed = 2000 + t
    tr_path = DUMP_DIR / f"{regime}_train_s{t}.json"
    va_path = DUMP_DIR / f"{regime}_val_s{val_seed}.json"
    if not tr_path.exists():
        subprocess.run(
            [str(V1_EXE), "dump", "--regime", regime, "--split", "train",
             "--task-seed", str(t), "--out", str(tr_path)],
            check=True, stdout=subprocess.DEVNULL,
        )
    if not va_path.exists():
        subprocess.run(
            [str(V1_EXE), "dump", "--regime", regime, "--split", "train",
             "--task-seed", str(val_seed), "--train-episodes", "192", "--out", str(va_path)],
            check=True, stdout=subprocess.DEVNULL,
        )
    return tr_path, va_path


def run_eval(regime: str, t: int) -> None:
    seed_dir = RUN_DIR / regime / f"seed{t}"
    eval_path = seed_dir / "eval.txt"
    if eval_path.exists():
        return
    res = subprocess.run(
        [str(V1_EXE), "eval", "--prog", "best.json", "--regime", regime, "--task-seed", str(t)],
        cwd=str(seed_dir), check=True, capture_output=True, text=True,
    )
    eval_path.write_text(res.stdout, encoding="utf-8")


def run_one(
    regime: str,
    t: int,
    threads: int,
    slice_secs: float,
    ckpt_dir: pathlib.Path,
) -> tuple[str, int, str]:
    seed_dir = RUN_DIR / regime / f"seed{t}"
    seed_dir.mkdir(parents=True, exist_ok=True)
    tr_path, va_path = ensure_dumps(regime, t)
    ckpt = ckpt_dir / f"autoplast_{regime}_seed{t}.ckpt"

    if not ((seed_dir / "best.json").exists() and (seed_dir / "summary.json").exists()):
        print(f"[START] {regime}/seed{t} (threads={threads}, slice={slice_secs:.0f}s)", flush=True)
        cmd = [
            str(V2_EXE),
            "--seed", str(t),
            "--no-const-tune",
            "--max-ep-evals", str(MAX_EP_EVALS),
            "--batch", "1024",
            "--threads", str(threads),
            "--st-l2", "0.015",
            "--train-dump", str(tr_path),
            "--val-dump", str(va_path),
            "--out", str(seed_dir),
        ]
        if slice_secs > 0.0:
            ckpt_dir.mkdir(parents=True, exist_ok=True)
            cmd += ["--checkpoint", str(ckpt), "--slice-secs", f"{slice_secs:.1f}"]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
            if proc.returncode == 75:
                lines = [ln for ln in proc.stdout.splitlines() if "CHECKPOINT" in ln or "RESUMED" in ln]
                print(f"[CKPT ] {regime}/seed{t}: {lines[-1] if lines else 'checkpointed'}", flush=True)
                return regime, t, "paused"
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(proc.returncode, cmd, output=proc.stdout)
        else:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(proc.returncode, cmd, output=proc.stdout)

    ckpt.unlink(missing_ok=True)
    run_eval(regime, t)
    sm = json.loads((seed_dir / "summary.json").read_text(encoding="utf-8"))
    msg = (
        f"wall={sm['wall_seconds']:.1f}s cands={sm['total_cands']} ep={sm['total_ep_evals']/1e6:.2f}M "
        f"len={sm['n_instrs']} tr_acc={sm['train_acc']:.4f} val_acc={sm['val_acc']:.4f}"
    )
    print(f"[DONE ] {regime}/seed{t}: {msg}", flush=True)
    return regime, t, "done"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--regime", choices=sorted(REGIMES), action="append", default=None)
    ap.add_argument("--seeds", type=int, nargs="*", default=None)
    ap.add_argument("--parallel", type=int, default=2)
    ap.add_argument("--threads", type=int, default=1)
    ap.add_argument("--slice-secs", type=float, default=0.0)
    ap.add_argument("--wall-budget", type=float, default=0.0,
                    help="Stop launching/slicing once wall-budget seconds have elapsed in this invocation.")
    ap.add_argument("--ckpt-dir", type=pathlib.Path, default=pathlib.Path(tempfile.gettempdir()))
    ap.add_argument("--dumps-only", action="store_true")
    args = ap.parse_args()

    assert V1_EXE.exists(), f"Missing v1 binary: {V1_EXE}"
    assert V2_EXE.exists(), f"Missing v2 binary: {V2_EXE}"
    all_jobs = []
    for regime in (args.regime or list(REGIMES)):
        for t in REGIMES[regime]:
            if args.seeds and t not in args.seeds:
                continue
            all_jobs.append((regime, t))

    if args.dumps_only:
        for regime, t in all_jobs:
            ensure_dumps(regime, t)
        print(f"dumps ready for {len(all_jobs)} seeds", flush=True)
        return

    pending = [(r, t) for r, t in all_jobs if not is_seed_done(r, t)]
    done_before = len(all_jobs) - len(pending)
    print(f"[QUEUE] {done_before}/{len(all_jobs)} already done, {len(pending)} pending", flush=True)
    if not pending:
        return

    if args.wall_budget > 0.0:
        deadline = time.monotonic() + args.wall_budget
        q: queue.Queue[tuple[str, int]] = queue.Queue()
        for item in pending:
            q.put(item)

        eff_workers = min(args.parallel, len(pending))
        eff_threads = args.threads if len(pending) > 1 else max(args.threads, args.parallel)

        def worker() -> None:
            while True:
                rem = deadline - time.monotonic()
                if rem < 30.0:
                    return
                try:
                    r, t = q.get_nowait()
                except queue.Empty:
                    return
                sl = min(args.slice_secs, rem) if args.slice_secs > 0.0 else rem
                run_one(r, t, eff_threads, sl, args.ckpt_dir)

        with ThreadPoolExecutor(max_workers=eff_workers) as ex:
            futs = [ex.submit(worker) for _ in range(eff_workers)]
            for f in as_completed(futs):
                f.result()
    elif args.parallel <= 1:
        for regime, t in pending:
            run_one(regime, t, args.threads, args.slice_secs, args.ckpt_dir)
    else:
        with ThreadPoolExecutor(max_workers=args.parallel) as ex:
            futs = [ex.submit(run_one, r, t, args.threads, args.slice_secs, args.ckpt_dir) for r, t in pending]
            for f in as_completed(futs):
                f.result()

    still_pending = sum(1 for r, t in all_jobs if not is_seed_done(r, t))
    print(f"[SUMMARY] {len(all_jobs) - still_pending}/{len(all_jobs)} completed, {still_pending} remaining", flush=True)


if __name__ == "__main__":
    main()

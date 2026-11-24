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
import subprocess
import sys
import tempfile

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


def run_one(regime: str, t: int, threads: int, slice_secs: float) -> tuple[str, int, str]:
    seed_dir = RUN_DIR / regime / f"seed{t}"
    seed_dir.mkdir(parents=True, exist_ok=True)
    tr_path, va_path = ensure_dumps(regime, t)

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
            ckpt = pathlib.Path(tempfile.gettempdir()) / f"autoplast_{regime}_seed{t}.ckpt"
            cmd += ["--checkpoint", str(ckpt), "--slice-secs", str(slice_secs)]
        while True:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
            if proc.returncode != 75:
                break
            lines = [ln for ln in proc.stdout.splitlines() if "CHECKPOINT" in ln or "RESUMED" in ln]
            print(f"[CKPT ] {regime}/seed{t}: {lines[-1] if lines else 'checkpointed'}", flush=True)
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, cmd, output=proc.stdout)

    run_eval(regime, t)
    sm = json.loads((seed_dir / "summary.json").read_text(encoding="utf-8"))
    msg = (
        f"wall={sm['wall_seconds']:.1f}s cands={sm['total_cands']} ep={sm['total_ep_evals']/1e6:.2f}M "
        f"len={sm['n_instrs']}"
    )
    print(f"[DONE ] {regime}/seed{t}: {msg}", flush=True)
    return regime, t, msg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--regime", choices=sorted(REGIMES), action="append", default=None)
    ap.add_argument("--seeds", type=int, nargs="*", default=None)
    ap.add_argument("--parallel", type=int, default=2)
    ap.add_argument("--threads", type=int, default=1)
    ap.add_argument("--slice-secs", type=float, default=0.0)
    ap.add_argument("--dumps-only", action="store_true")
    args = ap.parse_args()

    assert V1_EXE.exists(), f"Missing v1 binary: {V1_EXE}"
    assert V2_EXE.exists(), f"Missing v2 binary: {V2_EXE}"
    jobs = []
    for regime in (args.regime or list(REGIMES)):
        for t in REGIMES[regime]:
            if args.seeds and t not in args.seeds:
                continue
            jobs.append((regime, t))

    if args.dumps_only:
        for regime, t in jobs:
            ensure_dumps(regime, t)
        print(f"dumps ready for {len(jobs)} seeds", flush=True)
        return

    if args.parallel <= 1:
        for regime, t in jobs:
            run_one(regime, t, args.threads, args.slice_secs)
    else:
        with ThreadPoolExecutor(max_workers=args.parallel) as ex:
            futs = [ex.submit(run_one, r, t, args.threads, args.slice_secs) for r, t in jobs]
            for f in as_completed(futs):
                f.result()


if __name__ == "__main__":
    main()

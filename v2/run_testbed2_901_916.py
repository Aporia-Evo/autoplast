"""Execute the pre-registered Testbed 2 counted run (task seeds 901..916)
using the frozen Memetic MAP-Elites v3.1 (--no-const-tune) method at
--max-ep-evals 22000000 --batch 1024 --st-l2 0.015, and record exact
autoplast eval and verify/opt_structure.py outputs per seed.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
_V1_DIR = ROOT / "target" / "release"
V1_EXE = _V1_DIR / ("autoplast.exe" if (_V1_DIR / "autoplast.exe").exists() else "autoplast")
_V2_DIR = ROOT / "v2" / "memetic" / "target" / "release"
V2_EXE = _V2_DIR / ("autoplast_memetic.exe" if (_V2_DIR / "autoplast_memetic.exe").exists() else "autoplast_memetic")
PY = sys.executable

SEEDS = list(range(901, 917))
MAX_EP_EVALS = 22_000_000
RUN_DIR = ROOT / "v2" / "runs" / "testbed2_901_916"
DUMP_DIR = RUN_DIR / "dumps"


def ensure_dumps(t: int) -> tuple[pathlib.Path, pathlib.Path]:
    DUMP_DIR.mkdir(parents=True, exist_ok=True)
    val_seed = 2000 + t
    tr_path = DUMP_DIR / f"opt_train_s{t}.json"
    va_path = DUMP_DIR / f"opt_val_s{val_seed}.json"
    if not tr_path.exists():
        subprocess.run(
            [
                str(V1_EXE), "dump",
                "--task", "opt",
                "--split", "train",
                "--task-seed", str(t),
                "--out", str(tr_path),
            ],
            check=True,
        )
    if not va_path.exists():
        subprocess.run(
            [
                str(V1_EXE), "dump",
                "--task", "opt",
                "--split", "train",
                "--task-seed", str(val_seed),
                "--train-episodes", "192",
                "--out", str(va_path),
            ],
            check=True,
        )
    return tr_path, va_path


def run_eval_and_structure(t: int) -> None:
    seed_dir = RUN_DIR / f"seed{t}"
    tr_path = DUMP_DIR / f"opt_train_s{t}.json"
    eval_path = seed_dir / "eval.txt"
    struct_path = seed_dir / "structure.txt"

    if not eval_path.exists():
        res = subprocess.run(
            [
                str(V1_EXE), "eval",
                "--task", "opt",
                "--opt-ops",
                "--prog", "best.json",
                "--task-seed", str(t),
            ],
            cwd=str(seed_dir),
            check=True,
            capture_output=True,
            text=True,
        )
        eval_path.write_text(res.stdout, encoding="utf-8")

    if not struct_path.exists():
        res = subprocess.run(
            [
                PY,
                str(ROOT / "verify" / "opt_structure.py"),
                "--task-json", str(tr_path),
                "best.json",
            ],
            cwd=str(seed_dir),
            check=True,
            capture_output=True,
            text=True,
        )
        struct_path.write_text(res.stdout, encoding="utf-8")


def run_one(t: int, threads: int, slice_secs: float = 0.0) -> tuple[int, str]:
    seed_dir = RUN_DIR / f"seed{t}"
    seed_dir.mkdir(parents=True, exist_ok=True)
    tr_path, va_path = ensure_dumps(t)

    if not ((seed_dir / "best.json").exists() and (seed_dir / "summary.json").exists()):
        print(f"[START] seed{t} (ts={t}, max_ep_evals={MAX_EP_EVALS}, threads={threads}, slice={slice_secs:.0f}s)", flush=True)
        cmd = [
            str(V2_EXE),
            "--task", "opt",
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
            ckpt = pathlib.Path(tempfile.gettempdir()) / f"autoplast_opt_seed{t}.ckpt"
            cmd += ["--checkpoint", str(ckpt), "--slice-secs", str(slice_secs)]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        if proc.returncode == 75:
            last_line = [ln for ln in proc.stdout.splitlines() if "CHECKPOINT" in ln or "RESUMED" in ln]
            msg = last_line[-1] if last_line else "checkpointed"
            print(f"[PAUSE] seed{t}: {msg}", flush=True)
            return t, "paused"
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, cmd, output=proc.stdout)

    run_eval_and_structure(t)
    sm = json.loads((seed_dir / "summary.json").read_text(encoding="utf-8"))
    msg = (
        f"wall={sm['wall_seconds']:.1f}s cands={sm['total_cands']} ep={sm['total_ep_evals']/1e6:.2f}M "
        f"len={sm['n_instrs']} pv={sm['persist_v']} tr_raw={sm['train_raw_obj']:.4f} val_raw={sm['val_raw_obj']:.4f}"
    )
    print(f"[DONE ] seed{t}: {msg}", flush=True)
    return t, msg


def parse_eval_txt(text: str) -> dict[str, tuple[float, float, float]]:
    out: dict[str, tuple[float, float, float]] = {}
    m_tr = re.search(r"train objective ([\-\d\.]+)\s+diverged ([\-\d\.]+)\s+max_state ([\-\d\.infnan]+)", text)
    if m_tr:
        out["train"] = (float(m_tr.group(1)), float(m_tr.group(2)), float(m_tr.group(3)))
    for line in text.splitlines():
        m = re.match(r"^(test opt [^:]+): objective ([\-\d\.]+)\s+diverged ([\-\d\.]+)\s+max_state ([\-\d\.infnan]+)", line)
        if m:
            out[m.group(1)] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))
    return out


def parse_structure_txt(text: str) -> str:
    line = text.strip().splitlines()[0] if text.strip() else ""
    m = re.match(r"^[^:]+:\s+(\S+)", line)
    return m.group(1) if m else "unknown"


def write_report(seeds: list[int]) -> None:
    suite_keys = [
        ("test opt train-distribution", "Suite 1"),
        ("test opt kappa1000", "κ=1000"),
        ("test opt d32", "d=32"),
        ("test opt d8", "d=8"),
        ("test opt sigma0.3", "σ=0.3"),
        ("test opt T200", "T=200"),
        ("test opt scale10/0.1", "scale"),
    ]
    rows = []
    adam_seeds: list[str] = []
    signed_only_seeds: list[str] = []
    raw_s1_count = 0
    class_counts: dict[str, int] = {}
    for t in seeds:
        seed_dir = RUN_DIR / f"seed{t}"
        if not ((seed_dir / "summary.json").exists() and (seed_dir / "eval.txt").exists() and (seed_dir / "structure.txt").exists()):
            continue
        sm = json.loads((seed_dir / "summary.json").read_text(encoding="utf-8"))
        ev = parse_eval_txt((seed_dir / "eval.txt").read_text(encoding="utf-8"))
        cls = parse_structure_txt((seed_dir / "structure.txt").read_text(encoding="utf-8"))
        class_counts[cls] = class_counts.get(cls, 0) + 1
        tr_obj, tr_div, _ = ev["train"]
        s1_obj, s1_div, _ = ev["test opt train-distribution"]
        max_div = max(ev[k][1] for k, _ in suite_keys)
        gap = tr_obj - s1_obj
        if s1_obj <= -3.023:
            raw_s1_count += 1
        passes = (s1_obj <= -3.023) and (max_div == 0.0) and (abs(gap) <= 0.1)
        if passes:
            adam_seeds.append(f"seed{t}")
        elif (s1_obj <= -3.023) and (max_div == 0.0) and (gap <= 0.1):
            signed_only_seeds.append(f"seed{t} (tr - S1 = {gap:+.3f})")
        live_str = "".join(
            lbl for flag, lbl in [(sm["live_m0"], "M0"), (sm["live_v2"], "V2"), (sm["live_v3"], "V3")] if flag
        ) or "-"
        suite_cells = " | ".join(
            f"{ev[k][0]:.3f}" + (f" (d={ev[k][1]:.3f})" if ev[k][1] > 0 else "")
            for k, _ in suite_keys
        )
        rows.append(
            f"| `seed{t}` | {sm['n_instrs']} | {live_str} | {sm['total_ep_evals']/1e6:.2f}M | "
            f"{tr_obj:.3f} | {suite_cells} | {gap:+.3f} | {cls} | {'**Yes**' if passes else 'No'} |"
        )

    signed_count = len(adam_seeds) + len(signed_only_seeds)
    signed_note = (
        f"; `{signed_count}/{len(rows)}` under literal signed `tr - S1 <= 0.1` including " + ", ".join(signed_only_seeds)
        if signed_only_seeds
        else ""
    )
    adam_list = ", ".join(adam_seeds) if adam_seeds else "none"
    lines = [
        "# Testbed 2 Counted Run Report (`testbed2_901_916`)",
        "",
        "Frozen method: `Memetic MAP-Elites v3.1` (`--task opt --no-const-tune --max-ep-evals 22000000 --batch 1024 --st-l2 0.015`).",
        "All suite numbers are produced by `autoplast eval --task opt --opt-ops --prog best.json --task-seed t` and structural classes by `verify/opt_structure.py`.",
        "",
        "Adam-level criterion: `Suite 1 <= -3.023`, `0` divergence on all 7 suites (including `T=200` and `scale`), and `|train - Suite 1| <= 0.1`.",
        "",
        "| Seed | Instrs | Live | `ep_evals` | `train` | `Suite 1` | `κ=1000` | `d=32` | `d=8` | `σ=0.3` | `T=200` | `scale` | `tr - S1` | Class | Adam-lvl |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ] + rows + [
        "",
        f"- **Adam-level count (strict `|tr - S1| <= 0.1`):** **{len(adam_seeds)}/{len(rows)}** (`{adam_list}`{signed_note})",
        f"- **Raw `Suite 1 <= -3.023`:** **{raw_s1_count}/{len(rows)}**",
        "- **Structural classes:** " + ", ".join(f"`{k}`: {v}" for k, v in sorted(class_counts.items())),
        "",
    ]
    (RUN_DIR / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="*", default=None)
    ap.add_argument("--parallel", type=int, default=2)
    ap.add_argument("--threads", type=int, default=1)
    ap.add_argument("--slice-secs", type=float, default=0.0)
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()

    assert V1_EXE.exists(), f"Missing v1 binary: {V1_EXE}"
    assert V2_EXE.exists(), f"Missing v2 binary: {V2_EXE}"
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    target_seeds = args.seeds if args.seeds else SEEDS

    if not args.report_only:
        if args.parallel <= 1:
            for t in target_seeds:
                run_one(t, args.threads, args.slice_secs)
        else:
            with ThreadPoolExecutor(max_workers=args.parallel) as ex:
                futs = [ex.submit(run_one, t, args.threads, args.slice_secs) for t in target_seeds]
                for f in as_completed(futs):
                    f.result()

    write_report(SEEDS)


if __name__ == "__main__":
    main()

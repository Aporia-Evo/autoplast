"""Execute the pre-registered Phase 2 frozen evaluation (`frozen_memetic_v1`) and post-hoc audit."""

from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_BIN_DIR = ROOT / "v2" / "memetic" / "target" / "release"
EXE = _BIN_DIR / ("autoplast_memetic.exe" if (_BIN_DIR / "autoplast_memetic.exe").exists() else "autoplast_memetic")
PY = sys.executable

ARMS = [
    ("s1", ROOT / "v2/data/collision3_train_s1.json", ROOT / "v2/data/collision3_val_s2001.json", [10, 11, 12, 13]),
    ("s501", ROOT / "v2/data/collision3_train_s501.json", ROOT / "v2/data/collision3_val_s2501.json", [100, 101, 102, 103]),
]


def main():
    for arm_name, tr, va, seeds in ARMS:
        arm_dir = ROOT / "v2" / "runs" / "frozen_memetic_v1" / arm_name
        arm_dir.mkdir(parents=True, exist_ok=True)
        for seed in seeds:
            out_dir = arm_dir / f"seed{seed}"
            print(f"\n================ FROZEN PHASE 2 | arm={arm_name} seed={seed} ================", flush=True)
            subprocess.run(
                [
                    str(EXE),
                    "--seed", str(seed),
                    "--max-cands", "300000",
                    "--batch", "1024",
                    "--threads", "16",
                    "--st-l2", "0.015",
                    "--train-dump", str(tr),
                    "--val-dump", str(va),
                    "--out", str(out_dir),
                ],
                check=True,
            )

    print("\n================ POST-HOC STRICT AUDIT (FROZEN PHASE 2) ================", flush=True)
    for arm_name, _, _, _ in ARMS:
        arm_dir = ROOT / "v2" / "runs" / "frozen_memetic_v1" / arm_name
        print(f"\n--- Auditing arm={arm_name} ({arm_dir}) ---", flush=True)
        subprocess.run([PY, "-u", str(ROOT / "v2" / "audit_run.py"), str(arm_dir)], check=True)


if __name__ == "__main__":
    main()

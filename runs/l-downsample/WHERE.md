# l-downsample: where it ran

All 32 seeds on the workstation (AMD Ryzen 7 5700G, 8 cores / 16 threads, Windows, native build with cargo --release, MSVC), 19 Nov 2026,
commit 6c2f60a, 2 seeds at a time x 8 threads:

    python local_runner.py --seeds 1-32 --budget 1500000 --tag l-downsample --parallel 2 --threads 8 --extra="--select downsample --val-log --commit 6c2f60a"

No seed failed, none was rerun. Total wall 6815 s. Runner log: runner_log_workstation.txt.
Self-checks before the run on the workstation: package F row `120052,22831,29.7,0.82164,0.8142,4,0.7183`;
d-kalman seed 9 row 50036 `50036,19779,46.5,0.50570,0.5094,12,0.3803` (Linux: real evaluations 19778; accuracies identical).
verify.py ran on the workstation (JAX on CPU) -> verify.txt.

| seed | minutes |
|---|---|
| 1 | 8.4 |
| 2 | 6.4 |
| 3 | 11.3 |
| 4 | 7.2 |
| 5 | 5.0 |
| 6 | 2.7 |
| 7 | 4.3 |
| 8 | 6.8 |
| 9 | 24.2 |
| 10 | 19.1 |
| 11 | 3.0 |
| 12 | 8.9 |
| 13 | 9.5 |
| 14 | 4.1 |
| 15 | 6.9 |
| 16 | 7.3 |
| 17 | 3.0 |
| 18 | 3.4 |
| 19 | 4.6 |
| 20 | 2.9 |
| 21 | 4.8 |
| 22 | 2.8 |
| 23 | 9.5 |
| 24 | 6.9 |
| 25 | 9.5 |
| 26 | 7.6 |
| 27 | 2.7 |
| 28 | 3.4 |
| 29 | 9.5 |
| 30 | 7.1 |
| 31 | 5.4 |
| 32 | 6.3 |

# i-base4m: where it ran

All 32 seeds ran on epyc (16 cores, 1 thread per core), 16 Nov 2026, about 10:05 to 14:54 UTC, under nice -n 10, with a keepalive kernel,
after the rerun of h-share seed 16. None on workstation or modal. No seed failed, none was rerun.
The JupyterHub server was found stopped later in the day, after the marker had been written.

Binary: commit 50c2d10, uploaded as the commit tarball (no .git, tree checked blob by blob 2618/2618), built with cargo 1.99.1 --release.
Self-check of F repeated: 120052,22831,28.9,0.82164,0.8142,4,0.7183 (matches).
Command (RUNBOOK.md, package I), commit passed through --extra because the tree has no .git:

    python local_runner.py --seeds 1-32 --budget 4000000 --tag i-base4m --parallel 2 --threads 8 --extra="--val-log --commit 50c2d10"

verify.py ran on workstation (JAX on CPU) at the same commit -> verify.txt. Runner log: runner_log_epyc.txt.

Total wall 17485 s.

| seed | minutes |
|---|---|
| 1 | 5.2 |
| 2 | 7.5 |
| 3 | 10.8 |
| 4 | 7.8 |
| 5 | 10.1 |
| 6 | 9.6 |
| 7 | 18.4 |
| 8 | 11.9 |
| 9 | 12.3 |
| 10 | 5.2 |
| 11 | 44.9 |
| 12 | 40.4 |
| 13 | 5.0 |
| 14 | 33.6 |
| 15 | 51.0 |
| 16 | 11.1 |
| 17 | 7.4 |
| 18 | 8.5 |
| 19 | 33.8 |
| 20 | 8.3 |
| 21 | 12.8 |
| 22 | 7.5 |
| 23 | 5.5 |
| 24 | 20.3 |
| 25 | 7.1 |
| 26 | 37.3 |
| 27 | 15.9 |
| 28 | 40.4 |
| 29 | 9.9 |
| 30 | 15.7 |
| 31 | 35.8 |
| 32 | 13.6 |

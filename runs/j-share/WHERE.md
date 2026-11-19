# j-share: where it ran

All 32 seeds ran on epyc (16 cores, 1 thread per core), started on 18 Nov 2026 right after j-lexicase (about 04:00 UTC), 48366 s,
under nice -n 10, with a keepalive kernel. None on workstation or modal. No seed failed, none was rerun.
The JupyterHub server was stopped by the executing agent after the results had been fetched (19 Nov 2026).

Binary: commit 50c2d10, the build of package I (tree checked blob by blob 2618/2618; self-check of F matched). No change under src/
up to 4308a1e. Command (RUNBOOK.md, package J), commit passed through --extra because the tree has no .git:

    python local_runner.py --seeds 1-32 --budget 1500000 --tag j-share --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --select share --val-log --level-acc 0.651 --level-long 0.838 --commit 50c2d10"

Timing (tag time-j-share, not committed), 150,000 candidates: 183 s and 320 s per seed; projection 22 h for 32 seeds.
Dump made with the epyc binary; verify.py --task-json ran on workstation (JAX on CPU) at the same commit -> verify_dump.txt; the dump was
deleted on both machines. Runner log: runner_log_epyc.txt.

Total wall 48366 s.

| seed | minutes |
|---|---|
| 1 | 46.9 |
| 2 | 46.5 |
| 3 | 48.8 |
| 4 | 46.2 |
| 5 | 75.7 |
| 6 | 50.2 |
| 7 | 39.7 |
| 8 | 52.9 |
| 9 | 46.2 |
| 10 | 76.3 |
| 11 | 43.6 |
| 12 | 44.0 |
| 13 | 52.5 |
| 14 | 44.9 |
| 15 | 36.6 |
| 16 | 49.1 |
| 17 | 74.3 |
| 18 | 53.4 |
| 19 | 39.2 |
| 20 | 43.9 |
| 21 | 47.2 |
| 22 | 40.6 |
| 23 | 78.5 |
| 24 | 49.6 |
| 25 | 40.0 |
| 26 | 44.0 |
| 27 | 49.6 |
| 28 | 41.3 |
| 29 | 43.3 |
| 30 | 54.8 |
| 31 | 42.7 |
| 32 | 39.6 |

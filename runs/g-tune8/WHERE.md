# g-tune8: where it ran

All 32 seeds ran on epyc (16 cores, 1 thread per core), 14 Nov 2026 22:47 UTC to 15 Nov 2026 about 10:45 UTC, under nice -n 10,
with a keepalive kernel for the JupyterHub server. None on workstation or modal. No seed failed, none was rerun.
The JupyterHub server was found stopped after the run had finished (marker present, all 32 summaries written).

Binary: commit ad31161, the same build on epyc as package H (tree checked blob by blob 1826/1826; self-check of F matched).
Command (RUNBOOK.md, package G), commit passed through --extra because the tree has no .git:

    python local_runner.py --seeds 1-32 --budget 1500000 --tag g-tune8 --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --tune-consts 8 --val-log --level-acc 0.651 --level-long 0.838 --commit ad31161"

Timing (tag time-g, not committed), 150,000 candidates: seed 1 97 s, seed 2 327 s; projection 18.8 h for 32 seeds.
Dump made with the epyc binary; verify.py --task-json ran on workstation (JAX on CPU) at the same commit -> verify_dump.txt;
the dump was deleted on both machines. Runner log: runner_log_epyc.txt.

Total wall 43041 s.

| seed | minutes |
|---|---|
| 1 | 46.6 |
| 2 | 55.0 |
| 3 | 81.5 |
| 4 | 49.9 |
| 5 | 32.2 |
| 6 | 72.6 |
| 7 | 41.7 |
| 8 | 86.0 |
| 9 | 41.2 |
| 10 | 46.6 |
| 11 | 24.4 |
| 12 | 31.0 |
| 13 | 38.0 |
| 14 | 78.5 |
| 15 | 57.9 |
| 16 | 35.6 |
| 17 | 36.1 |
| 18 | 26.5 |
| 19 | 30.8 |
| 20 | 45.5 |
| 21 | 33.7 |
| 22 | 63.1 |
| 23 | 50.5 |
| 24 | 17.5 |
| 25 | 41.5 |
| 26 | 42.3 |
| 27 | 20.4 |
| 28 | 44.7 |
| 29 | 27.5 |
| 30 | 53.9 |
| 31 | 30.6 |
| 32 | 33.2 |

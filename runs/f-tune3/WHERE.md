# f-tune3: where it ran

All 16 seeds ran on epyc (16 cores, 1 thread per core), 14 Nov 2026, under nice -n 10. None on workstation or modal. No seed failed, none was rerun.
The three arms ran one after the other (f-tune8, f-tune3, f-random), 10:15 to 12:35 UTC, with a keepalive kernel for the JupyterHub server.

Binary: commit 6df6477, uploaded to epyc as the commit tarball (no .git, tree checked blob by blob 1522/1522), built with cargo 1.99.1 --release.
Self-check from RUNBOOK.md: last log row of the default search seed 2 at 120,000 was 120052,22831,27.7,0.82164,0.8142,4,0.7183 (matches).
Command (RUNBOOK.md, package F), commit passed through --extra because the tree has no .git:

    python local_runner.py --seeds 1-16 --budget 1500000 --tag f-tune3 --parallel 2 --threads 8 --extra="--tune-consts 3 --val-log --commit 6df6477"

Timing (not committed), 150,000 candidates: time-f (--tune-consts 8 --val-log) 27 s and 23 s per seed; time-fr (--algo random --val-log,
added by the executing agent to estimate the random arm) 18 s and 17 s.
verify.py ran on workstation (JAX on CPU) at the same commit -> verify.txt. Runner log: runner_log_epyc.txt.

Total wall 3333 s.

| seed | minutes |
|---|---|
| 1 | 2.7 |
| 2 | 6.1 |
| 3 | 4.8 |
| 4 | 3.1 |
| 5 | 5.1 |
| 6 | 3.6 |
| 7 | 5.9 |
| 8 | 4.8 |
| 9 | 19.5 |
| 10 | 2.9 |
| 11 | 22.4 |
| 12 | 5.0 |
| 13 | 12.0 |
| 14 | 2.6 |
| 15 | 6.5 |
| 16 | 2.7 |

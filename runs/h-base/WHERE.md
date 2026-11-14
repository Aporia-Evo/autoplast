# h-base: where it ran

All 32 seeds ran on epyc (16 cores, 1 thread per core), 14 Nov 2026, under nice -n 10. None on workstation or modal.
The three arms of package H ran one after the other (h-base, h-share, h-lexicase), 15:07 to 22:18 UTC, with a keepalive kernel.
No seed failed, none was rerun.

Binary: commit ad31161, uploaded as the commit tarball (no .git, tree checked blob by blob 1826/1826), built with cargo 1.99.1 --release.
Self-check of package F repeated: 120052,22831,28.3,0.82164,0.8142,4,0.7183 (matches).
Command (RUNBOOK.md, package H), commit passed through --extra because the tree has no .git:

    python local_runner.py --seeds 1-32 --budget 1500000 --tag h-base --parallel 2 --threads 8 --extra="--val-log --commit ad31161"

Timing (not committed), 150,000 candidates: time-h-share 47 s and 57 s per seed, time-h-lex 15 s and 16 s.
verify.py ran on workstation (JAX on CPU) at the same commit -> verify.txt. Runner log: runner_log_epyc.txt.

Total wall 4916 s.

| seed | minutes |
|---|---|
| 1 | 2.1 |
| 2 | 2.9 |
| 3 | 3.9 |
| 4 | 2.7 |
| 5 | 2.6 |
| 6 | 3.7 |
| 7 | 6.9 |
| 8 | 4.4 |
| 9 | 3.3 |
| 10 | 2.0 |
| 11 | 14.3 |
| 12 | 13.3 |
| 13 | 1.8 |
| 14 | 12.7 |
| 15 | 11.7 |
| 16 | 4.2 |
| 17 | 2.7 |
| 18 | 2.6 |
| 19 | 2.5 |
| 20 | 3.2 |
| 21 | 4.7 |
| 22 | 2.0 |
| 23 | 2.3 |
| 24 | 3.7 |
| 25 | 1.8 |
| 26 | 3.9 |
| 27 | 5.7 |
| 28 | 3.9 |
| 29 | 3.4 |
| 30 | 4.7 |
| 31 | 13.7 |
| 32 | 4.7 |

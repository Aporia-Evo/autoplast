# h-lexicase: where it ran

All 32 seeds ran on epyc (16 cores, 1 thread per core), 14 Nov 2026, under nice -n 10. None on workstation or modal.
The three arms of package H ran one after the other (h-base, h-share, h-lexicase), 15:07 to 22:18 UTC, with a keepalive kernel.
No seed failed, none was rerun.

Binary: commit ad31161, uploaded as the commit tarball (no .git, tree checked blob by blob 1826/1826), built with cargo 1.99.1 --release.
Self-check of package F repeated: 120052,22831,28.3,0.82164,0.8142,4,0.7183 (matches).
Command (RUNBOOK.md, package H), commit passed through --extra because the tree has no .git:

    python local_runner.py --seeds 1-32 --budget 1500000 --tag h-lexicase --parallel 2 --threads 8 --extra="--select lexicase --val-log --commit ad31161"

Timing (not committed), 150,000 candidates: time-h-share 47 s and 57 s per seed, time-h-lex 15 s and 16 s.
verify.py ran on workstation (JAX on CPU) at the same commit -> verify.txt. Runner log: runner_log_epyc.txt.

Total wall 8919 s.

| seed | minutes |
|---|---|
| 1 | 5.7 |
| 2 | 16.8 |
| 3 | 6.7 |
| 4 | 5.4 |
| 5 | 5.2 |
| 6 | 6.8 |
| 7 | 17.0 |
| 8 | 6.8 |
| 9 | 6.9 |
| 10 | 6.7 |
| 11 | 5.5 |
| 12 | 23.4 |
| 13 | 14.4 |
| 14 | 5.4 |
| 15 | 6.7 |
| 16 | 6.5 |
| 17 | 5.8 |
| 18 | 14.8 |
| 19 | 8.6 |
| 20 | 5.8 |
| 21 | 6.9 |
| 22 | 27.1 |
| 23 | 7.7 |
| 24 | 3.8 |
| 25 | 13.6 |
| 26 | 5.2 |
| 27 | 17.2 |
| 28 | 7.6 |
| 29 | 5.0 |
| 30 | 5.1 |
| 31 | 6.4 |
| 32 | 7.0 |

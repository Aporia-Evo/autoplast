# h-share: where it ran

All 32 seeds ran on epyc (16 cores, 1 thread per core), 14 Nov 2026, under nice -n 10. None on workstation or modal.
The three arms of package H ran one after the other (h-base, h-share, h-lexicase), 15:07 to 22:18 UTC, with a keepalive kernel.
Seed 16 failed with a panic (see h_report.md); it was not rerun.

Binary: commit ad31161, uploaded as the commit tarball (no .git, tree checked blob by blob 1826/1826), built with cargo 1.99.1 --release.
Self-check of package F repeated: 120052,22831,28.3,0.82164,0.8142,4,0.7183 (matches).
Command (RUNBOOK.md, package H), commit passed through --extra because the tree has no .git:

    python local_runner.py --seeds 1-32 --budget 1500000 --tag h-share --parallel 2 --threads 8 --extra="--select share --val-log --commit ad31161"

Timing (not committed), 150,000 candidates: time-h-share 47 s and 57 s per seed, time-h-lex 15 s and 16 s.
verify.py ran on workstation (JAX on CPU) at the same commit -> verify.txt. Runner log: runner_log_epyc.txt.

Total wall 11913 s.

| seed | minutes |
|---|---|
| 1 | 10.6 |
| 2 | 9.2 |
| 3 | 11.3 |
| 4 | 12.7 |
| 5 | 9.8 |
| 6 | 19.6 |
| 7 | 19.6 |
| 8 | 12.3 |
| 9 | 14.8 |
| 10 | 12.7 |
| 11 | 11.3 |
| 12 | 10.2 |
| 13 | 10.1 |
| 14 | 10.8 |
| 15 | 11.5 |
| 16 | 11.4 | failed (panic)
| 17 | 13.2 |
| 18 | 12.0 |
| 19 | 12.1 |
| 20 | 11.3 |
| 21 | 13.4 |
| 22 | 12.0 |
| 23 | 14.9 |
| 24 | 11.4 |
| 25 | 15.0 |
| 26 | 10.3 |
| 27 | 10.8 |
| 28 | 9.6 |
| 29 | 14.3 |
| 30 | 10.1 |
| 31 | 9.2 |
| 32 | 12.6 |

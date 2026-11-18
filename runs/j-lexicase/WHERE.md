# j-lexicase: where it ran

All 32 seeds ran on epyc (16 cores, 1 thread per core), from 17 Nov 2026 11:56 UTC, 57897 s, under nice -n 10, with a keepalive kernel.
None on workstation or modal. No seed failed, none was rerun. j-share started right after on the same machine.

Binary: commit 50c2d10, the build of package I (tree checked blob by blob 2618/2618; self-check of F matched). No change under src/
up to 4308a1e. Command (RUNBOOK.md, package J), commit passed through --extra because the tree has no .git:

    python local_runner.py --seeds 1-32 --budget 1500000 --tag j-lexicase --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --select lexicase --val-log --level-acc 0.651 --level-long 0.838 --commit 50c2d10"

The start was held once by the platform's safety check (16 Nov) and sent again unchanged on 17 Nov after the owner's release.
Timing (tag time-j-lex, not committed), 150,000 candidates: 156 s and 138 s per seed; projection 13 h for 32 seeds.
Dump made with the epyc binary; verify.py --task-json ran on workstation (JAX on CPU) at the same commit -> verify_dump.txt; the dump was
deleted on both machines. Runner log: runner_log_epyc.txt.

Total wall 57897 s.

| seed | minutes |
|---|---|
| 1 | 40.4 |
| 2 | 39.7 |
| 3 | 20.9 |
| 4 | 101.4 |
| 5 | 47.4 |
| 6 | 79.9 |
| 7 | 34.8 |
| 8 | 56.7 |
| 9 | 81.5 |
| 10 | 57.4 |
| 11 | 39.5 |
| 12 | 25.0 |
| 13 | 43.5 |
| 14 | 56.6 |
| 15 | 69.1 |
| 16 | 91.1 |
| 17 | 58.2 |
| 18 | 109.4 |
| 19 | 51.1 |
| 20 | 40.4 |
| 21 | 149.6 |
| 22 | 33.7 |
| 23 | 88.1 |
| 24 | 66.4 |
| 25 | 58.9 |
| 26 | 27.7 |
| 27 | 71.2 |
| 28 | 60.3 |
| 29 | 43.3 |
| 30 | 69.3 |
| 31 | 46.1 |
| 32 | 44.8 |

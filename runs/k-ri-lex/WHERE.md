# k-ri-lex: where it ran

All 32 seeds ran on epyc (16 cores, 1 thread per core), started 2026-11-19T20:33:59Z, 63244 s, under nice -n 10, with a keepalive kernel.
None on workstation or modal. No seed of this run failed, none was rerun.

Binary: commit 6c2f60a (contains "Corrected 19 Nov"; tree checked blob by blob 3238/3238), built in ~/autoplast-k on 19 Nov 2026. No k-ri-lex
run or timing had been started with an earlier build, so there is no k-ri-lex-faulty folder. Self-checks on epyc after the build:
package F row `120052,22831,29.2,0.82164,0.8142,4,0.7183`; d-kalman seed 9 row `50036,19778,40.3,0.50570,0.5094,12,0.3803` (both as expected).
Command (RUNBOOK.md, package K), commit passed through --extra because the tree has no .git:

    python local_runner.py --seeds 1-32 --budget 1500000 --tag k-ri-lex --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --select lexicase --residual-insert --val-log --level-acc 0.651 --level-long 0.838 --commit 6c2f60a"

Timing (tag time-k-ri-lex, not committed), 150,000 candidates: 264 s and 273 s per seed; projection 273 s x 10 x 16 pairs = 12.1 h, x2 = 24.3 h.
Dump made with the epyc binary; verify.py --task-json and the epsilon check ran on workstation (JAX on CPU) at the same commit ->
verify_dump.txt, verify_eps_x64.txt; the dump was deleted on both machines. Runner log: runner_log_epyc.txt (start/end: runner_start_utc.txt,
runner_done_utc.txt).

## Addendum: two aborted starts before the complete run

The same command was started twice before, and both times the hub server was stopped from outside about 10 minutes after the start, which
killed the runner and both search processes (stderr empty, no out-of-memory event in the cgroup, journal: `received signal 15` at 15:54:54 UTC
for the second start). Cause: the keepalive kernel of these two starts only slept in a loop and printed nothing, so the hub's idle culler saw no
activity; the complete run used a keepalive that prints a line every 60 s. Both folders were renamed, not deleted, and are committed unchanged:
- aborted1/: started 2026-11-19T13:26:00Z; seeds 1 and 2 reached 300,020 candidates (last log rows at 570 s); no summary.
- aborted2/: started 2026-11-19T15:44:43Z; seeds 1 and 2 reached 300,020 candidates (last log rows at 570 s); no summary.
Their log rows up to 300,020 equal those of seeds 1 and 2 of the complete run in every column except the seconds.

Total wall 63244 s.

| seed | minutes |
|---|---|
| 1 | 48.8 |
| 2 | 46.4 |
| 3 | 83.5 |
| 4 | 102.8 |
| 5 | 31.2 |
| 6 | 98.6 |
| 7 | 83.9 |
| 8 | 78.4 |
| 9 | 34.4 |
| 10 | 39.6 |
| 11 | 41.2 |
| 12 | 96.6 |
| 13 | 55.1 |
| 14 | 42.9 |
| 15 | 52.2 |
| 16 | 43.8 |
| 17 | 39.5 |
| 18 | 83.7 |
| 19 | 55.9 |
| 20 | 42.4 |
| 21 | 44.0 |
| 22 | 77.8 |
| 23 | 42.8 |
| 24 | 40.7 |
| 25 | 137.4 |
| 26 | 85.3 |
| 27 | 99.7 |
| 28 | 48.3 |
| 29 | 81.0 |
| 30 | 44.1 |
| 31 | 38.0 |
| 32 | 98.7 |

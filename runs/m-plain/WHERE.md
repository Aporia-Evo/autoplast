# m-plain: where it ran

All 8 seeds ran on epyc (16 cores, 1 thread per core), started 2026-11-21T21:35:22Z, 7660 s, under nice -n 10, with a keepalive kernel that
prints a line every 60 s. None on workstation or modal. No seed failed, none was rerun, no interruption. m-lexicase started right after in the
same script (run_M.sh).

Binary: commit dce11aa (tree checked blob by blob 4327/4327), built in a fresh directory on epyc on 21 Nov 2026. Self-checks after the build:
package F row `120052,22831,28.4,0.82164,0.8142,4,0.7183`; d-kalman seed 9 row 50036 `50036,19778,39.3,0.50570,0.5094,12,0.3803` (both as expected).
No timing run (RUNBOOK: eight seeds per arm); expected from K about 60 minutes per seed. Command (RUNBOOK.md, package M), commit passed through --extra:

    python local_runner.py --seeds 801-808 --task-seed-from-seed --budget 1500000 --tag m-plain --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --val-log --level-acc 0.651 --level-long 0.838 --commit dce11aa"

Dumps and the long probe were made with the epyc binary; verify.py ran on workstation (JAX on CPU); the dumps were deleted afterwards.
Runner log: runner_log_epyc.txt.

| task seed | minutes |
|---|---|
| 801 | 22.5 |
| 802 | 19.2 |
| 803 | 29.1 |
| 804 | 18.6 |
| 805 | 82.6 |
| 806 | 19.1 |
| 807 | 31.6 |
| 808 | 28.6 |

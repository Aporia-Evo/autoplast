# m-lexicase: where it ran

All 8 seeds ran on epyc (16 cores, 1 thread per core), started 2026-11-21T23:43:02Z right after m-plain in the same script (run_M.sh), 10191 s,
under nice -n 10, with a keepalive kernel that prints a line every 60 s. None on workstation or modal. No seed failed, none was rerun, no interruption.

Binary and self-checks: as in runs/m-plain/WHERE.md (commit dce11aa). Command (RUNBOOK.md, package M), commit passed through --extra:

    python local_runner.py --seeds 801-808 --task-seed-from-seed --budget 1500000 --tag m-lexicase --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --select lexicase --val-log --level-acc 0.651 --level-long 0.838 --commit dce11aa"

Dumps and the long probe were made with the epyc binary; verify.py ran on workstation (JAX on CPU); the dumps were deleted afterwards.
Runner log: runner_log_epyc.txt.

| task seed | minutes |
|---|---|
| 801 | 78.5 |
| 802 | 19.3 |
| 803 | 26.3 |
| 804 | 29.7 |
| 805 | 23.9 |
| 806 | 19.5 |
| 807 | 71.9 |
| 808 | 26.8 |

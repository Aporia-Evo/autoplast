# n-random: where it ran

All 16 seeds ran on epyc (16 cores, 1 thread per core), started 2026-11-22T04:15:36Z, 1027 s, under nice -n 10, with a keepalive kernel that prints a line
every 60 s. None on workstation or modal. No seed failed, none was rerun, no interruption. Started right after n-plain in the same script (run_N.sh).

Binary: commit dce11aa (tree checked blob by blob 4327/4327; self-checks in runs/m-plain/WHERE.md, among them d-kalman seed 9 row
`50036,19778,39.3,0.50570,0.5094,12,0.3803`). Command (RUNBOOK.md, package N), commit passed through --extra:

    python local_runner.py --seeds 901-916 --task-seed-from-seed --budget 300000 --tag n-random --parallel 2 --threads 8 --task opt --extra="--opt-ops --persist-v 2 --algo random --commit dce11aa"

Timing (not committed), 30,000 candidates, seeds 901-902: time-n-plain 51 s and 24 s (projection 51 s x 10 x 8 pairs = 1.1 h, x2 = 2.3 h);
time-n-random 13 s and 13 s (0.3 h, x2 = 0.6 h; this second timing tag is an extra of the executing agent, RUNBOOK lists only time-n-plain).
Train dumps (`autoplast dump --task opt --split train --task-seed N`) made with the epyc binary; verify/opt_structure.py ran on the workstation
with the verify folder on PYTHONPATH (the script's own path insert splits on "/" and does not find verify_opt on Windows; the script itself is
unchanged). The dumps were deleted afterwards. Runner log: runner_log_epyc.txt.

| task seed | minutes |
|---|---|
| 901 | 2.1 |
| 902 | 2.1 |
| 903 | 2.1 |
| 904 | 2.1 |
| 905 | 2.1 |
| 906 | 2.1 |
| 907 | 2.1 |
| 908 | 2.1 |
| 909 | 2.1 |
| 910 | 2.1 |
| 911 | 2.1 |
| 912 | 2.1 |
| 913 | 2.1 |
| 914 | 2.1 |
| 915 | 2.1 |
| 916 | 2.1 |

# d-kalman: where it ran

All 16 seeds ran on epyc (16 cores, 1 thread per core), 12 Nov 2026, 14:07 to 20:18 UTC, under nice -n 10. None on workstation or modal.
No seed failed, none was rerun. Load at the check before the timing run: 0.00.

Binary: commit e979a8e, uploaded to epyc as the commit tarball (no .git), built there with cargo 1.99.1 --release; baselines self-check OK.
Command (RUNBOOK.md, package D, step 2), commit passed through --extra because the uploaded tree has no .git:

    python local_runner.py --seeds 1-16 --budget 1500000 --tag d-kalman --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --commit e979a8e"

Started with nohup; a keepalive kernel kept the JupyterHub server from being stopped for idleness (it had stopped twice that day
within minutes of inactivity). runner_log_epyc.txt is the runner's own log.

Timing (tag time-d, epyc, not committed): 150,000 candidates, seed 1 110 s, seed 2 196 s.
Step 3: autoplast dump --regime collision3 --split test with the epyc binary; verify.py --task-json ran on workstation (JAX on CPU) at
the same commit on that dump -> verify_dump.txt. The dump was deleted afterwards on both machines.

Total wall 22069 s.

| seed | minutes |
|---|---|
| 1 | 61.0 |
| 2 | 58.8 |
| 3 | 84.7 |
| 4 | 34.7 |
| 5 | 21.0 |
| 6 | 89.3 |
| 7 | 26.0 |
| 8 | 17.4 |
| 9 | 39.7 |
| 10 | 107.1 |
| 11 | 21.5 |
| 12 | 34.8 |
| 13 | 35.1 |
| 14 | 30.6 |
| 15 | 34.2 |
| 16 | 24.1 |

## Seeds 17 to 32 (package E)

All 16 ran on epyc, 13 Nov 2026, 15:06 to 20:32 UTC, under nice -n 10, with the same binary as seeds 1-16 (sha256 4b3d4ef3...,
built 12 Nov 2026 09:35 UTC from e979a8e, not rebuilt). Load before the start 0.05. No seed failed, none was rerun.
Command (RUNBOOK.md, package E), commit passed through --extra as for seeds 1-16:

    python local_runner.py --seeds 17-32 --budget 1500000 --tag d-kalman --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --commit e979a8e"

The runner skipped seeds 1-16 and rewrote aggregate.md for all 32 seeds. Keepalive kernel as in D. Runner log: runner_log_epyc_E.txt.
Dump made with the epyc binary, verify.py run on workstation (same verify.py as at e979a8e) -> verify_dump_17-32.txt; dump deleted on both machines.

Total wall 19314 s.

| seed | minutes |
|---|---|
| 17 | 34.2 |
| 18 | 16.6 |
| 19 | 19.6 |
| 20 | 55.4 |
| 21 | 25.8 |
| 22 | 28.9 |
| 23 | 14.7 |
| 24 | 29.6 |
| 25 | 91.3 |
| 26 | 15.2 |
| 27 | 54.5 |
| 28 | 26.8 |
| 29 | 41.3 |
| 30 | 61.3 |
| 31 | 72.5 |
| 32 | 43.6 |

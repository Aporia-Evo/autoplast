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

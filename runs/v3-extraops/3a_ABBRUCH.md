# 3a: run aborted (addendum, post hoc)

Time: 2026-11-04 07:19 UTC. Started 4 Nov 2026 05:35 UTC (`v3-extraops`, then `v3-nomatvec` queued and held by
runs/v3-nomatvec/PAUSE). Stopped by the user's decision about 2.6 h in ("stop erstmal den
lauf"), after concluding that the setup is too rigid (fixed matrix memory, fixed linear
readout, a task where delta is near-optimal) and the search is inefficient. This is an
aborted run, not a result; no rate is computed and the decision rule is not applied.

How it was stopped: the background cell was interrupted (SIGINT). That did not end
local_runner.py, which started seeds 4 and 5 after the first two autoplast processes were
killed. The runner processes and their children were then killed by command line (psutil).
v3-nomatvec never started. Lesson: interrupting the cell is not enough; kill the runner.

State of runs/v3-extraops (raw files kept unchanged):
| seed | status | candidates | train acc at stop | note |
|---|---|---|---|---|
| 1 | killed | 1,400,052 of 1.5M | 0.909 | reached delta level in training; no best.json written |
| 2 | finished (2,695 s) | 1,500,020 | 0.912 | delta beta=0.5 at 998,644 candidates; see below |
| 3 | killed | 950,004 | 0.730 | linear-attention level |
| 4 | killed | 300,020 | 0.720 | |
| 5 | killed | 150,004 | 0.726 | |
| 6-16 | not started | | | |

Seed 2 (only finished seed, Rust values, not JAX-verified):
`S' = S + tanh(0.722·v − S·tanh²(max(k, tanh³ k)))⊗(<tanh³ k, tanh²(max(k, tanh³ k))>·k)`
It uses the extra op VecMax. Train 0.912, T12 ow0.3 0.914, T64 K8 0.850, T128 K8 0.845,
d32 T24 0.974. This is the level of tuned DeltaNet on v3 (0.923 / 0.852 / 0.850).

Resume: delete runs/v3-nomatvec/PAUSE as needed and rerun the commands in 3a_VORHERSAGE.md;
local_runner.py skips seeds whose summary.md exists (only seed 2 here). Seeds 1, 3, 4 and 5
restart from scratch.

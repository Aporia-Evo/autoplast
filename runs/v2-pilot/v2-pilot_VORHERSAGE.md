# v2-pilot: prediction (written before the run)

Time: 2026-11-03 14:37 UTC. Commit: 2782d52 (branch exp/v2-rediscovery-rate).

Purpose: timing pilot required by CLAUDE.md before the 16-seed rediscovery-rate run (queue item 1).

Command: `modal run modal_runner.py --seeds 1-2 --budget 300000 --tag v2-pilot`
(8 CPUs per container, --threads 8, --batch 128, add-node on, CPU only.)

Extrapolation method: wall time grows faster than candidates because programs get
matrix-heavy later. Local v2 logs: t(1.5M)/t(300k) = 11.5 (seed 1) and 24.4 (seed 2).
The 16-seed estimate will be pilot time at 300k times this factor range, times 16.

Predictions (subjective probabilities):
- Search wall time per seed at 300k on Modal: 15 to 90 s (p = 0.7).
- Image build plus cold start dominates the pilot cost (p = 0.75).
- Both seeds reach the linear-attention milestone by 300k (p = 0.9).
- Neither seed reaches delta beta=0.5 by 300k (p = 0.85; local seed 2 needed 865k).
- Estimated 16-seed cost at 1.5M: 1 to 6 container-hours (8 CPUs each) (p = 0.6).

## Addendum (2026-11-03 14:39 UTC, post hoc)

The pilot did not run. `modal run` exited after 2.1 s with "Token ID is malformed" before any
container or image build started; no Modal credits were used. Afterwards the decision came in
that CPU searches belong on the local machine (Ryzen 5700G, 8 cores / 16 threads) and Modal is
for GPU runs only, so this Modal pilot is withdrawn, not retried. Predictions above stay
unchanged and untested.

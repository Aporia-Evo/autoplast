# v2-localpilot: prediction (written before the run)

Time: 2026-11-03 15:01 UTC. Commit: e75904a (branch exp/v2-rediscovery-rate). Machine: Ryzen 5700G,
8 cores / 16 threads, Windows, cargo 1.91.1 release build.

Purpose: timing pilot before the local 16-seed rediscovery-rate run (CLAUDE.md queue item 1).
Replaces the withdrawn Modal pilot (runs/v2-pilot).

Command (two processes in parallel, 8 threads each, i.e. the layout planned for 16 seeds):
`autoplast search --seed S --budget 300000 --threads 8 --batch 128 --log-every 50000 --out runs/v2-localpilot/seedS`
for S = 1, 2. Add-node on. Same flags as the Modal runner except where it ran alone.

Extrapolation: wall time grows faster than candidates. Local v2 logs give
t(1.5M)/t(300k) = 11.5 (seed 1) and 24.4 (seed 2). Estimate for 16 seeds at 1.5M =
pilot time per seed at 300k x factor (11.5 to 24.4) x 16 seeds / 2 parallel.

Predictions (subjective probabilities):
- Wall time per seed at 300k: 20 to 90 s (p = 0.7).
- Both seeds reach the linear-attention milestone by 300k (p = 0.9).
- Neither seed reaches delta beta=0.5 by 300k (p = 0.85).
- Estimated 16-seed total at 1.5M: 1 to 6 hours on this machine (p = 0.6).
- Results with 8 threads differ from runs/v2-local for the same seed, because batch and
  thread count change the evaluation order (p = 0.7).

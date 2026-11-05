# v3-localpilot: prediction (written before the run)

Time: 2026-11-03 21:06 UTC. Code: ff3b76c plus uncommitted v3 task option (git.exe blocked by the sandbox).
Command: `python local_runner.py --seeds 1-2 --budget 300000 --tag v3-localpilot --task v3 --parallel 2 --threads 8`

Purpose: timing pilot before a 16-seed v3 run. One v3 evaluation runs 96x12 + 48x64 = 4,224
writes against 1,152 in v2 (factor 3.7).

Predictions (subjective probabilities):
- Wall time per seed at 300k: 2 to 6 min (p = 0.7).
- Both seeds reach the linear-attention milestone by 300k (p = 0.85).
- Neither seed reaches the v3 delta beta=0.5 milestone by 300k (p = 0.8).
- Extrapolated 16-seed v3 run at 1.5M: 4 to 12 hours locally (p = 0.6).

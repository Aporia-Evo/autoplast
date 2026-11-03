# v2: prediction (written before the run)

Time: 2026-11-03 15:10 UTC. Branch exp/v2-rediscovery-rate; commit = the commit that adds this file and
local_runner.py. Machine: Ryzen 5700G, cargo 1.91.1 release build.

Question (CLAUDE.md queue item 1): at what rate does the search rediscover the delta family
from an empty program, and after how many candidates (median)?

Command: `python local_runner.py --seeds 1-16 --budget 1500000 --tag v2 --parallel 2 --threads 8`
(per seed: `autoplast search --threads 8 --batch 128 --log-every 50000`, add-node on).
No change to search space, mutations or fitness relative to the pilot.

Prior evidence: runs/v2-local (2 seeds, other threads/batch): 1 of 2 reached delta beta=0.5,
at 865k candidates. Pilot (300k): both seeds at decayed linear attention.

Predictions (subjective probabilities):
- Linear-attention milestone reached by 16/16 seeds (p = 0.9).
- Delta beta=0.5 milestone reached by at least 1 seed (p = 0.9), by 3 to 9 of 16 (p = 0.6).
- Median candidates to delta beta=0.5 among seeds that reach it: 400k to 1.2M (p = 0.6).
- At least one seed ends on a rule outside the linear/delta family with a state-dependent
  gate, like v2-local seed 1 (p = 0.5).
- For every seed's best rule, train minus test ow0.3 is at most 0.03 (p = 0.8).
- Total wall time 1.5 to 3.1 h (p = 0.6); under 4 h (p = 0.85).

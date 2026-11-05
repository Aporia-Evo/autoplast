# v2-noaddnode: prediction (written before the run)

Time: 2026-11-03 19:41 UTC. Branch exp/v2-rediscovery-rate; commit = the commit that adds this file.
Machine: Ryzen 5700G, same binary as runs/v2.

Question (CLAUDE.md queue item 2): does the NEAT-style add-node (split-edge) mutation matter
for rediscovering the delta rule? Earlier evidence was 1 vs 2 seeds with different train sets.

Command: `python local_runner.py --seeds 1-16 --budget 1500000 --tag v2-noaddnode --parallel 2 --threads 8 --no-split-edge`
Only difference to runs/v2: `--no-split-edge`. Same seeds, budget, threads, batch, task.

Decision rule, fixed now: compare the delta beta=0.5 rate with v2 (6/16) by two-sided
Fisher exact test. With 16 vs 16 seeds this is significant (p < 0.05) only at 0/16
(p = 0.018) or at 13/16 or more (p = 0.029). Any result from 1 to 12 seeds means "no
detectable effect at this sample size", not "no effect". The median candidates to delta
are compared descriptively only.

Predictions (subjective probabilities):
- Linear-attention milestone reached by 16/16 seeds (p = 0.9).
- Delta beta=0.5 reached by fewer than 6 seeds (p = 0.5); by 0 seeds (p = 0.15).
- Result in the non-significant band 1 to 12 seeds (p = 0.8).
- Seeds that reach delta do so with a > 1 again (p = 0.9).
- Total wall time 1.2 to 3 h (p = 0.6).

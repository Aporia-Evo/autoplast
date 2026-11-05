# v3-baselines: prediction (written before the computation)

Time: 2026-11-03 21:01 UTC. Code: ff3b76c plus the uncommitted v3 task option (README "Task v3"); git.exe
is blocked by the sandbox, so this cannot be committed before the run.

Question: does the v3 task punish growth factors a > 1, and what do the tuned baselines
score on it? Commands:
- `autoplast baselines --task v3` and `autoplast baselines` (v2, for the new test columns)
- `autoplast sweep --task v3` and `autoplast sweep` (v2, refined alpha grid)
- `autoplast eval` of all 32 best rules from runs/v2 and runs/v2-noaddnode (new test columns)

Predictions (subjective probabilities):
- Tuned Gated DeltaNet on v3 has its optimum at a <= 1.0 (p = 0.65).
- On v2 with the refined grid the optimum stays at a > 1 (p = 0.8).
- Delta beta=0.5 (a = 1) keeps test T128 K8 above 0.8 (p = 0.6).
- Of the 14 found delta rules (all a > 1), at least 12 fall below 0.5 on T128 K8 (p = 0.75).
- Linear attention scores below 0.3 on T64 K8 (many overwrites of the same key) (p = 0.7).
- Tuned Gated DeltaNet on v3 is still at least 0.95 on test d16 T12 ow0.3 (p = 0.6).

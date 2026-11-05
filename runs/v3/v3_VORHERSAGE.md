# v3: prediction (written before the run)

Time: 2026-11-03 21:19 UTC. Code: ff3b76c plus the uncommitted v3 task option (README "Task v3"); git.exe is
blocked by the sandbox, archive artifact autoplast_uncommitted.tar.gz holds the code state.

Question (CLAUDE.md queue item 3): on the v3 task (96 standard + 48 long episodes), how often
does the search find a delta rule, with which growth factor a, and how do the found rules do
on the long held-out suites against tuned DeltaNet / Gated DeltaNet on v3?

Command: `python local_runner.py --seeds 1-16 --budget 1500000 --tag v3 --task v3 --parallel 2 --threads 8`
(add-node on, as in v2). Reference: v3 sweep (DeltaNet a=1: T12 0.923, T64 0.852, T128 0.850;
Gated DeltaNet a=1.01: 0.930, 0.833, 0.809). Milestones are the v3 train accuracies of the
reference rules (delta beta=0.5: 0.901).

Predictions (subjective probabilities):
- Delta beta=0.5 milestone reached by 4 to 12 of 16 seeds (p = 0.6); by at least 1 (p = 0.95).
- Median growth factor a of the delta seeds in [0.98, 1.03] (p = 0.65); no delta seed has
  a > 1.06 (p = 0.7).
- Every delta seed keeps T128 K8 at or above 0.75 (p = 0.6).
- At least one seed beats tuned DeltaNet on v3 on T128 K8 by more than 0.02 (p = 0.25).
- No seed beats tuned Gated DeltaNet on v3 on T12 ow0.3 by more than 0.01 (p = 0.75).
- Overfitting check: train minus the query-weighted held-out mix (0.70 x T12 ow0.3 + 0.30 x
  T64 K8, matching the train set's query shares) is at most 0.03 for every seed (p = 0.7).
- Total wall time 4 to 9 h (p = 0.65).

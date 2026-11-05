# stage2-baselines: prediction (written before the computation)

Time: 2026-11-05 05:25 UTC. Code: 689142e plus the uncommitted regime option (README "Stage-2 regimes").

Question (CLAUDE.md item 5, first part): on which regime are tuned DeltaNet / Gated DeltaNet
weak, and how much headroom does the offline least-squares reference show?
Commands per regime R in collision, overload, noisyq, longgap:
`autoplast baselines --regime R`, `autoplast sweep --regime R`,
`autoplast dump --regime R --split test` then `python verify/ceiling.py` on it.

Predictions (subjective probabilities):
- collision: tuned DeltaNet below 0.80 on its regime test (p 0.6); LS reference at least 0.05
  above the best tuned family (p 0.6).
- overload: tuned DeltaNet below 0.70 (p 0.6); LS reference at least 0.05 above (p 0.5).
- noisyq: tuned DeltaNet at least 0.05 below its v2 value 0.924 (p 0.6); LS reference within
  0.03 of the best tuned family (p 0.5).
- longgap: tuned DeltaNet 0.83 to 0.87 (p 0.7); LS reference at least 0.95 (p 0.7).
- Gated DeltaNet gains at most 0.01 over DeltaNet on every regime test (p 0.6).
- The largest headroom (LS reference minus best tuned family) is on longgap or collision (p 0.6).

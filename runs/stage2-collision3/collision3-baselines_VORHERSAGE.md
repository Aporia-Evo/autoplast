# collision3 baselines: prediction (written before the computation)

Time: 2026-11-05 05:57 UTC. Code: 3bc77d0 plus the collision3 regime (README "Stage-2 regimes").
Commands: `autoplast baselines --regime collision3`, `autoplast sweep --regime collision3`,
`autoplast dump --regime collision3 --split test` and `verify/ceiling.py` on it.
Reference from the short collision regime: DeltaNet 0.658, GDN 0.725 (a = 1.15), LS 1.000.

Predictions (subjective probabilities):
- Tuned Gated DeltaNet optimum at a <= 1.01 on collision3 (p 0.7).
- Tuned DeltaNet on the collision3 test between 0.60 and 0.72 (p 0.6).
- Tuned GDN at most 0.02 above tuned DeltaNet (p 0.65).
- LS reference at least 0.95 (p 0.8), so headroom of at least 0.2 over the best tuned family (p 0.65).

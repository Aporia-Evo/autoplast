# stage2-baselines: result

Time: 2026-11-05 05:34 UTC. Code: 689142e plus the regime option (README "Stage-2 regimes"). Local, 423 s total.
Raw outputs: baselines_R.md, sweep_R.md, ceiling_R.txt; task dumps train_R.json / test_R.json.

Held-out regime test (512 episodes, seed 9); tuned families tuned on the regime's train set:

| regime | linear attention | delta β=0.5 | tuned DeltaNet (e) | tuned Gated DeltaNet (a, e) | GDN on T128 K8 | LS reference |
|---|---|---|---|---|---|---|
| collision | 0.524 | 0.647 | 0.658 (0.30) | 0.725 (1.15, 0.60) | 0.000 | 1.000 |
| overload | 0.477 | 0.653 | 0.663 (0.40) | 0.723 (1.03, 0.50) | 0.400 | 0.956 |
| noisyq | 0.724 | 0.899 | 0.901 (0.45) | 0.934 (1.10, 0.65) | 0.020 | 0.971 |
| longgap | 0.049 | 0.850 | 0.875 (0.75) | 0.875 (1.00, 0.75) | 0.863 | 1.000 |

LS reference = offline ridge least squares on the final latest pairs (verify/ceiling.py,
lam 1e-3); train-set values 1.000 / 0.966 / 0.973 / 1.000.

Reading:
- Collision and overload leave large headroom: tuned DeltaNet 0.66, LS reference 1.00 and 0.96.
  Correlated keys (collision) or more keys than dimensions (overload) are where a single
  delta step per write is far from the best linear memory. Noisy queries leave little room
  (0.901 vs 0.971); long gaps 0.125.
- The Gated DeltaNet lead on collision, overload and noisyq comes with a > 1 and collapses
  on T128 K8 (0.000 / 0.400 / 0.020). These three regimes use short episodes (12 or 32
  writes), so the v2 amplification artefact is back. On them, tuned DeltaNet (a = 1) is the
  honest baseline unless the regimes are combined with long episodes as in v3.
- The LS reference is close to what known non-delta memories compute online (recursive least
  squares / Mesa layer; multi-step delta such as DeltaProduct moves towards it). Those need
  more state or more steps than one d×d matrix with one update. A found rule that closes
  part of this gap has to be compared with them, not only with Gated DeltaNet.

Predictions vs outcome:
- collision: DeltaNet below 0.80 (p 0.6): yes, 0.658. LS at least 0.05 above best tuned (p 0.6): yes, +0.275.
- overload: DeltaNet below 0.70 (p 0.6): yes, 0.663. LS at least 0.05 above (p 0.5): yes, +0.233.
- noisyq: DeltaNet at least 0.05 below 0.924 (p 0.6): no, 0.901. LS within 0.03 of best tuned (p 0.5): no, +0.037.
- longgap: DeltaNet 0.83 to 0.87 (p 0.7): no, 0.875. LS at least 0.95 (p 0.7): yes, 1.000.
- GDN gains at most 0.01 over DeltaNet everywhere (p 0.6): no (+0.067, +0.060, +0.033, 0).
- Largest headroom on longgap or collision (p 0.6): yes, collision.

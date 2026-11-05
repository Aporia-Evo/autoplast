# 3a timing pilot: result (both variants)

Time: 2026-11-04 05:29 UTC. Seeds 1-2, budget 300k, task v3, two in parallel, 8 threads each.
Prediction: runs/v3-nomatvec/3a_VORHERSAGE.md.

| variant | seed | wall s | delta 0.5 at | best rule (300k) | train | T12 ow0.3 | T64 K8 | T128 K8 |
|---|---|---|---|---|---|---|---|---|
| no MatVec | 1 | 196 | no | `S' = <tanh k, tanh k>·S + v⊗(<norm(tanh k − tanh v ⊙ tanh k), k>·k)` | 0.723 | 0.768 | 0.566 | 0.559 |
| no MatVec | 2 | 539 | 80,628 | `S' = S − σ(0.365)·S(k kᵀ) + tanh(0.365·tanh v)⊗k` | 0.908 | 0.920 | 0.852 | 0.854 |
| extra ops | 1 | 253 | no | `S' = 2.101·v⊗k − tanh(−S)` | 0.724 | 0.796 | 0.542 | 0.538 |
| extra ops | 2 | 388 | no | `S' = tanh(tanh(v⊗(tanh k + tanh² k)) + tanh(S))` | 0.721 | 0.788 | 0.570 | 0.556 |
| v3 (reference) | 1, 2 | 132, 200 | no, 18,420 | | | | | |

No-MatVec seed 2 builds the delta rule through `S (k kᵀ)` as expected. The extra-ops seeds
use the new elementwise matrix tanh (a saturating memory) and stay at linear-attention level
at 300k.

Cost: mean per seed at 300k is 368 s (no MatVec) and 321 s (extra ops) against 166 s for v3.
With the v3 factor t(1.5M)/t(300k) = 9.6, a 16-seed run takes about 7.8 h (no MatVec) and
6.8 h (extra ops), 14.6 h together; with the v2 factor 16.6 up to 13.6 h and 11.8 h.

Predictions vs outcome (pilot only): wall 2 to 6 min per seed for both (no: no-MatVec seed 2
took 9 min, extra-ops seed 2 6.5 min). The others concern the full runs.

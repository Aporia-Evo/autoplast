# 5a-pilot-A: 2 seeds, budget 300000, task v2 --regime collision3, add-node on, local

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) | wall s | best rule |
|---|---|---|---|---|---|---|
| 1 | 14,324 | no | no | no | 220 | `S' = ((v)⊗(tanh((k + k))) + σ((0.915 + 0.915))·S)` |
| 2 | 21,876 | no | no | no | 261 | `S' = ((v)⊗(k) - |tanh(tanh((tanh(k) + (tanh(k) ⊙ v))))|·(0 - S))` |

- linear attention: reached by 2/2 seeds, median 21,876 candidates
- delta rule (beta=1): reached by 0/2 seeds
- delta rule (beta=0.5): reached by 0/2 seeds
- gated delta (alpha=0.9): reached by 0/2 seeds

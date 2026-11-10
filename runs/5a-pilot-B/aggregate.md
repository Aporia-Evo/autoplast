# 5a-pilot-B: 2 seeds, budget 300000, task v2 --extra-ops --evolve-readout --regime collision3, add-node on, local

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) | wall s | best rule |
|---|---|---|---|---|---|---|
| 1 | 86,900 | no | no | no | 225 | `S' = tanh(tanh(0.947·((v)⊗(k) - (0 - S))))` |
| 2 | 6,260 | no | no | 51,188 | 638 | `S' = ((tanh((v)⊗(k)) + tanh(tanh(S))) + (tanh(tanh((v)⊗(k))) - (… ⊙ …)))` |

- linear attention: reached by 2/2 seeds, median 86,900 candidates
- delta rule (beta=1): reached by 0/2 seeds
- delta rule (beta=0.5): reached by 0/2 seeds
- gated delta (alpha=0.9): reached by 1/2 seeds, median 51,188 candidates

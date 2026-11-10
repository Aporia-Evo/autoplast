# 5a-pilot-C: 2 seeds, budget 300000, task v2 --evolve-readout --regime collision3, add-node on, local

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) | wall s | best rule |
|---|---|---|---|---|---|---|
| 1 | 8,436 | no | no | no | 86 | `S' = <tanh(k), tanh(k)>·((v)⊗(tanh(k)) + S)` |
| 2 | 25,204 | no | no | no | 178 | `S' = (|tanh(tanh(tanh(v)))|·(((v + v))⊗(k) + S) - 0)` |

- linear attention: reached by 2/2 seeds, median 25,204 candidates
- delta rule (beta=1): reached by 0/2 seeds
- delta rule (beta=0.5): reached by 0/2 seeds
- gated delta (alpha=0.9): reached by 0/2 seeds

# v3a-pilot-extraops: 2 seeds, budget 300000, task v3 --extra-ops, add-node on, local

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) | wall s | best rule |
|---|---|---|---|---|---|---|
| 1 | 18,548 | no | no | 20,084 | 253 | `S' = ((1.101·(v)⊗(k) + (v)⊗(k)) - tanh((0 - S)))` |
| 2 | 47,988 | no | no | 49,524 | 388 | `S' = tanh((tanh((v)⊗((tanh(k) + tanh(tanh(k))))) + tanh(S)))` |

- linear attention: reached by 2/2 seeds, median 47,988 candidates
- delta rule (beta=1): reached by 0/2 seeds
- delta rule (beta=0.5): reached by 0/2 seeds
- gated delta (alpha=0.9): reached by 2/2 seeds, median 49,524 candidates

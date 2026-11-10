# v3a-pilot-nomatvec: 2 seeds, budget 300000, task v3 --no-op MatVec, add-node on, local

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) | wall s | best rule |
|---|---|---|---|---|---|---|
| 1 | 81,140 | no | no | 83,316 | 196 | `S' = ((v)⊗(<norm((tanh(k) - (tanh(v) ⊙ tanh(k)))), k>·k) + <tanh(k), tanh(k)>·S)` |
| 2 | 13,684 | 78,836 | 80,628 | 78,836 | 539 | `S' = ((tanh(0.365·tanh(v)))⊗((k - 0)) - (σ(0.365)·(S)(((k - 0))⊗((k - 0))) - S))` |

- linear attention: reached by 2/2 seeds, median 81,140 candidates
- delta rule (beta=1): reached by 1/2 seeds, median 78,836 candidates
- delta rule (beta=0.5): reached by 1/2 seeds, median 80,628 candidates
- gated delta (alpha=0.9): reached by 2/2 seeds, median 83,316 candidates

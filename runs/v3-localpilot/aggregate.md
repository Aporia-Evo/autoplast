# v3-localpilot: 2 seeds, budget 300000, task v3, add-node on, local

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) | wall s | best rule |
|---|---|---|---|---|---|---|
| 1 | 74,740 | no | no | 82,676 | 132 | `S' = (σ(2.278)·S + (v)⊗(k))` |
| 2 | 13,172 | 15,732 | 18,420 | 14,196 | 200 | `S' = (S + ((tanh(tanh(tanh(v))) - 0.595·(S - 0.595·(k)⊗(tanh(tanh(v))))·k))⊗(k))` |

- linear attention: reached by 2/2 seeds, median 74,740 candidates
- delta rule (beta=1): reached by 1/2 seeds, median 15,732 candidates
- delta rule (beta=0.5): reached by 1/2 seeds, median 18,420 candidates
- gated delta (alpha=0.9): reached by 2/2 seeds, median 82,676 candidates

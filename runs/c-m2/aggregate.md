# c-m2: 16 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 672681  time: 1621s  pop: 500  tournament: 10
    commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | wall s | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|---|
| 1 | unclassified | 0.651 ±0.014 | 1621.5 | decayed linear attention (3,060), unclassified (21,620), linear attention (22,900), gated delta rule (79,348), delta rule (79,988) | `S' = ((tanh((σ(((-0.941 + |S·k|) + |S·k|)) + (-0.941 + |S·k|)·((-0.941 + |S·k|) + |S·k|))·(v - S·tanh(k))))⊗(norm(` |
| 2 | unclassified | 0.683 ±0.013 | 4406.1 | decayed linear attention (3,316), linear, not error-correcting (11,124), delta + Kronecker mix (12,020), unclassified (12,276), linear attention (13,684) | `S' = ((1.114·1.114·1.114·(-0.889·(0 - (P1 + (v)⊗(k))) - ((P1 + (v)⊗(k))·k)⊗(k)) + 1.114·1.114·1.114·(-0.889·(0 - (` |
| 3 | unclassified | 0.512 ±0.014 | 1101.9 | unclassified (884), decayed linear attention (1,268), linear attention (9,972) | `S' = ((v)⊗(norm(tanh(tanh((k + k))))) + 0.880·S)` |
| 4 | decayed linear attention | 0.512 ±0.014 | 1454.9 | decayed linear attention (3,316), linear attention (4,724), unclassified (6,388) | `S' = (|tanh(tanh(k))|·(<v, tanh(v)>·v)⊗(tanh(tanh(k))) + <v, tanh(v)>·<v, tanh(v)>·S)` |
| 5 | unclassified | 0.626 ±0.014 | 1605.3 | unclassified (884), decayed linear attention (2,292), linear attention (30,068), gated delta rule (1,095,540), delta rule (1,096,436) | `S' = (((v - S·tanh(tanh(tanh(tanh(k))))))⊗(|tanh(tanh(tanh(tanh(k))))|·tanh(tanh(|tanh(tanh(tanh(tanh(k))))|·tanh(` |
| 6 | unclassified | 0.641 ±0.014 | 5005.1 | decayed linear attention (1,012), linear attention (3,316), unclassified (5,364) | `S' = (((tanh(v))⊗(k) - P1) - ((((tanh(v))⊗(k) + (P1 + (tanh(v))⊗(k))))((tanh(tanh(tanh(k))))⊗((0 - tanh(tanh(tanh(` |
| 7 | unclassified | 0.512 ±0.014 | 941.3 | decayed linear attention (4,084), unclassified (12,276), linear attention (12,276) | `S' = ((v)⊗(norm(tanh(tanh((k + k))))) + 0.880·S)` |
| 8 | decayed linear attention | 0.510 ±0.014 | 1211.6 | unclassified (1,140), decayed linear attention (2,548), linear attention (3,060) | `S' = ((v)⊗(tanh(tanh(tanh(k)))) - 0.869·(0 - S))` |
| 9 | unclassified | 0.667 ±0.013 | 3740.7 | decayed linear attention (2,164), linear attention (12,020), unclassified (15,092), gated delta rule (724,084), delta rule (725,108) | `S' = ((0.888·(v)⊗(k) + (0.888·0.888·(v)⊗(k) + (S + (P1)ᵀ))) - ((0.888·(v)⊗(k) + (0.888·0.888·(v)⊗(k) + (S + (P1)ᵀ)` |
| 10 | unclassified | 0.514 ±0.014 | 1789.2 | unclassified (3,188), decayed linear attention (3,828), linear attention (12,788) | `S' = ((0.855·P1 + (tanh(v))⊗(tanh(k))) + <(tanh(v) - (k ⊙ k)), (tanh(v) - (k ⊙ k))>·(((tanh(v))⊗(tanh(k)) + P1) + ` |
| 11 | delta rule | 0.619 ±0.014 | 745.5 | decayed linear attention (1,908), unclassified (14,196), gated delta rule (1,452,148), delta rule (1,453,300) | `S' = (((tanh(v) - P1·tanh(k)))⊗(tanh(tanh(k))) + S)` |
| 12 | delta rule | 0.627 ±0.014 | 1687.9 | unclassified (756), decayed linear attention (1,652), linear attention (2,548), gated delta rule (47,604), delta rule (51,188) | `S' = ((S + ((tanh(v) + P1·(k + k)))⊗((k + k))) + -0.146·((tanh(v) + P1·(k + k)))⊗((k + k)))` |
| 13 | unclassified | 0.623 ±0.014 | 1943.0 | decayed linear attention (5,748), unclassified (9,588), linear, not error-correcting (46,708) | `S' = ((tanh(|tanh(tanh(<(k + 0), tanh(tanh(k))>·tanh(tanh(k))))|·(v + tanh((0 - S)·tanh(<(k + 0), tanh(tanh(k))>·t` |
| 14 | unclassified | 0.515 ±0.014 | 2901.8 | unclassified (884), decayed linear attention (1,012) | `S' = (0.646·(<(v ⊙ v), P1·(v ⊙ v)>·P1)ᵀ + (<(v ⊙ v), P1·(v ⊙ v)>·P1 - (P1 - (v)⊗(|tanh(tanh(k))|·(k + tanh(k))))))` |
| 15 | unclassified | 0.512 ±0.014 | 919.6 | decayed linear attention (1,780), unclassified (9,204), linear attention (10,100) | `S' = 0.880·((v)⊗(norm(tanh(tanh((k + k))))) + S)` |
| 16 | unclassified | 0.621 ±0.014 | 1621.7 | decayed linear attention (4,212), unclassified (8,052), linear attention (9,076) | `S' = ((v)⊗((tanh(k) + tanh(k))) - (P1 - S))` |

- decayed linear attention: seen in 16/16 seeds (median 2,548 candidates), final rule in 2/16
- delta + Kronecker mix: seen in 1/16 seeds (median 12,020 candidates), final rule in 0/16
- delta rule: seen in 5/16 seeds (median 725,108 candidates), final rule in 2/16
- gated delta rule: seen in 5/16 seeds (median 724,084 candidates), final rule in 0/16
- linear attention: seen in 13/16 seeds (median 10,100 candidates), final rule in 0/16
- linear, not error-correcting: seen in 2/16 seeds (median 46,708 candidates), final rule in 0/16
- unclassified: seen in 16/16 seeds (median 8,052 candidates), final rule in 12/16

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 1 | 22,900 | 79,988 | 80,884 | 79,348 |
| 2 | 13,428 | 170,868 | 198,644 | 133,108 |
| 3 | 9,972 | – | – | – |
| 4 | 4,724 | – | – | – |
| 5 | 30,068 | 1,095,796 | 1,103,476 | 1,095,028 |
| 6 | 3,316 | 18,676 | 25,844 | 17,908 |
| 7 | 12,276 | – | – | – |
| 8 | 3,060 | – | – | – |
| 9 | 12,020 | 724,212 | 725,108 | 723,060 |
| 10 | 12,788 | – | – | – |
| 11 | 14,452 | 1,453,300 | 1,454,068 | 1,452,148 |
| 12 | 2,548 | 49,396 | 49,780 | 46,964 |
| 13 | 45,812 | 45,940 | 56,948 | 45,940 |
| 14 | 9,460 | – | – | 514,548 |
| 15 | 10,100 | – | – | – |
| 16 | 9,076 | 425,716 | 426,868 | 409,716 |

# v3-noaddnode: 16 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
    add-node mutation: off  reciprocal op: on  persistent registers: 1 matrix, 0 vector
    candidates: 1500020  real evaluations (after cache): 326409  time: 341s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|
| 1 | linear attention | 0.814 ±0.014 | unclassified (1,780), decayed linear attention (2,548), linear, not error-correcting (15,092), linear attention (68,468) | `S' = σ(0)·1.915·(S + (v)⊗(k))` |
| 2 | gated delta rule | 0.973 ±0.006 | unclassified (756), decayed linear attention (1,780), linear, not error-correcting (7,540), linear attention (10,100), delta rule (803,188), gated delta rule (804,212) | `S' = (1.108·S + (|tanh(v)|·|tanh(v)|·(v - S·tanh(k)))⊗(tanh(tanh(k))))` |
| 3 | linear attention | 0.818 ±0.013 | unclassified (1,780), decayed linear attention (2,804), linear attention (6,900) | `S' = (|tanh(v)|·S + |tanh(norm(tanh(v)))|·(tanh(norm(tanh(v))))⊗(k))` |
| 4 | linear attention | 0.814 ±0.014 | decayed linear attention (1,396), linear, not error-correcting (3,444), unclassified (10,356), linear attention (13,044) | `S' = ((v)⊗(k) - 0.958·(0 - S))` |
| 5 | linear attention | 0.814 ±0.014 | unclassified (6,132), decayed linear attention (6,260), linear, not error-correcting (7,796), linear attention (13,428) | `S' = (0.958·S + (v)⊗(k))` |
| 6 | linear attention | 0.819 ±0.013 | decayed linear attention (884), linear, not error-correcting (5,492), linear attention (6,004) | `S' = (σ((3.156 + <v, k>))·(S + (v)⊗(k)) - σ(0)·(v)⊗(k))` |
| 7 | linear attention | 0.814 ±0.014 | unclassified (1,780), decayed linear attention (2,676), linear, not error-correcting (5,748), linear attention (25,972) | `S' = 0.958·(S + (v)⊗(k))` |
| 8 | linear attention | 0.814 ±0.014 | unclassified (9,844), decayed linear attention (10,228), linear attention (17,652) | `S' = 0.958·((v)⊗(k) + S)` |
| 9 | linear attention | 0.812 ±0.014 | decayed linear attention (3,572), linear, not error-correcting (4,468), unclassified (11,380), linear attention (30,836) | `S' = ((v)⊗((tanh(k) + k)) - <k, tanh(k)>·(0 - S))` |
| 10 | gated delta rule | 0.967 ±0.006 | decayed linear attention (1,780), unclassified (3,444), linear attention (13,684), delta rule (425,076), gated delta rule (425,460) | `S' = ((((0 - S))((tanh(k))⊗(tanh(k))))((tanh(k))⊗(tanh(k))) + ((v)⊗(tanh(k)) - -1.138·S))` |
| 11 | gated delta rule | 0.965 ±0.006 | unclassified (1,524), decayed linear attention (1,908), linear, not error-correcting (3,956), linear attention (10,996), delta rule (610,932), gated delta rule (875,252) | `S' = (0.567·(((v)⊗(tanh(k)) + (S + 0)) - ((S + 0))((tanh(tanh(k)))⊗(tanh(tanh(k))))) + 0.567·(((v)⊗(tanh(k)) + (S ` |
| 12 | gated delta rule | 0.973 ±0.006 | unclassified (9,460), decayed linear attention (9,716), linear, not error-correcting (15,988), linear attention (67,700), delta rule (73,716), gated delta rule (112,628) | `S' = (((v - tanh(S·tanh(k))))⊗(0.897·tanh(k)) + 1.107·S)` |
| 13 | linear attention | 0.814 ±0.014 | decayed linear attention (884), linear, not error-correcting (3,444), linear attention (26,612) | `S' = ((v)⊗(k) - 0.958·(0 - S))` |
| 14 | unclassified | 0.824 ±0.013 | unclassified (884), decayed linear attention (1,780), linear, not error-correcting (2,932), linear attention (34,292) | `S' = ((((((v)⊗(k) + σ(3.490)·S))((v)⊗(k)))((v)⊗(k)))((((v)⊗(k) + σ(3.490)·S))((v)⊗(k))) - (((((v)⊗(k) + σ(3.490)·S` |
| 15 | linear attention | 0.814 ±0.014 | decayed linear attention (628), linear, not error-correcting (3,060), unclassified (9,844), linear attention (36,980) | `S' = 0.958·((v)⊗(k) + S)` |
| 16 | gated delta rule | 0.970 ±0.006 | decayed linear attention (4,212), unclassified (8,436), linear attention (29,044), delta rule (49,012), linear, not error-correcting (51,828), gated delta rule (374,004) | `S' = ((0.554·S + 0.554·S) + ((v - S·tanh(tanh(k))))⊗(tanh(tanh(tanh(k)))))` |

- decayed linear attention: seen in 16/16 seeds (median 2,548 candidates), final rule in 0/16
- delta rule: seen in 5/16 seeds (median 425,076 candidates), final rule in 0/16
- gated delta rule: seen in 5/16 seeds (median 425,460 candidates), final rule in 5/16
- linear attention: seen in 16/16 seeds (median 25,972 candidates), final rule in 10/16
- linear, not error-correcting: seen in 13/16 seeds (median 5,492 candidates), final rule in 0/16
- unclassified: seen in 14/16 seeds (median 6,132 candidates), final rule in 1/16

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 1 | 68,468 | – | – | 68,468 |
| 2 | 10,100 | 803,956 | 804,212 | 10,100 |
| 3 | 6,900 | – | – | 6,900 |
| 4 | 13,044 | – | – | 13,044 |
| 5 | 13,428 | – | – | 13,428 |
| 6 | 6,004 | – | – | 6,004 |
| 7 | 25,972 | – | – | 25,972 |
| 8 | 17,652 | – | – | 17,652 |
| 9 | 30,836 | – | – | 30,836 |
| 10 | 13,684 | 425,332 | 426,100 | 13,684 |
| 11 | 10,996 | 610,292 | 611,316 | 10,996 |
| 12 | 67,956 | 67,956 | 74,228 | 67,700 |
| 13 | 26,612 | – | – | 26,612 |
| 14 | 34,292 | – | – | 34,292 |
| 15 | 36,980 | – | – | 36,980 |
| 16 | 29,044 | 49,012 | 71,028 | 29,044 |

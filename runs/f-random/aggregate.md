# f-random: 16 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 870418  time: 176s  pop: 500  tournament: 10
    commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | wall s | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|---|
| 1 | linear attention | 0.772 ±0.015 | 176.4 | decayed linear attention (628), unclassified (13,684), linear attention (14,196) | `S' = (S + (v)⊗(k))` |
| 2 | linear attention | 0.772 ±0.015 | 180.1 | unclassified (628), decayed linear attention (628), linear attention (17,908) | `S' = (S + (v)⊗(k))` |
| 3 | linear attention | 0.772 ±0.015 | 179.3 | unclassified (628), linear attention (1,780) | `S' = ((v)⊗(k) + S)` |
| 4 | linear attention | 0.772 ±0.015 | 178.3 | unclassified (628), decayed linear attention (884), linear attention (6,388) | `S' = (S + (v)⊗(k))` |
| 5 | linear attention | 0.772 ±0.015 | 177.1 | decayed linear attention (756), unclassified (2,420), linear attention (45,940) | `S' = ((v)⊗(k) + S)` |
| 6 | linear attention | 0.772 ±0.015 | 177.4 | unclassified (756), decayed linear attention (884), linear attention (45,428) | `S' = (S + (v)⊗(k))` |
| 7 | linear attention | 0.772 ±0.015 | 177.8 | decayed linear attention (628), unclassified (7,412), linear attention (28,532) | `S' = ((v)⊗(k) + S)` |
| 8 | linear attention | 0.772 ±0.015 | 177.4 | unclassified (628), decayed linear attention (756), linear attention (5,364) | `S' = (S + (v)⊗(k))` |
| 9 | linear attention | 0.772 ±0.015 | 176.7 | unclassified (628), decayed linear attention (628), linear attention (12,532) | `S' = ((v)⊗(k) + S)` |
| 10 | linear attention | 0.772 ±0.015 | 176.0 | unclassified (756), decayed linear attention (756), linear attention (42,100) | `S' = ((v)⊗(k) + S)` |
| 11 | linear attention | 0.772 ±0.015 | 177.8 | unclassified (628), decayed linear attention (1,652), linear attention (7,412) | `S' = ((v)⊗(k) + S)` |
| 12 | linear attention | 0.772 ±0.015 | 178.7 | decayed linear attention (628), unclassified (2,164), linear attention (5,108) | `S' = ((v)⊗(k) + S)` |
| 13 | linear attention | 0.772 ±0.015 | 176.2 | decayed linear attention (628), unclassified (3,060), linear attention (10,356) | `S' = (S + (v)⊗(k))` |
| 14 | linear attention | 0.772 ±0.015 | 176.3 | unclassified (628), decayed linear attention (1,652), linear attention (43,508) | `S' = ((v)⊗(k) + S)` |
| 15 | linear attention | 0.772 ±0.015 | 176.2 | decayed linear attention (884), linear attention (4,980) | `S' = (S + (v)⊗(k))` |
| 16 | linear attention | 0.772 ±0.015 | 176.6 | unclassified (628), decayed linear attention (884), linear attention (10,356) | `S' = (S + (v)⊗(k))` |

- decayed linear attention: seen in 15/16 seeds (median 756 candidates), final rule in 0/16
- linear attention: seen in 16/16 seeds (median 12,532 candidates), final rule in 16/16
- unclassified: seen in 15/16 seeds (median 628 candidates), final rule in 0/16

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 1 | 14,196 | – | – | 14,196 |
| 2 | 17,908 | – | – | 17,908 |
| 3 | 1,780 | – | – | 1,780 |
| 4 | 6,388 | – | – | 6,388 |
| 5 | 45,940 | – | – | 45,940 |
| 6 | 45,428 | – | – | 45,428 |
| 7 | 28,532 | – | – | 28,532 |
| 8 | 5,364 | – | – | 5,364 |
| 9 | 12,532 | – | – | 12,532 |
| 10 | 42,100 | – | – | 42,100 |
| 11 | 7,412 | – | – | 7,412 |
| 12 | 5,108 | – | – | 5,108 |
| 13 | 10,356 | – | – | 10,356 |
| 14 | 43,508 | – | – | 43,508 |
| 15 | 4,980 | – | – | 4,980 |
| 16 | 10,356 | – | – | 10,356 |

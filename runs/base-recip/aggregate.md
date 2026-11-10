# base-recip (run as v3, renamed on merge): 16 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
    add-node mutation: on  reciprocal op: on  persistent registers: 1 matrix, 0 vector
    candidates: 1500020  real evaluations (after cache): 368281  time: 388s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|
| 1 | linear attention | 0.817 ±0.013 | unclassified (5,364), decayed linear attention (10,228), linear, not error-correcting (10,868), linear attention (180,468) | `S' = (<tanh(v), v>·S + (tanh(tanh(v)))⊗(k))` |
| 2 | linear attention | 0.814 ±0.014 | unclassified (1,268), linear attention (3,956), decayed linear attention (38,772) | `S' = 0.958·(S + (v)⊗(k))` |
| 3 | unclassified | 0.969 ±0.006 | unclassified (628), linear, not error-correcting (1,268), linear attention (3,188), gated delta rule (857,588) | `S' = 1.115·(((v)⊗(tanh(tanh(tanh(tanh(k))))) + S) - ((((v)⊗(tanh(tanh(tanh(tanh(k))))) + S))((tanh(tanh(tanh(k))))` |
| 4 | gated delta rule | 0.967 ±0.006 | unclassified (7,284), decayed linear attention (9,460), linear, not error-correcting (10,996), linear attention (16,372), delta rule (16,884), gated delta rule (1,448,564) | `S' = ((tanh((0.381·v + (0 - S)·tanh(k))))⊗(tanh(tanh(tanh(k)))) - 1/(|tanh(tanh(k))|)·(0 - S))` |
| 5 | gated delta rule | 0.971 ±0.006 | decayed linear attention (4,980), linear, not error-correcting (5,492), unclassified (6,388), linear attention (11,252), delta rule (1,106,932), gated delta rule (1,107,572) | `S' = 1.125·(S + (((norm(tanh(v)) - tanh(S·tanh(k))) - (tanh(tanh(k)) - tanh(tanh(tanh(k))))))⊗(tanh(tanh(tanh(k)))` |
| 6 | linear attention | 0.821 ±0.013 | decayed linear attention (628), linear, not error-correcting (2,292), unclassified (4,596), linear attention (8,692) | `S' = (((v)⊗(k) + 0.955·S) + (0.955·(((tanh(k) ⊙ tanh(k)) - k))⊗((tanh(k) ⊙ tanh(k))))(0.955·(((tanh(k) ⊙ tanh(k)) ` |
| 7 | linear attention | 0.817 ±0.013 | unclassified (756), decayed linear attention (1,012), linear attention (6,260) | `S' = (<tanh(v), v>·S + (tanh(tanh(v)))⊗(k))` |
| 8 | linear attention | 0.817 ±0.013 | unclassified (3,828), decayed linear attention (4,596), linear, not error-correcting (5,620), linear attention (16,500) | `S' = |tanh(v)|·(S + (tanh(norm(tanh(v))))⊗(k))` |
| 9 | gated delta rule | 0.973 ±0.006 | unclassified (3,700), linear attention (20,468), decayed linear attention (541,812), delta rule (735,348), gated delta rule (951,796) | `S' = ((((v)⊗(tanh(tanh(k))) + S) - 0.675·(S)((k)⊗(k))) + 0.097·(((v)⊗(tanh(tanh(k))) + S) - 0.675·(S)((k)⊗(k))))` |
| 10 | linear attention | 0.814 ±0.014 | decayed linear attention (2,036), unclassified (2,676), linear attention (10,740) | `S' = 0.958·((v)⊗(k) + S)` |
| 11 | linear attention | 0.814 ±0.014 | unclassified (6,900), decayed linear attention (7,540), linear attention (42,100) | `S' = ((v)⊗(k) - 0.958·(0 - S))` |
| 12 | gated delta rule | 0.975 ±0.005 | unclassified (3,572), decayed linear attention (4,212), linear attention (37,236), delta rule (154,996), gated delta rule (167,796) | `S' = (((tanh(v) - S·tanh(k)))⊗(0.751·k) + 1.099·((v)⊗((tanh(k) - k)) + S))` |
| 13 | linear attention | 0.817 ±0.013 | decayed linear attention (1,780), linear, not error-correcting (3,060), unclassified (3,188), linear attention (9,332) | `S' = ((tanh(tanh(v)))⊗(k) - (0 - <tanh(v), v>·S))` |
| 14 | linear attention | 0.817 ±0.013 | unclassified (1,396), decayed linear attention (1,780), linear, not error-correcting (2,804), linear attention (13,172) | `S' = ((tanh(tanh(v)))⊗(k) + <v, tanh(v)>·S)` |
| 15 | linear attention | 0.814 ±0.014 | decayed linear attention (1,396), linear, not error-correcting (3,572), unclassified (5,236), linear attention (25,844) | `S' = (0.958·S + (v)⊗(k))` |
| 16 | linear attention | 0.829 ±0.013 | decayed linear attention (3,188), linear, not error-correcting (3,828), unclassified (5,364), linear attention (46,324) | `S' = (<k, tanh(k)>·S + (<k, tanh(k)>·v)⊗((((tanh(k))⊗((v ⊙ (tanh(k) + 0.569·v))))(<k, tanh(k)>·S)·norm(tanh(k)) + ` |

- decayed linear attention: seen in 15/16 seeds (median 4,212 candidates), final rule in 0/16
- delta rule: seen in 4/16 seeds (median 735,348 candidates), final rule in 0/16
- gated delta rule: seen in 5/16 seeds (median 951,796 candidates), final rule in 4/16
- linear attention: seen in 16/16 seeds (median 16,372 candidates), final rule in 11/16
- linear, not error-correcting: seen in 10/16 seeds (median 3,828 candidates), final rule in 0/16
- unclassified: seen in 16/16 seeds (median 3,828 candidates), final rule in 1/16

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 1 | 180,724 | – | – | 180,468 |
| 2 | 3,956 | – | – | 3,956 |
| 3 | 3,188 | 835,572 | 836,468 | 3,188 |
| 4 | 16,372 | 16,884 | 57,716 | 16,244 |
| 5 | 11,252 | 1,107,316 | 1,107,700 | 11,252 |
| 6 | 8,692 | – | – | 8,692 |
| 7 | 6,260 | – | – | 6,260 |
| 8 | 16,500 | – | – | 16,500 |
| 9 | 20,852 | 734,580 | 737,908 | 7,924 |
| 10 | 10,740 | – | – | 10,740 |
| 11 | 42,100 | – | – | 42,100 |
| 12 | 37,236 | 154,996 | 156,148 | 37,236 |
| 13 | 9,332 | – | – | 9,332 |
| 14 | 13,172 | – | – | 13,172 |
| 15 | 25,844 | – | – | 25,844 |
| 16 | 46,324 | – | – | 45,940 |

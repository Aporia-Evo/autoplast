# k-plain2m: 32 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 2100084  real evaluations (after cache): 1380176  time: 5151s  pop: 500  tournament: 10
    commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | wall s | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|---|
| 1 | decayed linear attention | 0.517 ±0.014 | 5152.8 | unclassified (5,364), decayed linear attention (9,332), linear, not error-correcting (11,764), linear attention (70,900) | `S' = |tanh(norm(tanh((P2·(0 + v) ⊙ k))))|·(((0 + v))⊗(tanh(k)) + |tanh((0 + v))|·S)` |
| 2 | unclassified | 0.676 ±0.013 | 4749.1 | unclassified (1,268), decayed linear attention (2,164), linear attention (4,596) | `S' = (((P2 - P1) - ((P2 - P1)·tanh(tanh(k)))⊗(tanh(tanh(tanh(k))))) + |(P2 - P1)·tanh(tanh(k))|·(((P2 - P1) - ((P2` |
| 3 | unclassified | 0.634 ±0.014 | 8252.8 | unclassified (628), linear, not error-correcting (1,268), decayed linear attention (1,524), linear attention (8,564), delta rule (340,212) | `S' = (1.009·(S + (tanh(v))⊗(k)) - 0.146·((S + (tanh(v))⊗(k)))((((k + k))⊗(tanh((k + k))) - (P2)(((k + k))⊗(tanh((k` |
| 4 | unclassified | 0.628 ±0.014 | 3009.3 | unclassified (3,828), decayed linear attention (4,468) | `S' = (((((((P1 - S)·(0 - P1)·k ⊙ norm(tanh(tanh(v)))) + tanh(tanh(v))) + (0 - P1)·k))⊗(k) + (((((P1 - S)·(0 - P1)·` |
| 5 | unclassified | 0.627 ±0.014 | 1873.0 | decayed linear attention (4,980), linear attention (8,948), unclassified (763,380), delta rule (766,068) | `S' = ((S + 0.702·(tanh(1.406·v))⊗(k)) + ((tanh(tanh(1.406·v)) - P2·tanh(k)))⊗(tanh(k)))` |
| 6 | unclassified | 0.689 ±0.013 | 10250.7 | decayed linear attention (628), unclassified (10,996) | `S' = …` |
| 7 | unclassified | 0.726 ±0.013 | 2360.9 | unclassified (756), decayed linear attention (1,012), linear attention (18,036), delta rule (66,292), gated delta rule (66,804) | `S' = (-0.052·1/(-0.052)·(P2 + S) + (((((v + v) + (v + v)) + ((v + v) + (v + v))) - 0.810·(P2 + S)·norm(k)))⊗(norm(` |
| 8 | unclassified | 0.510 ±0.014 | 1355.4 | unclassified (3,828), decayed linear attention (4,596), linear attention (462,964) | `S' = ((v)⊗(tanh((tanh(k) + k))) - (-1.862·S + S))` |
| 9 | unclassified | 0.863 ±0.010 | 3402.6 | unclassified (3,700), linear attention (19,956), decayed linear attention (26,356), gated delta rule (248,692), delta rule (249,588) | `S' = ((P2 + ((((norm(tanh(v)) + norm(tanh(v))) + (norm(tanh(v)) + norm(tanh(v)))) + (norm(tanh(v)) + norm(tanh(v))` |
| 10 | unclassified | 0.644 ±0.014 | 9080.1 | decayed linear attention (2,036), unclassified (3,572), linear attention (6,772) | `S' = ((…)((0.430·((P2 - (v)⊗(k)) - (P1)((P2 - (v)⊗(k)))) + ((P2 - (v)⊗(k)) - (P1)((P2 - (v)⊗(k)))))) - ((P2 - (v)⊗` |
| 11 | unclassified | 0.518 ±0.014 | 1867.7 | decayed linear attention (4,724), unclassified (10,356), linear attention (13,428) | `S' = (<tanh(k), tanh(k)>·S - (v)⊗(tanh(norm(tanh((P1·(k + k) - tanh(k)))))))` |
| 12 | unclassified | 0.648 ±0.014 | 2971.0 | unclassified (3,572), decayed linear attention (4,212), gated delta rule (9,076), delta + Kronecker mix (14,964) | `S' = ((P2)(S) - ((norm((<norm(S·k), ((S·k - tanh(v)) + S·k)> + <S·k, k>)·tanh(tanh((norm(tanh(((tanh(v) - (S·k - t` |
| 13 | unclassified | 0.668 ±0.013 | 3408.9 | decayed linear attention (1,780), unclassified (2,676) | `S' = ((((norm(v))⊗(k) + ((norm(v))⊗(k) + (P1 - P2))) + ((norm(v))⊗(k) + ((norm(v))⊗(k) + (P1 - P2)))) - 0.971·(((n` |
| 14 | unclassified | 0.523 ±0.014 | 2810.1 | unclassified (1,396), decayed linear attention (1,780), linear attention (4,852) | `S' = ((P1 - P2) + (((v)⊗(k) + (v)⊗(k)) + (((v)⊗(k) + (v)⊗(k)) + ((v)⊗(k) - P2))))` |
| 15 | unclassified | 0.663 ±0.014 | 2807.3 | decayed linear attention (1,396), unclassified (8,948), linear attention (18,548), delta rule (19,828) | `S' = (P1 + (((v - P2·tanh(k)))⊗(norm(tanh(k))) + S))` |
| 16 | unclassified | 0.635 ±0.014 | 2140.6 | decayed linear attention (3,188), unclassified (8,436), linear attention (11,380), delta rule (11,764), linear, not error-correcting (12,788) | `S' = ((((v - S·k) + P2·(v - S·k)))⊗((σ(0)·norm((k - ((S·k ⊙ S·S·k) + (v ⊙ S·S·k)))) - ((S·k ⊙ S·S·k) + (v ⊙ S·S·k)` |
| 17 | unclassified | 0.623 ±0.014 | 2937.3 | decayed linear attention (884), unclassified (4,084) | `S' = ((P1 - P2) + (tanh(v))⊗(tanh(norm(tanh(tanh(k))))))` |
| 18 | unclassified | 0.568 ±0.014 | 1619.7 | decayed linear attention (2,676), unclassified (4,980), linear attention (6,772) | `S' = (0.897·S + (tanh(v))⊗(norm((k + P2·tanh(k)))))` |
| 19 | decayed linear attention | 0.515 ±0.014 | 1641.4 | unclassified (756), decayed linear attention (1,140), linear attention (14,452) | `S' = (<tanh(norm((((v ⊙ v) ⊙ 1.806·k) + k))), tanh(norm((((v ⊙ v) ⊙ 1.806·k) + k)))>·S + (<tanh(norm((((v ⊙ v) ⊙ 1` |
| 20 | unclassified | 0.521 ±0.014 | 4848.8 | unclassified (4,724), decayed linear attention (5,492) | `S' = 0.875·(S + ((0 + v))⊗(norm(tanh(((tanh((k + k)) + (P1)(P2)·k) - (tanh((0 + v)) ⊙ norm((P1)(P2)·k)))))))` |
| 21 | unclassified | 0.578 ±0.014 | 2237.5 | decayed linear attention (756), unclassified (5,492) | `S' = (((0.438·P2 + 0.869·1/(0.495)·(v)⊗(k)) + (0.438·P2 + 0.869·1/(0.495)·(v)⊗(k))) - ((0.438·P2 + 0.869·1/(0.495)` |
| 22 | unclassified | 0.519 ±0.014 | 2510.4 | unclassified (4,852), decayed linear attention (6,260), linear attention (12,404) | `S' = ((v)⊗((((P2)ᵀ·P1·tanh(k) + ((norm(tanh(k)) + tanh(k)) + (P2)ᵀ·P1·tanh(k))) - tanh(P1·P1·tanh(k)))) + 0.896·S)` |
| 23 | unclassified | 0.622 ±0.014 | 2397.5 | decayed linear attention (1,396), unclassified (6,132), linear attention (7,924) | `S' = ((tanh(v))⊗(tanh(k)) - (P2 - (S + P1)))` |
| 24 | unclassified | 0.654 ±0.014 | 2801.7 | decayed linear attention (628), linear attention (7,796), unclassified (12,148), gated delta rule (1,092,596), delta rule (1,093,108) | `S' = ((P2 - (tanh(P2·tanh(tanh(tanh(k)))))⊗(tanh(tanh(tanh(k))))) + σ(2.319)·(tanh(tanh(v)))⊗(norm(((tanh(tanh(v))` |
| 25 | unclassified | 0.667 ±0.013 | 8527.2 | decayed linear attention (1,140), linear, not error-correcting (2,036), unclassified (6,516), linear attention (8,436), delta rule (828,532) | `S' = (((v)⊗((k + k)))(((k + k))⊗((k + k))) + (((k + k))⊗(tanh(k)) + ((P2 + (S + (v)⊗((k + k)))) - 0.424·0.424·((P2` |
| 26 | decayed linear attention | 0.511 ±0.014 | 1269.8 | decayed linear attention (1,780), unclassified (2,804), linear attention (5,364) | `S' = <tanh(tanh(tanh(v))), norm(tanh(tanh(v)))>·((v)⊗(tanh(k)) + S)` |
| 27 | unclassified | 0.681 ±0.013 | 4783.3 | decayed linear attention (1,396), unclassified (12,404), linear attention (14,068), gated delta rule (74,740), delta rule (75,380), delta + Kronecker mix (78,068) | `S' = (σ(<tanh((P1 - (S + P2))·tanh(tanh(k))), norm((tanh((P1 - (S + P2))·tanh(tanh(k))) + tanh(tanh(v))))>·<tanh((` |
| 28 | unclassified | 0.615 ±0.014 | 2257.7 | unclassified (884), decayed linear attention (1,524) | `S' = ((((0.115·((v - -1.892·k) - (tanh((((P2 - P1))ᵀ·k + k)) + (((P2 - P1))ᵀ·k + k))) + (0.115·((v - -1.892·k) - (` |
| 29 | unclassified | 0.512 ±0.014 | 3504.4 | decayed linear attention (1,780), unclassified (3,956), linear attention (5,108) | `S' = ((P1)(((v)⊗(tanh(k)) + (v)⊗(tanh(k)))) + (((v)⊗(tanh(k)) + (v)⊗(tanh(k))) + ((v)⊗(tanh(k)) + P2)))` |
| 30 | unclassified | 0.642 ±0.014 | 5604.3 | decayed linear attention (2,164), unclassified (2,420), linear attention (5,876), delta rule (192,628), linear, not error-correcting (193,268) | `S' = (((v)⊗(k) + S) + σ(0)·<tanh(tanh((k - P2·σ(0)·k))), (k - P2·σ(0)·k)>·|((v)⊗(k) + S)·tanh((k - P2·σ(0)·k))|·(0` |
| 31 | unclassified | 0.633 ±0.014 | 6241.5 | decayed linear attention (2,164), unclassified (6,772) | `S' = (σ(0)·(((S + P2) + (((norm(tanh(v)) + (norm(tanh(v)) + norm(tanh(v)))) + tanh(v)))⊗(k)) + (((norm(tanh(v)) + ` |
| 32 | unclassified | 0.600 ±0.014 | 4067.2 | decayed linear attention (4,596), unclassified (9,844), linear, not error-correcting (10,996), linear attention (33,780) | `S' = ((tanh(v))⊗(tanh(k)) + 0.999·0.999·(S - (S)(P2)))` |

- decayed linear attention: seen in 32/32 seeds (median 2,036 candidates), final rule in 3/32
- delta + Kronecker mix: seen in 2/32 seeds (median 78,068 candidates), final rule in 0/32
- delta rule: seen in 10/32 seeds (median 249,588 candidates), final rule in 0/32
- gated delta rule: seen in 5/32 seeds (median 74,740 candidates), final rule in 0/32
- linear attention: seen in 23/32 seeds (median 8,948 candidates), final rule in 0/32
- linear, not error-correcting: seen in 6/32 seeds (median 11,764 candidates), final rule in 0/32
- unclassified: seen in 32/32 seeds (median 4,724 candidates), final rule in 29/32

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 1 | 70,900 | – | – | 147,700 |
| 2 | 4,596 | 76,788 | 83,060 | 76,404 |
| 3 | 8,564 | 335,860 | 339,828 | 335,348 |
| 4 | 10,100 | 274,676 | 275,444 | 273,524 |
| 5 | 8,948 | 766,068 | 767,220 | 763,380 |
| 6 | 11,636 | 164,980 | 194,676 | 162,932 |
| 7 | 18,036 | 67,060 | 67,572 | 65,268 |
| 8 | 462,196 | – | – | – |
| 9 | 19,956 | 248,948 | 257,524 | 85,364 |
| 10 | 6,772 | 41,332 | 42,740 | 24,436 |
| 11 | 13,428 | – | – | 158,580 |
| 12 | 9,460 | 11,636 | 14,964 | 11,636 |
| 13 | 6,388 | 1,498,612 | 2,076,276 | 1,474,292 |
| 14 | 4,852 | – | – | 744,436 |
| 15 | 18,548 | 19,572 | 20,724 | 18,932 |
| 16 | 11,380 | 11,764 | 20,084 | 11,764 |
| 17 | 7,412 | 822,004 | 879,988 | 70,644 |
| 18 | 6,772 | – | – | 949,748 |
| 19 | 14,452 | – | – | 315,764 |
| 20 | 20,468 | – | – | 195,828 |
| 21 | 9,972 | 2,038,516 | – | 1,151,860 |
| 22 | 12,404 | – | – | 211,444 |
| 23 | 7,924 | 1,510,388 | 1,524,084 | 1,508,980 |
| 24 | 7,796 | 1,093,108 | 1,099,508 | 225,780 |
| 25 | 8,436 | 827,252 | 828,404 | 40,820 |
| 26 | 5,364 | – | – | – |
| 27 | 14,068 | 75,380 | 75,892 | 74,740 |
| 28 | 18,676 | 2,086,260 | 2,086,260 | 626,932 |
| 29 | 5,108 | – | – | – |
| 30 | 5,876 | 192,628 | 194,420 | 185,588 |
| 31 | 7,412 | 306,804 | 311,284 | 305,908 |
| 32 | 33,780 | 546,804 | – | 519,156 |

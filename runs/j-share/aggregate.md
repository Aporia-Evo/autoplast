# j-share: 32 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 937470  time: 2815s  pop: 500  tournament: 10
    commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | wall s | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|---|
| 1 | unclassified | 0.642 ±0.014 | 2816.6 | unclassified (5,364), decayed linear attention (8,948), linear, not error-correcting (15,604) | `S' = (σ(0)·S + ((((tanh(v) - P1·norm(k)))⊗(k) + P1) - P2))` |
| 2 | unclassified | 0.651 ±0.014 | 2792.3 | unclassified (1,268), decayed linear attention (2,164) | `S' = (P1 + (P2 + ((v - σ(σ(0))·P2·k))⊗(norm(k))))` |
| 3 | unclassified | 0.618 ±0.014 | 2927.3 | unclassified (628), decayed linear attention (1,268), linear, not error-correcting (1,268), gated delta rule (117,492), delta rule (1,002,740) | `S' = (((1/((0.814 + 0.814)) + -1.015)·(v + P2·(0 + k)))⊗((0 + k)) - (-1.015·(((v + P2·(0 + k)))⊗((0 + k)) - P2) + ` |
| 4 | delta rule | 0.617 ±0.014 | 2772.1 | unclassified (3,828), decayed linear attention (4,468), linear attention (190,452), delta rule (1,006,708) | `S' = ((((S)ᵀ + (k)⊗(v)) - σ(0)·(((k + 0))⊗(k))((S)ᵀ)))ᵀ` |
| 5 | unclassified | 0.672 ±0.013 | 4542.6 | decayed linear attention (4,980), unclassified (6,516), linear attention (7,028) | `S' = ((v)⊗(σ(σ(1/(0)))·norm(k)) + (((P2 - P1))(((0 + norm(k)))⊗(σ(σ(1/(0)))·norm(k))) + P1))` |
| 6 | unclassified | 0.673 ±0.013 | 3014.0 | decayed linear attention (628), unclassified (2,932) | `S' = ((P2·k)⊗(norm((v + k))) - ((P1 - ((v + (P1·k + v)))⊗(k)) + P2))` |
| 7 | unclassified | 0.638 ±0.014 | 2382.7 | unclassified (756), decayed linear attention (1,012), linear, not error-correcting (177,140), delta rule (182,900) | `S' = (((v)⊗(tanh((tanh(k) + tanh(k)))) - (P2 - (v)⊗(tanh((tanh(k) + tanh(k)))))) + (S + P1))` |
| 8 | unclassified | 0.631 ±0.014 | 3172.3 | unclassified (3,828), decayed linear attention (4,596), linear attention (37,492) | `S' = ((0·P1·v)⊗(0) + (σ((0·0 + (0 + 0·0)))·((v)⊗(tanh(k)) + P1) - (P2 - S)))` |
| 9 | unclassified | 0.698 ±0.013 | 2772.8 | unclassified (3,700), decayed linear attention (13,428), delta rule (211,828) | `S' = (((((v)⊗((k + k))·0 - S·tanh(tanh(k))) + 0))⊗(k) - (σ(1/((0 + <k, tanh(tanh(k))>)))·(P2 - (v)⊗((k + k))) - S)` |
| 10 | delta rule | 0.617 ±0.014 | 4580.9 | decayed linear attention (2,036), unclassified (4,468), linear attention (10,740), delta rule (186,228) | `S' = (σ(0)·(((v)⊗((0 - k)) - S))((k)⊗(k)) - ((v)⊗((0 - k)) - S))` |
| 11 | unclassified | 0.668 ±0.013 | 2618.8 | decayed linear attention (4,724), unclassified (7,028) | `S' = (σ((σ(0) + σ(0)))·(S + (P2 - P1)) - (σ((σ(0) + σ(0)))·σ(σ(0))·((0 - v) + ((P2 - P1) + S)·k))⊗(σ(σ(0))·k))` |
| 12 | unclassified | 0.644 ±0.014 | 2640.8 | unclassified (3,572), decayed linear attention (4,212), linear attention (29,428) | `S' = (P1 + ((P1 + (v)⊗((0 + k))) + ((S + (S·(0 - norm(tanh((0 + k)))))⊗(tanh((0 + k)))) - P1)))` |
| 13 | delta rule | 0.603 ±0.014 | 3149.1 | decayed linear attention (1,780), unclassified (3,060), linear attention (4,340), delta rule (525,556) | `S' = (((v - (0.396·S + 0.396·S)·(0 + k)))⊗((0 + k)) + σ((<v, v> + 1/(0.396))·1/(0.396))·S)` |
| 14 | delta + Kronecker mix | 0.627 ±0.014 | 2696.8 | unclassified (1,396), decayed linear attention (1,780), delta rule (115,060), delta + Kronecker mix (549,108) | `S' = ((((v - S·k))⊗(k) + S) - ((0.609·k)⊗(norm(((v - S·k))⊗(k)·0.609·k)))ᵀ)` |
| 15 | unclassified | 0.624 ±0.014 | 2194.9 | decayed linear attention (1,396), unclassified (4,084), linear attention (6,260) | `S' = (((P1·v + (0 + v)))⊗((0 + k)) + (S - σ(0)·P2))` |
| 16 | unclassified | 0.621 ±0.014 | 2946.3 | decayed linear attention (3,188), linear attention (5,364), unclassified (50,164), delta rule (149,876) | `S' = ((P2 + ((v + (v - P1·k)))⊗(k)) + (σ((<(k ⊙ (v - P1·k)), (v - P1·k)> + 0))·(P2 + ((v + (v - P1·k)))⊗(k)) + (P2` |
| 17 | unclassified | 0.659 ±0.014 | 4457.0 | decayed linear attention (884), unclassified (5,876) | `S' = (((v)⊗(k) + P2) - 0.868·(P2)(((0 - k))⊗(0.868·((0 - k) - (0·(0 - k) ⊙ 0)))))` |
| 18 | delta rule | 0.615 ±0.014 | 3201.3 | decayed linear attention (2,676), unclassified (4,084), linear attention (5,748), delta rule (643,956) | `S' = ((S + ((v + v))⊗(k)) - ((S + ((v + v))⊗(k)))((tanh(k))⊗(σ(0)·k)))` |
| 19 | unclassified | 0.658 ±0.014 | 2354.9 | unclassified (756), decayed linear attention (1,140), linear attention (2,804), delta rule (941,940) | `S' = (σ(0.433)·((norm(v) - tanh(S·k)))⊗(tanh(tanh(k))) + 1/(|((P1)((0 - P1))·((norm(v) - tanh(S·k)) - v) + tanh(ta` |
| 20 | unclassified | 0.642 ±0.014 | 2635.3 | unclassified (4,724), decayed linear attention (5,492), linear attention (12,660) | `S' = ((((((v + v) + ((P1 - P2) + 0)·tanh(k)))⊗(k) + P2) + (v)⊗(k)) - (v)⊗(k))` |
| 21 | unclassified | 0.643 ±0.014 | 2834.0 | decayed linear attention (756), unclassified (3,188), linear attention (4,852) | `S' = ((-0.916·((P1 + (v)⊗(k)) - P2)·k)⊗(norm(tanh(k))) - -0.916·((P1 + (v)⊗(k)) - P2))` |
| 22 | unclassified | 0.657 ±0.014 | 2434.0 | unclassified (4,852), decayed linear attention (6,260), linear, not error-correcting (7,668), linear attention (15,604), delta rule (18,164) | `S' = (σ(σ(1/(σ(1/(|k|)))))·((v - (S + ((0)⊗(0) - P2))·norm(tanh(tanh(k)))))⊗(k) + (S + ((0)⊗(0) - P2)))` |
| 23 | unclassified | 0.641 ±0.014 | 4709.5 | decayed linear attention (1,396), unclassified (3,444) | `S' = σ((σ(0) + 0))·(S - σ(0)·(((((S)(P2) + P1) - ((v + v))⊗(k)) + (S)(P2)) + (S)(P2)))` |
| 24 | unclassified | 0.653 ±0.014 | 2978.6 | decayed linear attention (628), unclassified (3,188), linear attention (8,820), delta rule (337,780) | `S' = (((v)⊗(k) - ((S + P2)·(k + 0))⊗(σ(σ(0))·(k + 0))) + (S + P2))` |
| 25 | unclassified | 0.614 ±0.014 | 2402.6 | decayed linear attention (1,140), linear, not error-correcting (2,036), unclassified (2,932), linear attention (11,892) | `S' = ((tanh(v))⊗(k) + (P1 + P2))` |
| 26 | unclassified | 0.653 ±0.014 | 2640.5 | decayed linear attention (1,780), linear, not error-correcting (4,212), unclassified (5,364), delta rule (13,684), delta + Kronecker mix (30,708) | `S' = ((P1 - (((0.293 + 0)·P1·tanh(tanh(k)) - (v - 0)))⊗((tanh(tanh(k)) + k))) - ((P1 - (((0.293 + 0)·P1·tanh(tanh(` |
| 27 | unclassified | 0.671 ±0.013 | 2974.5 | decayed linear attention (1,396), unclassified (3,188), linear attention (5,876) | `S' = (((tanh(σ(0)·(((S - P1))(P2) - (S - P1))·k) - v))⊗(tanh(k)) - (σ(0)·(((S - P1))(P2) - (S - P1)) + (0·(((S - P` |
| 28 | delta rule | 0.617 ±0.014 | 2478.6 | unclassified (884), decayed linear attention (1,524), linear attention (3,060), delta rule (6,260) | `S' = (((S)((0·P2 - 0·P2)) + S) + ((((0 + v) + tanh(0)) + ((S)((0·P2 - 0·P2)) + S)·(σ(0)·k - k)))⊗(k))` |
| 29 | unclassified | 0.604 ±0.014 | 2598.1 | decayed linear attention (1,780), unclassified (3,956), linear attention (11,508) | `S' = (((0 - P2) + ((v + 0))⊗(k)) + ((P2 + ((v + 0))⊗(k))·σ((0 + 0))·(k + 0))⊗((k + 0)))` |
| 30 | unclassified | 0.655 ±0.014 | 3285.8 | decayed linear attention (2,164), unclassified (2,420), linear attention (3,700), delta rule (733,812) | `S' = (|0| + σ(|0|))·(((v)⊗(k) + (P2 - P1)) - ((P2 - P1)·0.620·k)⊗(k))` |
| 31 | unclassified | 0.633 ±0.014 | 2560.6 | decayed linear attention (2,164), linear attention (3,316), unclassified (5,108), linear, not error-correcting (8,308), delta rule (22,644) | `S' = ((σ(0)·((((S - P1) + P1))ᵀ)ᵀ + (S - P1)) + (((((P1)ᵀ - (P1)ᵀ) - (S - P1))·k + (v - norm(0))))⊗(k))` |
| 32 | unclassified | 0.640 ±0.014 | 2377.4 | decayed linear attention (4,596), linear, not error-correcting (6,132), unclassified (7,028), linear attention (8,436) | `S' = ((S + P1) + ((norm(v) - ((S + P1) + 0)·k))⊗(k))` |

- decayed linear attention: seen in 32/32 seeds (median 2,036 candidates), final rule in 0/32
- delta + Kronecker mix: seen in 2/32 seeds (median 549,108 candidates), final rule in 1/32
- delta rule: seen in 16/32 seeds (median 211,828 candidates), final rule in 5/32
- gated delta rule: seen in 1/32 seeds (median 117,492 candidates), final rule in 0/32
- linear attention: seen in 21/32 seeds (median 7,028 candidates), final rule in 0/32
- linear, not error-correcting: seen in 8/32 seeds (median 7,668 candidates), final rule in 0/32
- unclassified: seen in 32/32 seeds (median 3,828 candidates), final rule in 26/32

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 1 | 28,276 | 84,084 | 103,412 | 28,276 |
| 2 | 7,412 | 78,580 | 79,604 | 24,180 |
| 3 | 5,620 | 433,780 | 1,002,740 | 117,492 |
| 4 | 190,452 | 346,740 | 417,652 | 346,740 |
| 5 | 7,028 | 15,348 | 32,500 | 13,556 |
| 6 | 5,364 | 162,804 | 737,140 | 126,068 |
| 7 | 18,932 | 177,140 | 482,292 | 19,700 |
| 8 | 34,804 | 59,380 | 261,108 | 41,204 |
| 9 | 13,428 | 207,732 | 211,828 | 112,884 |
| 10 | 10,740 | 39,156 | 52,340 | 22,644 |
| 11 | 7,796 | 54,772 | 63,348 | 54,004 |
| 12 | 29,428 | 102,132 | 103,028 | 102,132 |
| 13 | 4,340 | 513,652 | – | 171,252 |
| 14 | 17,908 | 115,060 | 117,620 | 52,340 |
| 15 | 6,260 | 13,556 | 53,876 | 13,556 |
| 16 | 5,364 | 60,916 | 149,876 | 51,316 |
| 17 | 36,212 | 66,420 | 104,564 | 46,068 |
| 18 | 5,748 | 298,612 | 1,368,052 | 111,220 |
| 19 | 2,804 | 770,804 | 964,084 | 241,780 |
| 20 | 12,660 | 24,692 | 34,036 | 24,436 |
| 21 | 4,852 | 351,988 | 351,988 | 75,764 |
| 22 | 15,604 | 18,164 | 35,060 | 18,164 |
| 23 | 8,820 | 91,892 | 116,340 | 67,316 |
| 24 | 8,564 | 26,612 | 337,780 | 26,612 |
| 25 | 11,892 | 74,612 | 1,428,596 | 70,132 |
| 26 | 10,356 | 13,044 | 30,708 | 10,868 |
| 27 | 5,876 | 50,804 | 73,716 | 47,348 |
| 28 | 3,060 | 6,260 | 13,940 | 5,364 |
| 29 | 10,868 | 232,692 | – | 45,684 |
| 30 | 3,700 | 733,812 | 733,812 | 342,516 |
| 31 | 3,316 | 7,284 | 98,420 | 7,156 |
| 32 | 8,436 | 57,332 | 57,332 | 51,060 |

# h-share: 32 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 952921  time: 633s  pop: 500  tournament: 10
    commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | wall s | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|---|
| 1 | gated delta rule | 0.970 ±0.006 | 635.0 | decayed linear attention (3,060), linear, not error-correcting (5,236), unclassified (9,716), linear attention (52,724), delta rule (61,684), gated delta rule (95,604) | `S' = ((((0·v - σ((σ(0) + σ(σ(0))))·S·norm(k)) + v))⊗(k) - (σ(0) + σ(σ(0)))·(0 - S))` |
| 2 | delta rule | 0.941 ±0.008 | 554.0 | decayed linear attention (3,316), unclassified (4,084), linear attention (13,812), delta rule (39,412) | `S' = (((norm(v) + (0 + (σ(|S·k|) + 0))·(0 - S)·σ(|S·k|)·k))⊗(tanh((0 + k))) - (0 - S))` |
| 3 | gated delta rule | 0.969 ±0.006 | 675.7 | unclassified (884), decayed linear attention (1,268), linear, not error-correcting (2,164), linear attention (19,572), delta rule (52,724), gated delta rule (195,572) | `S' = (1.092·(0 + S) - σ(σ(1.092))·((1.092·(0 + S)·(k + 0))⊗(k) - ((0 + (0 + v)))⊗((k + 0))))` |
| 4 | unclassified | 0.943 ±0.008 | 761.6 | decayed linear attention (3,316), unclassified (5,364), linear attention (8,180), linear, not error-correcting (44,276) | `S' = ((((norm((v + S·(0 + k))) - S·(0 + k)))⊗((0 + k)) + ((v)⊗(k) + S)) + (((0 ⊙ v) ⊙ (0 ⊙ v)))⊗(v))` |
| 5 | unclassified | 0.945 ±0.008 | 590.9 | unclassified (884), decayed linear attention (2,420), linear attention (25,844), delta rule (41,076) | `S' = (((norm(σ(0)·(v + S·(0 + tanh(k)))) - S·(0 + tanh(k))))⊗((0 + tanh(k))) + ((((v)⊗(tanh(tanh(k))) - 0) + S) + ` |
| 6 | gated delta rule | 0.954 ±0.007 | 1177.0 | decayed linear attention (1,012), linear, not error-correcting (1,268), unclassified (3,444), linear attention (22,260), delta rule (44,916), gated delta rule (62,836) | `S' = ((0 + (0 + -2.209))·0·(k)⊗(norm(k)) - (((S + ((v + 0))⊗(k)) + -2.209·(S + ((v + 0))⊗(k))) + (S)((k)⊗(norm(k))` |
| 7 | linear, not error-correcting | 0.931 ±0.009 | 1177.9 | decayed linear attention (4,084), linear, not error-correcting (4,980), unclassified (5,236), linear attention (25,844), delta rule (29,044) | `S' = ((0 + S) + σ(σ(0))·(tanh((v - tanh(S·tanh(k)))))⊗(norm(k)))` |
| 8 | delta rule | 0.936 ±0.008 | 739.7 | unclassified (1,140), linear attention (3,316), delta rule (33,012) | `S' = ((S + (v)⊗(k)) - ((((|(0 - v)| + -0.548) + 0)·S·(k - 0))⊗(tanh(((k - 0) - norm(norm((0 - v)))))))((v)⊗(k)))` |
| 9 | gated delta rule | 0.960 ±0.007 | 889.1 | decayed linear attention (2,164), linear, not error-correcting (2,804), unclassified (3,828), delta rule (15,220), gated delta rule (1,158,900) | `S' = ((S - ((((S - 0) - 0)·k - v))⊗(k)) + σ(|v|)·0.233·((S - 0) - 0))` |
| 10 | gated delta rule | 0.971 ±0.006 | 764.7 | unclassified (3,188), decayed linear attention (3,828), linear, not error-correcting (4,852), linear attention (105,588), delta rule (334,964), gated delta rule (684,404) | `S' = ((σ(σ(0)) + σ(0))·(S + 0) + σ((σ(σ(0)) + (σ(σ(0)) + σ(0))))·(((v)⊗((k + (σ(σ(0)) + σ(0))·0)))((k)⊗(tanh(k))) ` |
| 11 | delta rule | 0.935 ±0.009 | 677.2 | decayed linear attention (1,908), linear, not error-correcting (2,804), unclassified (4,468), linear attention (14,068), delta rule (30,452) | `S' = ((v)⊗(tanh(k)) - ((S)(((tanh(k) + ((tanh(k) + (tanh(k) - tanh(k))) ⊙ (tanh(k) + (tanh(k) - tanh(k))))))⊗(σ((0` |
| 12 | gated delta rule | 0.954 ±0.007 | 610.2 | unclassified (756), decayed linear attention (2,804), linear attention (3,316), linear, not error-correcting (67,444), delta rule (69,748), gated delta rule (132,468) | `S' = ((((0 + v) - S·(k + 0)))⊗((k + 0)) - ((-0.676·-0.676 + 0)·-0.676·-0.676·(0 - S) - S))` |
| 13 | linear, not error-correcting | 0.957 ±0.007 | 603.4 | decayed linear attention (5,748), unclassified (8,692), linear attention (79,476), delta rule (84,468), gated delta rule (1,053,428), linear, not error-correcting (1,304,180) | `S' = (0.139·S + ((tanh(((v + 0) - S·k)))⊗(k) + S))` |
| 14 | gated delta rule | 0.967 ±0.006 | 647.1 | unclassified (884), decayed linear attention (1,012), linear, not error-correcting (1,652), linear attention (7,924), delta rule (104,948), gated delta rule (680,436) | `S' = ((σ(0)·S + (0 + S)) - (0 + 0.780)·(σ(0)·S + ((v + S·(0 - k)))⊗((0·(v + S·(0 - k)) + (0 - k)))))` |
| 15 | delta + Kronecker mix | 0.964 ±0.006 | 687.1 | decayed linear attention (1,780), linear, not error-correcting (2,676), unclassified (3,828), linear attention (17,268), delta rule (22,132), gated delta rule (235,636), delta + Kronecker mix (1,185,268) | `S' = (σ(0)·σ(0)·(σ(0)·S - (norm((0 - (S·k - v))))⊗(k)) - (((S·k - v))⊗(k) - S))` |
| 16 | gated delta rule | 0.971 ±0.006 | 693.3 | decayed linear attention (4,212), linear, not error-correcting (4,852), unclassified (6,772), linear attention (17,268), gated delta rule (38,772) | `S' = ((-1.438 + σ(σ(0)))·-0.371·(0 + S) + (-1.438 + σ(σ(0)))·((((0 + S)·k + (0 - ((v + v) + v))))⊗(k) - (0 + S)))` |
| 17 | gated delta rule | 0.940 ±0.008 | 789.6 | unclassified (1,140), decayed linear attention (2,676), linear attention (18,804), delta rule (98,932), gated delta rule (597,492) | `S' = (((1.065·((S)((tanh(k))⊗(tanh((0 - tanh(k))))) + S) + (v)⊗(tanh(k))))ᵀ)ᵀ` |
| 18 | delta rule | 0.938 ±0.008 | 718.2 | unclassified (1,012), decayed linear attention (2,036), linear attention (63,476), delta rule (65,012) | `S' = ((((((0 - v) + (0 - v)))⊗(((0 ⊙ 0) - k)) + (((0 - v) + (0 - v)))⊗(((0 ⊙ 0) - k))) - ((σ(0) + 0)·(S·((0 ⊙ 0) -` |
| 19 | unclassified | 0.943 ±0.008 | 727.2 | unclassified (1,268), decayed linear attention (1,524), linear, not error-correcting (2,036), linear attention (5,876), delta rule (61,684) | `S' = (((σ(0·0) + 0) + (σ(0·0) + 0))·((norm(((norm(v))⊗(k) + S)·((v ⊙ 0) - k)) + S·(k - 0)))⊗(norm(((v ⊙ 0) - k))) ` |
| 20 | gated delta rule | 0.961 ±0.007 | 677.4 | decayed linear attention (1,268), linear, not error-correcting (2,036), unclassified (7,412), linear attention (31,476), delta rule (37,364), gated delta rule (930,292) | `S' = ((((v - S·(k + 0)))⊗((k + 0)) + S) - σ(-1.573)·(0 - S))` |
| 21 | unclassified | 0.946 ±0.008 | 801.2 | unclassified (6,004), decayed linear attention (6,516), linear attention (7,028), delta rule (19,188) | `S' = (0.093·S - ((((0 - v))⊗(k) + (S·tanh((k + (k ⊙ (0 - v)))))⊗(norm(tanh((k + (k ⊙ (0 - v))))))) - S))` |
| 22 | unclassified | 0.943 ±0.008 | 718.6 | decayed linear attention (628), linear, not error-correcting (1,908), unclassified (2,676), linear attention (6,132), delta rule (103,924) | `S' = (((norm((S·norm(k) + v)) - S·norm(k)))⊗(k) + (((v)⊗(norm(k)) + S) - 0))` |
| 23 | unclassified | 0.948 ±0.008 | 895.8 | unclassified (13,300), decayed linear attention (14,196), linear attention (19,956), delta rule (66,548) | `S' = (((((k)⊗(v))ᵀ + (k)⊗(v)) + (((k)⊗(v) - S))((k)⊗(norm((k - (0 + 0)))))) + (-0.607 + -0.607)·((k)⊗(v) - S))` |
| 24 | gated delta rule | 0.969 ±0.006 | 686.5 | decayed linear attention (5,236), linear, not error-correcting (6,388), unclassified (8,308), linear attention (12,276), gated delta rule (78,324) | `S' = (-1.094·(0 - S) + ((v)⊗(norm(k)) - ((0 - S))((((tanh(k) - (0 ⊙ 0)) - (0 ⊙ 0)))⊗(-0.794·(tanh(k) - (0 ⊙ 0)))))` |
| 25 | gated delta rule | 0.970 ±0.006 | 899.1 | unclassified (1,780), decayed linear attention (2,932), linear attention (78,068), delta rule (150,004), gated delta rule (160,884) | `S' = (((1.101·(S + σ(σ(1.101))·((v - S·k))⊗(tanh(k))) - (tanh(k))⊗(0)) + S) - S)` |
| 26 | gated delta rule | 0.970 ±0.006 | 620.8 | decayed linear attention (3,572), unclassified (4,340), linear attention (24,308), delta rule (341,876), gated delta rule (474,612) | `S' = ((σ((0 + σ(0))) + σ((0 + σ(0))))·σ((0 + σ(0)))·((v - S·tanh((k - 0))))⊗(tanh((k - 0))) - ((σ((0 + σ(0))) + σ(` |
| 27 | gated delta rule | 0.963 ±0.007 | 648.9 | unclassified (1,652), decayed linear attention (2,420), linear, not error-correcting (3,188), linear attention (8,180), delta rule (24,820), gated delta rule (597,364) | `S' = ((0.167·S + S) + ((((tanh(0) - k) + tanh(0)) - ((tanh(0) - k) + ((v - S·k) + v))))⊗(tanh((tanh(0) - k))))` |
| 28 | gated delta rule | 0.960 ±0.007 | 575.8 | unclassified (3,956), decayed linear attention (4,724), linear, not error-correcting (5,236), linear attention (13,684), delta rule (163,444), gated delta rule (479,988) | `S' = (((0 + 0))⊗(norm((0 ⊙ norm(0)))) + (1.174·S + ((v - S·k))⊗(k)))` |
| 29 | unclassified | 0.943 ±0.008 | 859.1 | decayed linear attention (3,956), unclassified (5,748), linear attention (9,972), delta rule (100,084) | `S' = (((norm(((0 + v) - (0 - (0·0 + S))·(k - 0))) + (0 - (0·0 + S))·(k - 0)))⊗((k - 0)) - ((0 - (0·0 + S)) - (0 + ` |
| 30 | unclassified | 0.940 ±0.008 | 605.1 | unclassified (5,620), decayed linear attention (6,644), linear attention (28,660), delta rule (105,716) | `S' = (((v)⊗(k) + ((v)⊗(k) + S)) + ((norm(((((v)⊗(k))ᵀ + S)·tanh(k) + 0)) - (((v)⊗(k))ᵀ + S)·tanh(k)))⊗(tanh(k)))` |
| 31 | gated delta rule | 0.964 ±0.006 | 550.8 | unclassified (6,388), decayed linear attention (8,052), linear attention (18,548), delta rule (50,932), gated delta rule (937,460) | `S' = (1.115·(σ(0.880)·(((1.115·S + 0) + 0)·tanh(k) - v))⊗(norm(((0·0 ⊙ norm(k)) - norm(k)))) + 1.115·S)` |
| 32 | unclassified | 0.942 ±0.008 | 757.5 | unclassified (628), decayed linear attention (884), linear, not error-correcting (1,396), gated delta rule (15,476), linear attention (17,396), delta rule (23,028) | `S' = ((S + ((norm(norm(k)))⊗((v - S·k)))ᵀ) + (σ(0)·norm((S·k + tanh(S·k))))⊗(norm(k)))` |

- decayed linear attention: seen in 31/32 seeds (median 2,932 candidates), final rule in 0/32
- delta + Kronecker mix: seen in 1/32 seeds (median 1,185,268 candidates), final rule in 1/32
- delta rule: seen in 29/32 seeds (median 61,684 candidates), final rule in 4/32
- gated delta rule: seen in 19/32 seeds (median 474,612 candidates), final rule in 16/32
- linear attention: seen in 31/32 seeds (median 17,396 candidates), final rule in 0/32
- linear, not error-correcting: seen in 20/32 seeds (median 3,188 candidates), final rule in 2/32
- unclassified: seen in 32/32 seeds (median 3,956 candidates), final rule in 9/32

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 1 | 52,724 | 61,300 | 61,684 | 52,724 |
| 2 | 14,196 | 39,412 | 90,100 | 13,812 |
| 3 | 19,572 | 51,956 | 119,412 | 19,572 |
| 4 | 9,332 | 10,356 | 87,668 | 8,180 |
| 5 | 25,844 | 29,556 | 41,076 | 25,844 |
| 6 | 22,260 | 60,916 | 61,812 | 22,260 |
| 7 | 25,844 | 29,044 | 29,044 | 25,844 |
| 8 | 3,316 | 15,476 | 33,012 | 3,316 |
| 9 | 15,220 | 15,220 | 31,988 | 15,220 |
| 10 | 105,588 | 334,964 | 360,308 | 105,588 |
| 11 | 14,068 | 30,452 | 99,188 | 14,068 |
| 12 | 3,316 | 62,196 | 69,748 | 3,316 |
| 13 | 79,476 | 84,468 | 110,068 | 79,476 |
| 14 | 7,924 | 104,948 | 241,780 | 7,924 |
| 15 | 17,268 | 22,132 | 29,940 | 17,268 |
| 16 | 18,548 | 39,284 | 39,284 | 13,172 |
| 17 | 22,388 | 98,036 | 98,932 | 18,676 |
| 18 | 63,476 | 65,012 | 83,444 | 63,476 |
| 19 | 7,028 | 61,556 | 64,884 | 5,876 |
| 20 | 31,476 | 37,364 | 76,660 | 31,220 |
| 21 | 7,028 | 19,188 | 153,076 | 7,028 |
| 22 | 6,132 | 103,924 | 123,124 | 6,132 |
| 23 | 19,956 | 73,716 | 121,332 | 19,956 |
| 24 | 12,276 | 56,692 | 78,324 | 12,276 |
| 25 | 78,068 | 150,004 | 150,004 | 78,068 |
| 26 | 24,820 | 49,396 | 430,708 | 24,308 |
| 27 | 8,180 | 11,764 | 154,868 | 8,180 |
| 28 | 13,684 | 41,716 | 163,444 | 13,684 |
| 29 | 9,972 | 14,068 | 44,532 | 9,972 |
| 30 | 28,660 | 88,308 | 105,716 | 28,660 |
| 31 | 20,212 | 24,052 | 52,084 | 18,292 |
| 32 | 17,140 | 26,612 | 197,236 | 17,140 |

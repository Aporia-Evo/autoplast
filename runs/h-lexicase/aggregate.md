# h-lexicase: 32 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 727559  time: 342s  pop: 500  tournament: 10
    commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | wall s | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|---|
| 1 | unclassified | 0.982 ±0.005 | 343.0 | unclassified (2,548), decayed linear attention (3,188), linear, not error-correcting (3,444), linear attention (33,780), gated delta rule (487,796), delta rule (487,924) | `S' = …` |
| 2 | gated delta rule | 0.973 ±0.006 | 1010.9 | decayed linear attention (1,652), unclassified (2,548), linear attention (4,212), delta rule (358,516), gated delta rule (487,668) | `S' = ((1.099·S + (0 - (σ(1.895)·v)⊗(tanh(k)))) + ((((1.099·S + (0 - (σ(1.895)·v)⊗(tanh(k)))))((((σ(1.895)·v)⊗(tanh` |
| 3 | delta + Kronecker mix | 0.978 ±0.005 | 400.6 | unclassified (1,268), decayed linear attention (2,804), linear, not error-correcting (4,340), linear attention (83,700), delta rule (133,108), delta + Kronecker mix (140,148), gated delta rule (310,132) | `S' = (σ(|tanh(|tanh(k)|·((0 - S)·tanh(k) + v))|)·(|tanh(k)|·((0 - S)·tanh(k) + v))⊗(k) - -1.100·S)` |
| 4 | unclassified | 0.981 ±0.005 | 323.2 | decayed linear attention (1,524), linear, not error-correcting (2,036), unclassified (3,060), linear attention (172,404), delta + Kronecker mix (371,444), delta rule (371,700), gated delta rule (413,684) | `S' = (σ(|σ(|(v - S·tanh(k))|)·σ(|(v - S·tanh(k))|)·S·tanh(k)|) + σ(|(v - S·tanh(k))|)·σ(|(v - S·tanh(k))|))·(((v -` |
| 5 | unclassified | 0.977 ±0.005 | 312.4 | unclassified (1,524), decayed linear attention (2,036), linear, not error-correcting (2,804), gated delta rule (27,380), linear attention (28,660), delta rule (361,716) | `S' = (σ(<(0 - S)·k, (0 - S)·k>)·((v + (0 - S)·k))⊗(k) - 1.111·(0 - S))` |
| 6 | unclassified | 0.977 ±0.005 | 406.9 | unclassified (1,268), decayed linear attention (2,420), linear, not error-correcting (3,188), linear attention (13,172), delta rule (164,212), gated delta rule (355,060) | `S' = (((σ(|(0 - S)·k|)·1.038·(v + (0 - S)·k))⊗(k) - 0.167·(0 - S)) - (0 - S))` |
| 7 | gated delta rule | 0.973 ±0.006 | 1017.8 | unclassified (756), decayed linear attention (2,036), linear attention (8,820), Kronecker delta rule (68,212), delta rule (74,868), gated delta rule (622,580) | `S' = (σ(1.441)·(S)((k)⊗((0 - k))) + (0.659 + 0.399)·((v)⊗(tanh(k)) + (0.659 + 0.399)·S))` |
| 8 | unclassified | 0.979 ±0.005 | 409.8 | unclassified (756), decayed linear attention (1,268), linear, not error-correcting (1,268), linear attention (108,532), delta + Kronecker mix (115,444), delta rule (116,724), gated delta rule (138,228) | `S' = ((|tanh(tanh(σ(0)·(1.119·v - 1.119·S·k)))|·tanh(σ(0)·(1.119·v - 1.119·S·k)))⊗(1.119·k) + (1.119·S + (v)⊗(1.11` |
| 9 | unclassified | 0.978 ±0.005 | 412.3 | decayed linear attention (4,084), linear, not error-correcting (4,852), unclassified (8,436), linear attention (28,020), delta rule (30,196), gated delta rule (211,188), delta + Kronecker mix (859,892) | `S' = (1.155·(0 - (0 - S)) + σ((|(0 - S)·k| + |(0 - S)·k|·1.155))·((v + 0.847·(0 - S)·k))⊗(k))` |
| 10 | gated delta rule | 0.975 ±0.005 | 399.6 | unclassified (1,396), decayed linear attention (1,780), linear, not error-correcting (2,932), linear attention (31,476), delta rule (32,372), gated delta rule (35,060) | `S' = |tanh(k)|·(((tanh(v) - (S + -0.161·S)·k))⊗(tanh(k)) - (-0.161·S - S))` |
| 11 | gated delta rule | 0.979 ±0.005 | 327.3 | unclassified (1,268), decayed linear attention (1,524), linear attention (18,548), delta rule (19,060), gated delta rule (381,300) | `S' = (((v - tanh((0.527 + 0.527)·S·k)))⊗(σ((0.527·<tanh((0.527 + 0.527)·S·k), tanh((0.527 + 0.527)·S·k)> + σ(0)))·` |
| 12 | unclassified | 0.958 ±0.007 | 1401.7 | unclassified (2,164), linear attention (11,892) | `S' = (((v)⊗(k) + S) + ((|tanh(S·k)|·σ(<S·k, S·k>)·(0 - (v)⊗(k)) + ((v)⊗(k) + S)))((((0 - (v)⊗(k)))ᵀ)((((v)⊗(k) + S` |
| 13 | gated delta rule | 0.972 ±0.006 | 866.3 | unclassified (2,548), decayed linear attention (3,316), linear attention (20,852), delta rule (872,052), gated delta rule (872,820) | `S' = ((1.101·S - (S)(((((tanh(tanh(k)))⊗(k))((tanh(tanh(k)))⊗(k)))((tanh(tanh(k)))⊗(k)))ᵀ)) + (tanh(v))⊗(k))` |
| 14 | delta + Kronecker mix | 0.978 ±0.005 | 321.1 | unclassified (628), linear, not error-correcting (1,652), linear attention (84,980), delta rule (94,708), gated delta rule (208,628), delta + Kronecker mix (1,021,812) | `S' = ((σ(<tanh((tanh(v) - S·tanh(k))), tanh((tanh(v) - S·tanh(k)))>)·1.114·tanh((tanh(v) - S·tanh(k))))⊗(tanh(k)) ` |
| 15 | gated delta rule | 0.971 ±0.006 | 399.9 | unclassified (3,572), decayed linear attention (3,700), linear attention (15,476), delta rule (25,076), linear, not error-correcting (26,868), gated delta rule (463,732) | `S' = (((1.156·(v + v) + (1.156·(v + v) + ((k)⊗(k) - S)·k)))⊗(tanh(tanh(k))) - 1.156·((k)⊗(k) - S))` |
| 16 | unclassified | 0.982 ±0.005 | 389.2 | decayed linear attention (1,140), linear, not error-correcting (2,164), unclassified (4,084), linear attention (4,468), delta rule (70,004), gated delta rule (76,020) | `S' = (|k| + (0.061·(<(((0 - S)·k + (0 - S)·k) + k), (0 - S)·k> + σ(σ(<(((0 - S)·k + (0 - S)·k) + k), (0 - S)·k>)))` |
| 17 | gated delta rule | 0.978 ±0.005 | 349.8 | decayed linear attention (1,140), linear, not error-correcting (1,268), unclassified (2,804), linear attention (14,068), delta rule (72,564), gated delta rule (75,764) | `S' = ((tanh(σ(0)·(v - (|S·k| + 1.110)·tanh(S·k))))⊗(tanh(k)) + 1.110·S)` |
| 18 | delta + Kronecker mix | 0.975 ±0.005 | 890.3 | decayed linear attention (1,908), linear, not error-correcting (2,804), unclassified (3,700), linear attention (4,980), delta + Kronecker mix (307,956), delta rule (311,028) | `S' = 1.074·(((tanh((tanh(S·k) - v)))⊗((tanh(S·k) - v)))(|(tanh(S·k) + v)|·σ(0)·(v)⊗(k)) - (0 - S))` |
| 19 | unclassified | 0.977 ±0.005 | 516.5 | unclassified (1,652), decayed linear attention (2,292), linear attention (8,564), delta rule (340,596) | `S' = ((((tanh(v) + tanh(v)) + tanh(|1.067·(0 - S)·k|·1.067·(0 - S)·σ(0.816)·k)))⊗(tanh(σ(0.816)·k)) - (0 + 1.067·(` |
| 20 | unclassified | 0.977 ±0.005 | 347.1 | decayed linear attention (1,268), linear, not error-correcting (1,908), unclassified (2,676), linear attention (11,380), delta rule (11,892), gated delta rule (128,372), delta + Kronecker mix (130,804) | `S' = (0.555·(S + S) - σ(<S·k, S·k>)·((v - S·k))⊗((0 - (k - 0))))` |
| 21 | gated delta rule | 0.977 ±0.005 | 416.9 | decayed linear attention (2,036), linear, not error-correcting (2,420), unclassified (3,316), linear attention (21,620), delta rule (267,124), gated delta rule (276,980) | `S' = (((1.113·S + 0) - σ(1.113·|1.113·S·k|·σ(0))·(1.113·S·k)⊗(k)) + (v)⊗(tanh(k)))` |
| 22 | gated delta rule | 0.971 ±0.006 | 1625.7 | decayed linear attention (1,140), linear, not error-correcting (1,908), linear attention (4,724), unclassified (14,836), delta rule (57,076), gated delta rule (795,252) | `S' = (0.101·((σ(2.184)·(v)⊗(σ(2.184)·k) - (0 - S)) - (((σ(2.184)·(v)⊗(σ(2.184)·k) - (0 - S)))(((v)⊗(σ(2.184)·k))ᵀ)` |
| 23 | unclassified | 0.972 ±0.006 | 459.8 | unclassified (1,396), linear, not error-correcting (40,948), linear attention (41,588), delta rule (97,908), delta + Kronecker mix (99,828), gated delta rule (171,636) | `S' = (((tanh(v) - tanh(S·k)))⊗(tanh(tanh(tanh(tanh(k))))) + (σ(-0.476·-0.476)·S + σ(-0.476·-0.476)·S))` |
| 24 | unclassified | 0.977 ±0.005 | 225.0 | unclassified (1,524), decayed linear attention (1,652), linear, not error-correcting (2,932), linear attention (27,636), delta rule (35,956), gated delta rule (43,124) | `S' = (((v - S·k))⊗(σ(1.160·|S·k|)·k) - -1.170·S)` |
| 25 | unclassified | 0.948 ±0.008 | 816.8 | unclassified (4,084), decayed linear attention (6,388), linear attention (17,652), delta rule (25,076) | `S' = (((S·tanh(k) - v))⊗(norm((norm(k) - k))) - ((((tanh(norm((norm(k) - k))) + 0.308·S·tanh(k)))⊗(tanh(norm((norm` |
| 26 | unclassified | 0.978 ±0.005 | 314.9 | unclassified (1,396), linear, not error-correcting (1,780), decayed linear attention (1,780), linear attention (14,708), delta rule (28,660), gated delta rule (267,636) | `S' = (σ(|tanh(S·k)|)·σ(|tanh(S·k)|) + σ(1.167))·(S + ((v - tanh(S·k)))⊗(σ(|tanh(S·k)|)·k))` |
| 27 | unclassified | 0.981 ±0.005 | 1029.4 | unclassified (2,164), decayed linear attention (2,676), linear, not error-correcting (4,596), linear attention (7,924), delta rule (66,420), gated delta rule (232,692) | `S' = (σ(0.960)·S - ((σ(0.960)·S)((k)⊗(k)) - σ((<(σ(0.960)·S)((k)⊗(k))·(tanh(k) + σ(0.960)·S·(0.960·v - tanh(k))), ` |
| 28 | unclassified | 0.979 ±0.005 | 456.9 | decayed linear attention (1,012), linear, not error-correcting (1,396), unclassified (2,164), linear attention (34,548), delta rule (45,172), gated delta rule (126,964) | `S' = (σ(σ(|v|)·|S·k|)·(((S + 0) + ((v - (S·k - tanh(v))))⊗(k)) - σ(|v|)·(S + 0)) + (S + 0))` |
| 29 | delta + Kronecker mix | 0.977 ±0.005 | 299.6 | unclassified (628), decayed linear attention (1,396), linear attention (7,796), linear, not error-correcting (97,780), delta + Kronecker mix (111,860) | `S' = (1.136·S + ((1.136·((1.136·tanh(v) + 1.136·tanh(v)) - S·tanh(k)) - norm(1.136·((1.136·tanh(v) + 1.136·tanh(v)` |
| 30 | unclassified | 0.971 ±0.006 | 305.7 | unclassified (884), decayed linear attention (1,140), linear attention (23,028), delta rule (24,052), linear, not error-correcting (720,500) | `S' = ((tanh((v - |tanh(S·tanh(k))|·tanh(S·tanh(k)))))⊗(tanh(k)) + 1.087·S)` |
| 31 | unclassified | 0.979 ±0.005 | 383.8 | unclassified (884), decayed linear attention (1,652), linear, not error-correcting (2,036), linear attention (9,844), delta rule (46,196), delta + Kronecker mix (254,836) | `S' = (((((((tanh(v) ⊙ k) + (0 - 1.131·S)·k) + tanh(1.131·v)) - norm((((tanh(v) ⊙ k) + (0 - 1.131·S)·k) + tanh(1.13` |
| 32 | gated delta rule | 0.975 ±0.005 | 420.0 | unclassified (756), decayed linear attention (2,036), linear, not error-correcting (3,060), linear attention (39,796), delta rule (66,676), gated delta rule (116,212) | `S' = (((v - σ(σ(0))·S·(σ(0) + (σ(0) + 0.178))·k))⊗(tanh(tanh((σ(0) + (σ(0) + 0.178))·k))) + (S + 0.178·σ(σ(0))·S))` |

- Kronecker delta rule: seen in 1/32 seeds (median 68,212 candidates), final rule in 0/32
- decayed linear attention: seen in 29/32 seeds (median 1,780 candidates), final rule in 0/32
- delta + Kronecker mix: seen in 10/32 seeds (median 254,836 candidates), final rule in 4/32
- delta rule: seen in 30/32 seeds (median 72,564 candidates), final rule in 0/32
- gated delta rule: seen in 25/32 seeds (median 232,692 candidates), final rule in 10/32
- linear attention: seen in 32/32 seeds (median 18,548 candidates), final rule in 0/32
- linear, not error-correcting: seen in 25/32 seeds (median 2,804 candidates), final rule in 0/32
- unclassified: seen in 32/32 seeds (median 2,164 candidates), final rule in 18/32

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 1 | 33,780 | 488,820 | 497,140 | 33,780 |
| 2 | 4,852 | 359,284 | 364,916 | 4,212 |
| 3 | 83,700 | 112,116 | 133,876 | 83,700 |
| 4 | 172,404 | 363,380 | 372,596 | 172,148 |
| 5 | 29,044 | 307,060 | 312,948 | 28,660 |
| 6 | 13,172 | 150,644 | 165,236 | 13,172 |
| 7 | 8,820 | 74,868 | 81,268 | 8,820 |
| 8 | 109,300 | 111,988 | 116,596 | 108,532 |
| 9 | 28,020 | 29,172 | 30,196 | 27,636 |
| 10 | 31,476 | 32,372 | 35,444 | 31,476 |
| 11 | 18,548 | 19,060 | 20,724 | 18,548 |
| 12 | 11,892 | 30,452 | 52,852 | 11,892 |
| 13 | 20,852 | 872,052 | 872,820 | 20,852 |
| 14 | 85,108 | 91,380 | 94,708 | 84,980 |
| 15 | 15,476 | 25,076 | 28,532 | 15,476 |
| 16 | 4,468 | 70,388 | 76,532 | 4,468 |
| 17 | 14,068 | 71,156 | 72,564 | 14,068 |
| 18 | 4,980 | 101,620 | 311,028 | 4,980 |
| 19 | 8,564 | 332,916 | 342,260 | 8,564 |
| 20 | 11,380 | 11,892 | 13,044 | 11,380 |
| 21 | 21,620 | 259,828 | 267,124 | 21,620 |
| 22 | 5,748 | 53,620 | 58,484 | 4,724 |
| 23 | 41,588 | 90,228 | 98,548 | 41,588 |
| 24 | 27,636 | 35,956 | 42,484 | 27,636 |
| 25 | 17,652 | 25,076 | 27,636 | 17,268 |
| 26 | 14,708 | 23,284 | 24,308 | 14,708 |
| 27 | 7,924 | 37,620 | 68,980 | 7,924 |
| 28 | 34,548 | 45,172 | 52,468 | 34,548 |
| 29 | 7,796 | 96,244 | 119,284 | 7,796 |
| 30 | 23,028 | 24,948 | 27,380 | 22,900 |
| 31 | 9,844 | 46,196 | 58,612 | 9,844 |
| 32 | 39,796 | 61,300 | 66,676 | 39,796 |

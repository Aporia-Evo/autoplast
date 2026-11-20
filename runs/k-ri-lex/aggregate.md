# k-ri-lex: 32 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1067790  time: 2929s  pop: 500  tournament: 10
    commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | wall s | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|---|
| 1 | unclassified | 0.735 ±0.013 | 2930.0 | decayed linear attention (1,140), unclassified (2,292) | `S' = ((-0.147·((S - P1) + (S - P1))·k)⊗((k - 0)) + ((((S - P1) + (v)⊗(((((k - 0) + ((k + k) + (k + k))) + ((k - 0)` |
| 2 | unclassified | 0.676 ±0.013 | 2784.8 | unclassified (3,060), decayed linear attention (7,284) | `S' = (((P1 - P2) + (0.385·S - ((v + (-0.736·(P1 - P2)·k + tanh(v))))⊗((0.011·v - k)))) + (0.385·S - ((v + (-0.736·` |
| 3 | unclassified | 0.734 ±0.013 | 5008.1 | unclassified (3,316), linear attention (4,340), decayed linear attention (6,900), gated delta rule (176,244), delta rule (177,652) | `S' = (((S + P2) + ((v + v))⊗(1.694·k)) + (((S + P2))(-0.821·(k)⊗(k)) + (-0.006·(S + P2))ᵀ))` |
| 4 | unclassified | 0.602 ±0.014 | 6168.0 | unclassified (1,908), linear attention (3,572), decayed linear attention (5,364) | `S' = ((((((v)⊗(k) + 0.215·((S)((P2 - ((S + P1))ᵀ)))(S)) + 0.010·(S)(0.215·((S)((P2 - ((S + P1))ᵀ)))(S))) + 0.215·S` |
| 5 | unclassified | 0.660 ±0.014 | 1874.0 | unclassified (884), decayed linear attention (2,292), delta rule (27,764), linear, not error-correcting (29,172) | `S' = ((S + -0.166·(P1 + P1)) + (0.532·(P2 + 0.038·((v - (P2 + S)·k))⊗((P2 + S)·k)) + ((((v - (P2 + S)·k) + 0.532·n` |
| 6 | unclassified | 0.664 ±0.014 | 5914.2 | unclassified (1,652), decayed linear attention (5,876), delta rule (118,388) | `S' = ((S + (P1 + -0.070·P2)) + ((v)⊗(k) - (σ((0 + σ(0)))·(S + (P1 + -0.070·P2)))((k)⊗(k))))` |
| 7 | unclassified | 0.740 ±0.013 | 5035.5 | unclassified (628), decayed linear attention (1,140), delta rule (209,012) | `S' = (… + ((…)((tanh(k))⊗(tanh(k))) + 0.050·((((((v + v))⊗(k) + ((v + v))⊗(k)) + (((v + v))⊗(k) + ((v + v))⊗(k))) ` |
| 8 | unclassified | 0.676 ±0.013 | 4704.7 | linear attention (1,652), decayed linear attention (3,828), unclassified (14,196) | `S' = (((S + P1) + σ(0)·(((v)⊗(k) + (v)⊗(k)) - (((S + P1))((k)⊗(k)) + -0.010·(S + P1)))) + σ(σ(0.530))·σ(0)·(((v)⊗(` |
| 9 | unclassified | 0.681 ±0.013 | 2061.8 | unclassified (884), decayed linear attention (3,444), linear attention (3,700), delta rule (101,620) | `S' = (((S + 0.176·P2) + ((0.176 + 0.012) + (0.176 + 0.012)·<norm((tanh(v) + -0.458·((S + 0.176·P2)·k + 0))), ((S +` |
| 10 | unclassified | 0.681 ±0.013 | 2375.1 | decayed linear attention (628), unclassified (1,652), delta rule (14,324) | `S' = ((((S + P1) + -0.848·P1) + ((((v + -0.233·S·k) + 0.146·(-0.233·S·k ⊙ k)))⊗(k) + (((v + -0.233·S·k) + 0.146·(-` |
| 11 | unclassified | 0.704 ±0.013 | 2472.7 | unclassified (1,396), decayed linear attention (1,908), linear attention (13,428), gated delta rule (20,340), delta rule (20,596) | `S' = ((((S + 0) + -0.029·(P2 + S)) + (((v + v) + -0.513·(P2 + S)·(k - 0)))⊗((k - 0))) + ((0.349·(P2 + σ(0)·((P2 + ` |
| 12 | unclassified | 0.723 ±0.013 | 5795.2 | unclassified (1,780), decayed linear attention (2,932), delta rule (63,220) | `S' = ((((P2 + ((v + -0.282·(P1·k + v)))⊗(tanh(k))))((P2 + ((v + -0.282·(P1·k + v)))⊗(tanh(k)))))(σ(0.203)·((((-0.2` |
| 13 | unclassified | 0.661 ±0.014 | 3305.9 | unclassified (1,780), linear attention (2,420), decayed linear attention (3,828) | `S' = ((((v + |(S + P1)·k|·-0.252·(S + P1)·k))⊗(k) - ((|(S + P1)·k|·-0.252·P1 - (S + 0.035·(k)⊗(v))) + -0.011·(S + ` |
| 14 | unclassified | 0.676 ±0.013 | 2572.8 | unclassified (2,164), decayed linear attention (13,172) | `S' = (((0.111·((S + S) - P2) + 0.111·((S + S) - P2)) + ((0.111·((S + S) - P2) + 0.111·((S + S) - P2)) + ((v + -0.1` |
| 15 | unclassified | 0.736 ±0.013 | 3131.5 | unclassified (1,140), decayed linear attention (1,780), gated Kronecker delta rule (2,548), linear attention (3,700) | `S' = ((-0.426·(-0.426·(P1 - P2) + (S + P2))·k)⊗(k) + ((((S + P2) + (-0.426·(-0.426·(P1 - P2) + (S + P2))·k)⊗(k)) +` |
| 16 | unclassified | 0.738 ±0.013 | 2627.5 | decayed linear attention (2,804), unclassified (3,316), linear, not error-correcting (3,956), linear attention (5,108), gated delta rule (34,036), delta rule (34,292) | `S' = (((S + (P2)ᵀ) + (-0.008·((S + (P2)ᵀ))ᵀ)(-0.008·((S + (P2)ᵀ))ᵀ)) + (((v + v) + -0.224·(S + (P2)ᵀ)·(k + k)))⊗((` |
| 17 | unclassified | 0.675 ±0.013 | 2372.1 | unclassified (1,524), decayed linear attention (1,908), linear attention (6,772), gated delta rule (23,156), delta rule (45,428) | `S' = ((((v + -0.134·S·k))⊗((((k + -0.134·-0.134·S·k) + 0.038·v) + ((k + -0.134·-0.134·S·k) + 0.038·v))) - (0 - S))` |
| 18 | unclassified | 0.737 ±0.013 | 5021.3 | linear attention (1,012), unclassified (3,700), decayed linear attention (4,084), delta rule (69,748) | `S' = ((-0.220·(S + P2))((((0 + k) + (0 + k)))⊗(((0 + k) + (0 + k)))) + ((S + P2) + (((v + v) + (v + v)))⊗((0 + k))` |
| 19 | unclassified | 0.686 ±0.013 | 3355.1 | unclassified (1,652), decayed linear attention (155,892), gated delta rule (157,044), delta rule (166,772) | `S' = (((((k)⊗((v + -0.180·S·k)) + (k)⊗((v + -0.180·S·k))) + ((k)⊗((v + -0.180·S·k)) + (k)⊗((v + -0.180·S·k)))) + (` |
| 20 | unclassified | 0.686 ±0.013 | 2546.6 | unclassified (1,012), decayed linear attention (9,716), gated delta rule (18,036), delta rule (22,132) | `S' = (((v + -0.443·S·k))⊗(k) + (S + 0.085·((-0.443·(P2)ᵀ + P1) + (P2 + 0.063·-0.443·(P2)ᵀ))))` |
| 21 | unclassified | 0.738 ±0.013 | 2640.6 | decayed linear attention (628), linear attention (1,140), unclassified (25,972) | `S' = (((S + (((P2 + P2) + -0.016·(P1)(S)) - P1)) + (((v + v))⊗(k) + 0.184·(((P2 + P2) + -0.016·(P1)(S)) - P1))) + ` |
| 22 | unclassified | 0.676 ±0.013 | 4670.5 | unclassified (1,140), linear attention (2,292), decayed linear attention (4,724), delta rule (43,252) | `S' = ((((S + ((P2 + -0.005·(0 + P1)))(S)) + (P2 + -0.005·(0 + P1))) + -0.212·(((((0 - v) + ((P2 + -0.005·(0 + P1))` |
| 23 | unclassified | 0.674 ±0.013 | 2568.6 | unclassified (1,780), decayed linear attention (2,932), linear, not error-correcting (3,444), gated delta rule (16,884), delta rule (18,676) | `S' = (((v + -0.227·(v + (P2 + (S - P1))·k)))⊗((k + k)) + (P2 + (S - P1)))` |
| 24 | unclassified | 0.672 ±0.013 | 2440.1 | unclassified (756), decayed linear attention (3,700), linear attention (4,084), delta rule (136,564) | `S' = (S + ((((v + v) + -0.367·((S + P2)·k - v)))⊗(k) + (0.172·P2 + 0.172·P2)))` |
| 25 | unclassified | 0.695 ±0.013 | 8246.5 | linear attention (1,396), decayed linear attention (2,804), unclassified (15,988), delta rule (39,796) | `S' = (… + -0.490·(((S + ((v)⊗(tanh((k + 0.008·(v + k)))) + ((S)((P2 + (P2)ᵀ)) + -0.048·((v)⊗(tanh((k + 0.008·(v + ` |
| 26 | unclassified | 0.682 ±0.013 | 5119.4 | linear attention (1,012), decayed linear attention (2,804), unclassified (7,668), gated delta rule (135,796), delta rule (140,532) | `S' = …` |
| 27 | unclassified | 0.645 ±0.014 | 5981.5 | unclassified (3,828), linear, not error-correcting (6,132), gated Kronecker delta rule (6,132), linear attention (7,540), decayed linear attention (9,204) | `S' = …` |
| 28 | unclassified | 0.676 ±0.013 | 2897.5 | unclassified (1,908), decayed linear attention (3,060), linear, not error-correcting (4,980), gated delta rule (7,284) | `S' = (((((v + 0.013·k) + 0.077·(P1 - P2)·S·k) - S·k))⊗(k) + 0.543·(((S + (P1 - P2)) - ((((v + 0.013·k) + 0.077·(P1` |
| 29 | unclassified | 0.710 ±0.013 | 4857.6 | unclassified (1,908), decayed linear attention (2,164), delta rule (233,076) | `S' = (… + …)` |
| 30 | unclassified | 0.686 ±0.013 | 2648.3 | unclassified (3,444), decayed linear attention (3,444), linear attention (4,852) | `S' = ((S + (0.908·((((v + v) + -0.068·(0 + k)) + -0.246·(P1 + S)·k))⊗(norm(tanh(k))) + (σ(-0.246)·P1 + 0.908·((((v` |
| 31 | unclassified | 0.671 ±0.013 | 2281.8 | unclassified (2,292), decayed linear attention (2,804), linear attention (8,564), delta rule (104,180) | `S' = (((v + (-0.217 + -0.019·σ(0))·S·k))⊗((k + k)) + ((P1 + S) + ((0 - (0 - ((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)` |
| 32 | unclassified | 0.619 ±0.014 | 5922.5 | unclassified (1,140), decayed linear attention (1,652), linear attention (3,572) | `S' = (((((((P2)(-0.213·(S)((S)ᵀ)) + ((S)ᵀ + 0.247·P2)) + -0.016·((S)ᵀ + 0.247·P2)) + 0.062·((k)⊗(v))((P2)(-0.213·(` |

- decayed linear attention: seen in 32/32 seeds (median 3,060 candidates), final rule in 0/32
- delta rule: seen in 20/32 seeds (median 69,748 candidates), final rule in 0/32
- gated Kronecker delta rule: seen in 2/32 seeds (median 6,132 candidates), final rule in 0/32
- gated delta rule: seen in 9/32 seeds (median 23,156 candidates), final rule in 0/32
- linear attention: seen in 19/32 seeds (median 3,700 candidates), final rule in 0/32
- linear, not error-correcting: seen in 5/32 seeds (median 4,980 candidates), final rule in 0/32
- unclassified: seen in 32/32 seeds (median 1,908 candidates), final rule in 32/32

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 1 | 5,620 | 111,220 | 111,732 | 106,484 |
| 2 | 6,516 | 28,148 | 29,172 | 16,372 |
| 3 | 4,340 | 177,268 | 178,036 | 156,404 |
| 4 | 3,572 | 102,900 | – | 28,788 |
| 5 | 6,516 | 27,764 | 32,244 | 12,916 |
| 6 | 3,956 | 118,004 | 120,948 | 18,932 |
| 7 | 2,804 | 209,652 | 210,548 | 95,348 |
| 8 | 1,652 | 109,556 | 116,596 | 96,244 |
| 9 | 3,700 | 99,828 | 101,876 | 40,436 |
| 10 | 2,676 | 13,684 | 14,324 | 12,148 |
| 11 | 13,428 | 20,596 | 21,364 | 20,340 |
| 12 | 5,876 | 63,604 | 64,884 | 57,332 |
| 13 | 2,420 | 55,796 | 71,924 | 37,876 |
| 14 | 10,100 | 60,404 | 60,404 | 58,100 |
| 15 | 3,700 | 60,660 | 181,108 | 46,964 |
| 16 | 5,108 | 34,164 | 34,420 | 21,364 |
| 17 | 6,772 | 45,428 | 45,940 | 23,156 |
| 18 | 1,012 | 64,372 | 66,676 | 37,748 |
| 19 | 2,804 | 164,980 | 166,900 | 157,044 |
| 20 | 4,980 | 21,236 | 22,644 | 19,444 |
| 21 | 1,140 | 92,404 | 103,540 | 22,388 |
| 22 | 2,292 | 40,820 | 43,252 | 36,724 |
| 23 | 5,364 | 18,036 | 20,596 | 16,884 |
| 24 | 4,084 | 136,564 | 137,332 | 46,964 |
| 25 | 1,652 | 41,204 | 42,868 | 39,284 |
| 26 | 1,012 | 140,532 | 140,532 | 135,796 |
| 27 | 7,540 | 60,532 | 267,380 | 20,980 |
| 28 | 5,364 | 8,308 | 23,668 | 6,772 |
| 29 | 6,900 | 233,076 | 233,076 | 47,220 |
| 30 | 4,852 | 118,260 | 118,772 | 34,036 |
| 31 | 8,564 | 104,692 | 104,692 | 99,188 |
| 32 | 3,572 | 35,316 | 753,140 | 27,764 |

# f-tune8: 16 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500140  real evaluations (after cache): 577913  time: 261s  pop: 500  tournament: 10
    commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | wall s | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|---|
| 1 | linear attention | 0.814 ±0.014 | 261.1 | decayed linear attention (3,060), linear, not error-correcting (4,596), unclassified (5,620), linear attention (13,980) | `S' = ((v)⊗(k) + -0.979·-0.979·S)` |
| 2 | gated delta rule | 0.970 ±0.006 | 840.4 | decayed linear attention (3,316), linear, not error-correcting (4,092), unclassified (5,756), linear attention (14,228), gated delta rule (782,052) | `S' = ((((0 - S))(((tanh(tanh(tanh(v))))⊗(tanh(k)))ᵀ))((((tanh(tanh(tanh(v))))⊗(tanh(k)))ᵀ)ᵀ) + ((tanh(tanh(tanh(v)` |
| 3 | linear attention | 0.814 ±0.014 | 213.8 | unclassified (884), decayed linear attention (1,268), linear, not error-correcting (1,916), linear attention (92,740) | `S' = (0.958·S + (v)⊗(k))` |
| 4 | delta rule | 0.940 ±0.008 | 1167.9 | decayed linear attention (3,316), linear attention (4,724), unclassified (279,156), delta rule (521,148) | `S' = ((0.353·((((v + v) ⊙ S·k) + (v + v)))⊗(k) + S) - (((0.353·((((v + v) ⊙ S·k) + (v + v)))⊗(k) + S))((0.353·((((` |
| 5 | gated delta rule | 0.975 ±0.005 | 470.5 | unclassified (884), decayed linear attention (2,292), linear, not error-correcting (3,708), linear attention (18,804), delta rule (290,740), gated delta rule (294,300) | `S' = 1.098·(((v + σ(1.098)·(0 - S)·k))⊗(tanh(tanh(k))) - (0 - S))` |
| 6 | gated delta rule | 0.972 ±0.006 | 490.6 | decayed linear attention (1,012), linear, not error-correcting (1,268), unclassified (2,676), linear attention (62,812), delta rule (220,212), gated delta rule (221,140) | `S' = ((tanh((0.664·v - S·k)))⊗(tanh(tanh(tanh(k)))) - 1.118·(0 - S))` |
| 7 | linear attention | 0.814 ±0.014 | 306.7 | decayed linear attention (4,084), linear, not error-correcting (4,980), unclassified (5,876), linear attention (19,596) | `S' = ((v)⊗(k) - 0.479·(0 - (S + S)))` |
| 8 | linear attention | 0.814 ±0.014 | 219.4 | unclassified (1,140), linear attention (6,804), decayed linear attention (22,300) | `S' = (0.958·S - (v)⊗((0 - k)))` |
| 9 | linear attention | 0.814 ±0.014 | 273.6 | decayed linear attention (2,164), linear, not error-correcting (2,804), unclassified (4,492), linear attention (14,660) | `S' = (σ(0) + 0.458)·(S + (v)⊗(k))` |
| 10 | linear attention | 0.814 ±0.014 | 245.8 | unclassified (3,188), decayed linear attention (3,828), linear, not error-correcting (4,468), linear attention (90,188) | `S' = ((v)⊗(k) - 0.958·(0 - S))` |
| 11 | unclassified | 0.971 ±0.006 | 470.7 | decayed linear attention (1,908), linear, not error-correcting (3,060), unclassified (3,060), linear attention (15,196), delta rule (115,340), gated delta rule (116,332) | `S' = (((v - S·tanh(k)))⊗(tanh(tanh(tanh(norm(tanh(tanh(k))))))) + 1.141·S)` |
| 12 | gated delta rule | 0.972 ±0.006 | 280.3 | unclassified (756), linear attention (35,540), decayed linear attention (56,324), gated delta rule (1,269,540) | `S' = 1.117·((S + (v)⊗(k)) - (σ(1.037·|S·<k, tanh(k)>·k|)·S·<k, tanh(k)>·k)⊗(<k, tanh(k)>·k))` |
| 13 | linear attention | 0.814 ±0.014 | 171.3 | decayed linear attention (5,900), linear, not error-correcting (6,924), unclassified (7,564), linear attention (25,780) | `S' = ((v)⊗(k) - -0.958·S)` |
| 14 | linear attention | 0.820 ±0.013 | 310.5 | unclassified (884), decayed linear attention (1,012), linear, not error-correcting (1,652), linear attention (5,620) | `S' = σ((<k, v> + 3.859))·σ((<k, v> + 3.859))·((σ((<k, v> + 3.859))·σ((<k, v> + 3.859)) + σ((<k, v> + 3.859)))·(v)⊗` |
| 15 | unclassified | 0.954 ±0.007 | 682.8 | decayed linear attention (1,780), linear, not error-correcting (2,940), unclassified (5,252), linear attention (149,468), delta rule (208,356) | `S' = ((v)⊗(k) - (((<S·k, S·k>·S·k)⊗(0.463·k) - S) - ((<S·k, S·k>·S·k)⊗(0.463·k))((<S·k, S·k>·S·k)⊗(0.463·k))))` |
| 16 | linear attention | 0.814 ±0.014 | 199.1 | decayed linear attention (4,212), linear, not error-correcting (4,852), unclassified (5,364), linear attention (6,644) | `S' = (0.958·S + (v)⊗(k))` |

- decayed linear attention: seen in 16/16 seeds (median 3,316 candidates), final rule in 0/16
- delta rule: seen in 5/16 seeds (median 220,212 candidates), final rule in 1/16
- gated delta rule: seen in 5/16 seeds (median 294,300 candidates), final rule in 4/16
- linear attention: seen in 16/16 seeds (median 18,804 candidates), final rule in 9/16
- linear, not error-correcting: seen in 13/16 seeds (median 3,708 candidates), final rule in 0/16
- unclassified: seen in 16/16 seeds (median 4,492 candidates), final rule in 2/16

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 1 | 13,980 | – | – | 13,980 |
| 2 | 14,228 | 782,052 | 782,052 | 14,228 |
| 3 | 93,252 | – | – | 92,740 |
| 4 | 4,724 | 280,612 | 520,284 | 4,724 |
| 5 | 18,804 | 291,548 | 292,436 | 18,804 |
| 6 | 62,812 | 220,212 | 221,140 | 62,812 |
| 7 | 19,596 | – | – | 19,596 |
| 8 | 6,804 | – | – | 6,804 |
| 9 | 14,660 | – | – | 14,660 |
| 10 | 90,188 | – | – | 90,188 |
| 11 | 15,196 | 116,332 | 116,636 | 15,196 |
| 12 | 35,540 | 1,269,540 | 1,269,540 | 35,540 |
| 13 | 25,780 | – | – | 25,780 |
| 14 | 5,620 | – | – | 5,620 |
| 15 | 149,340 | 196,260 | 208,356 | 149,340 |
| 16 | 6,644 | – | – | 6,644 |

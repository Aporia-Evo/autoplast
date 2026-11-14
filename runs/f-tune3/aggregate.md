# f-tune3: 16 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500064  real evaluations (after cache): 320066  time: 159s  pop: 500  tournament: 10
    commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | wall s | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|---|
| 1 | linear attention | 0.814 ±0.014 | 159.8 | decayed linear attention (3,060), linear, not error-correcting (4,596), unclassified (5,620), linear attention (17,456) | `S' = 0.958·(S + (v)⊗(k))` |
| 2 | gated delta rule | 0.973 ±0.006 | 368.2 | decayed linear attention (3,316), linear, not error-correcting (4,087), unclassified (6,647), linear attention (17,039), delta rule (28,958), gated delta rule (30,262) | `S' = 1.106·(((v - S·norm(tanh(k))))⊗(0.744·tanh(k)) - (0 - S))` |
| 3 | gated delta rule | 0.970 ±0.006 | 287.4 | unclassified (884), decayed linear attention (1,268), linear, not error-correcting (1,911), linear attention (127,502), gated delta rule (212,130), delta rule (212,592) | `S' = (1.107·S - ((v + S·(0 - tanh(tanh(k)))))⊗(tanh((0 - tanh(tanh(k))))))` |
| 4 | linear attention | 0.814 ±0.014 | 183.7 | decayed linear attention (3,316), linear attention (4,724) | `S' = ((v)⊗(k) + (0.458 + σ(0))·S)` |
| 5 | decayed linear attention | 0.814 ±0.014 | 307.3 | unclassified (884), decayed linear attention (2,292), linear, not error-correcting (3,703), linear attention (14,735) | `S' = σ((1.055 + <(k + k), (tanh(k) - v)>))·(S + (v)⊗(tanh(k)))` |
| 6 | linear attention | 0.818 ±0.013 | 219.0 | decayed linear attention (1,012), linear, not error-correcting (1,268), unclassified (2,676), linear attention (36,317) | `S' = |tanh(v)|·(S + ((norm(tanh(norm(tanh(v)))) + tanh(norm(tanh(v)))))⊗(k))` |
| 7 | gated delta rule | 0.977 ±0.005 | 352.7 | decayed linear attention (4,084), linear, not error-correcting (4,980), unclassified (5,876), linear attention (45,947), delta rule (99,755), gated delta rule (325,823) | `S' = (σ(σ(<S·(0 - k), S·(0 - k)>)) + 0.444)·(((v + σ(σ(<S·(0 - k), S·(0 - k)>))·S·(0 - k)))⊗(tanh(k)) + S)` |
| 8 | decayed linear attention | 0.818 ±0.013 | 289.5 | unclassified (1,140), linear attention (11,442), decayed linear attention (11,878) | `S' = σ(2.758)·(S - (norm(tanh(v)))⊗(((v - tanh(k)) - tanh(v))))` |
| 9 | delta rule | 0.938 ±0.008 | 1167.8 | decayed linear attention (2,164), linear, not error-correcting (2,804), unclassified (4,349), linear attention (15,072), gated Kronecker delta rule (767,461), delta rule (1,194,409) | `S' = (((tanh(v))⊗(k) + ((tanh(v))⊗(k) + (S - 0))) + (((σ(0)·((tanh(v))⊗(k))ᵀ)(((tanh(v))⊗(k) + (S - 0))) - 2.421·(` |
| 10 | linear attention | 0.814 ±0.014 | 173.4 | unclassified (3,188), decayed linear attention (3,828), linear, not error-correcting (4,468), linear attention (69,289) | `S' = ((v)⊗(k) - 0.958·(0 - S))` |
| 11 | gated delta rule | 0.972 ±0.006 | 1342.1 | decayed linear attention (1,908), linear, not error-correcting (3,060), unclassified (3,060), linear attention (15,362), gated delta rule (369,246) | `S' = (σ(0.182)·(((tanh(v))⊗(tanh(tanh(tanh(k)))) + S) + ((tanh(v))⊗(tanh(tanh(tanh(k)))) + S)) + (((tanh(v))⊗(tanh` |
| 12 | unclassified | 0.972 ±0.006 | 297.2 | unclassified (756), linear attention (13,181), decayed linear attention (131,030), delta rule (153,088), linear, not error-correcting (155,467), delta + Kronecker mix (247,450), gated delta rule (351,547) | `S' = 1.117·(|(S·k + v)|·((0.371·norm((S·k + v)) - S·k))⊗(k) + S)` |
| 13 | gated delta rule | 0.971 ±0.006 | 720.6 | decayed linear attention (7,671), linear, not error-correcting (8,823), unclassified (10,231), linear attention (17,152), delta rule (27,648), gated delta rule (311,098) | `S' = (-0.388 + -0.731)·(0 - ((-0.731·(S)((k)⊗(k)) + (v)⊗(k)) + S))` |
| 14 | linear attention | 0.814 ±0.014 | 154.7 | unclassified (884), decayed linear attention (1,012), linear, not error-correcting (1,652), linear attention (5,620) | `S' = 0.958·(S + (v)⊗(k))` |
| 15 | linear, not error-correcting | 0.970 ±0.006 | 390.8 | decayed linear attention (1,780), linear, not error-correcting (2,935), unclassified (5,495), linear attention (6,775), delta rule (16,396) | `S' = ((tanh((v - S·k)))⊗(tanh(|tanh(norm(tanh(k)))|·tanh(norm(tanh(k))))) + 1.095·S)` |
| 16 | linear attention | 0.817 ±0.013 | 164.4 | decayed linear attention (4,212), linear, not error-correcting (4,852), unclassified (5,364), linear attention (6,644) | `S' = (<tanh(v), v>·S + (tanh(tanh(v)))⊗(k))` |

- decayed linear attention: seen in 16/16 seeds (median 3,316 candidates), final rule in 2/16
- delta + Kronecker mix: seen in 1/16 seeds (median 247,450 candidates), final rule in 0/16
- delta rule: seen in 7/16 seeds (median 99,755 candidates), final rule in 1/16
- gated Kronecker delta rule: seen in 1/16 seeds (median 767,461 candidates), final rule in 0/16
- gated delta rule: seen in 6/16 seeds (median 325,823 candidates), final rule in 5/16
- linear attention: seen in 16/16 seeds (median 15,362 candidates), final rule in 6/16
- linear, not error-correcting: seen in 14/16 seeds (median 4,087 candidates), final rule in 1/16
- unclassified: seen in 15/16 seeds (median 3,188 candidates), final rule in 1/16

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 1 | 17,456 | – | – | 17,456 |
| 2 | 17,039 | 28,958 | 30,739 | 17,039 |
| 3 | 127,502 | 212,592 | 212,911 | 126,987 |
| 4 | 4,724 | – | – | 4,724 |
| 5 | 14,735 | – | – | 14,735 |
| 6 | 36,317 | – | – | 36,317 |
| 7 | 45,947 | 97,603 | 99,755 | 45,947 |
| 8 | 11,878 | – | – | 11,442 |
| 9 | 15,072 | 1,177,803 | 1,196,749 | 14,816 |
| 10 | 69,289 | – | – | 69,289 |
| 11 | 15,362 | 369,246 | 369,422 | 14,287 |
| 12 | 13,181 | 153,612 | 170,444 | 13,181 |
| 13 | 17,152 | 27,648 | 28,498 | 17,152 |
| 14 | 5,620 | – | – | 5,620 |
| 15 | 6,775 | 16,396 | 61,298 | 6,775 |
| 16 | 6,644 | – | – | 6,644 |

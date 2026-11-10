# v3-nomatvec: 16 seeds, budget 1500000, task v3 --no-op MatVec, add-node on, local

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) | wall s | best rule |
|---|---|---|---|---|---|---|
| 1 | 78,068 | 1,076,084 | 1,076,980 | 99,060 | 998 | `S' = (((v)⊗(k) - 1.004·(0 - S)) - (((v)⊗(k) - 1.004·(0 - S)))(0.596·(k)⊗(k)))` |
| 2 | 13,044 | 25,332 | 49,140 | 25,076 | 5323 | `S' = ((S + (tanh(norm(tanh(v))))⊗(tanh(k))) - ((S - (tanh(v))⊗((((tanh(k) - v) ⊙ tanh(norm(tanh(v)))) ⊙ ((tanh(k) - v) ⊙` |
| 3 | 21,492 | 58,612 | 60,788 | 58,612 | 3726 | `S' = (0.673·((tanh(v))⊗(k) - ((S + 0))(((tanh(k))⊗(k))((tanh(k))⊗(k)))) + (S + 0))` |
| 4 | 62,708 | no | no | 118,644 | 344 | `S' = (0.907·S + (v)⊗(k))` |
| 5 | 8,820 | no | no | 14,452 | 847 | `S' = σ(2.277)·((v)⊗(k) + S)` |
| 6 | 6,260 | no | no | 180,212 | 2394 | `S' = (((v)⊗(k) - (-0.092·(0 - S) + (0 - S))) + ((-1.095·((v)⊗(k) - (-0.092·(0 - S) + (0 - S))))(-0.092·(0 - S)))((-1.095` |
| 7 | 7,540 | 1,351,028 | 1,356,532 | 113,140 | 2864 | `S' = 1.002·1.002·1.002·((S - (((tanh(tanh(k)))⊗(tanh(tanh(tanh(v)))) - ((0 - (tanh(tanh(tanh(v))))⊗(tanh(tanh(k)))) + S)` |
| 8 | 9,204 | no | no | 29,428 | 437 | `S' = 0.907·(S + (v)⊗(k))` |
| 9 | 20,084 | no | no | 37,236 | 353 | `S' = ((v)⊗(k) + 0.907·S)` |
| 10 | 16,244 | no | no | 25,588 | 2191 | `S' = ((v)⊗(tanh(k)) + <v, tanh(v)>·(S - (<((tanh(v) + (tanh(v) ⊙ tanh(v))) + v), tanh(k)>·S)((v)⊗(tanh(k)))))` |
| 11 | 9,716 | no | no | 58,356 | 550 | `S' = 0.907·((v)⊗(k) + S)` |
| 12 | 46,068 | no | no | 69,108 | 456 | `S' = ((v)⊗(k) - σ(2.278)·(0 - S))` |
| 13 | 29,300 | no | no | 35,188 | 349 | `S' = ((v)⊗(k) + 0.907·S)` |
| 14 | 123,124 | no | no | 125,044 | 498 | `S' = ((v)⊗(k) - (σ(-0.187) + σ(-0.187))·(0 - S))` |
| 15 | 17,396 | no | no | 45,428 | 382 | `S' = (σ(2.278)·S + (v)⊗(k))` |
| 16 | 97,652 | 382,964 | 384,372 | 138,868 | 1664 | `S' = ((tanh(v))⊗(norm(tanh(k))) + (S - (0.674·S)((tanh(k))⊗(tanh(k)))))` |

- linear attention: reached by 16/16 seeds, median 20,084 candidates
- delta rule (beta=1): reached by 5/16 seeds, median 382,964 candidates
- delta rule (beta=0.5): reached by 5/16 seeds, median 384,372 candidates
- gated delta (alpha=0.9): reached by 16/16 seeds, median 58,612 candidates

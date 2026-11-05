# v3-extraops: 16 seeds, budget 1500000, task v3 --extra-ops, add-node on, local

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) | wall s | best rule |
|---|---|---|---|---|---|---|
| 1 | 18,548 | 1,215,732 | 1,253,492 | 20,084 | 4314 | `S' = ((((0 - S))((tanh((k - tanh((k - 0.638·tanh(k))))))⊗(norm(tanh((k - 0.638·tanh(k)))))) + (tanh(v))⊗(k)) - (0 - S))` |
| 2 | 47,988 | 994,036 | 998,644 | 49,524 | 2695 | `S' = ((tanh((0.722·v - S·tanh(tanh(max(k, tanh(tanh(tanh(k)))))))))⊗(<tanh(tanh(tanh(k))), tanh(tanh(max(k, tanh(tanh(ta` |
| 3 | 15,348 | no | no | 17,652 | 5117 | `S' = …` |
| 4 | 25,844 | no | no | 26,996 | 793 | `S' = (tanh(S) + (v)⊗((k + k)))` |
| 5 | 11,252 | 1,294,964 | 1,301,236 | 12,788 | 4849 | `S' = (((tanh((0 - S)·tanh(tanh(tanh(tanh(tanh(tanh(k))))))))⊗(tanh(tanh(tanh(tanh(tanh(tanh(k))))))) + (v)⊗(k)) - (0 - S` |
| 6 | 19,828 | 746,356 | no | 19,828 | 11266 | `S' = tanh((tanh(tanh(((tanh(tanh(tanh((S + 0)))) - (S + 0)))((((k + k) + (k ⊙ k)))⊗((k + k))))) + (tanh(((tanh(tanh(tanh` |
| 7 | 13,300 | no | no | 13,300 | 1300 | `S' = (1.051·((v)⊗(k) + (v)⊗(k)) - tanh((0 - S)))` |
| 8 | 11,380 | 765,300 | 772,468 | 13,300 | 3258 | `S' = (((norm(tanh(v)) - |S·tanh(tanh(tanh(tanh(tanh(k)))))|·S·tanh(tanh(tanh(tanh(tanh(k)))))))⊗(max(tanh(k), tanh(tanh(` |
| 9 | 174,836 | no | no | 175,348 | 1450 | `S' = σ(2.453)·(tanh(S) + (v)⊗(tanh(k)))` |
| 10 | 14,324 | 20,468 | 30,708 | 14,708 | 1338 | `S' = (((tanh(v) + (0 - S)·tanh(tanh(tanh(k)))))⊗(tanh(0.764·max(tanh(k), tanh(tanh(tanh(k)))))) - (0 - S))` |
| 11 | 9,716 | 647,412 | 698,356 | 11,252 | 1341 | `S' = (((tanh(v) - S·0.750·k))⊗(0.750·k) + S)` |
| 12 | 7,668 | no | no | 8,564 | 1445 | `S' = ((v)⊗((k + k)) + σ(abs(sum(max(0.786·(σ⃗(((tanh((k + k)) + tanh(S)·tanh((k + k))) + (k + k))) - relu(tanh(S)·tanh((` |
| 13 | 31,092 | no | no | 33,524 | 6395 | `S' = (tanh(tanh(tanh(((v)⊗(k) + tanh(tanh(tanh(S))))))) + ((tanh(tanh(tanh(((v)⊗(k) + tanh(tanh(tanh(S))))))) - tanh(tan` |
| 14 | 68,980 | 1,014,516 | 1,022,324 | 70,772 | 1455 | `S' = ((tanh(((0 - S)·max(tanh(tanh(tanh(tanh(tanh(tanh(k)))))), tanh(tanh(tanh(k)))) + tanh(v))))⊗(tanh(tanh(max(tanh(ta` |
| 15 | 15,988 | 323,572 | 325,492 | 17,012 | 925 | `S' = ((S + ((tanh(v) - S·k))⊗(0.571·k)) + ((((tanh(v) - S·k))⊗(0.571·k) - (((tanh(v) - S·k))⊗(0.571·k))(((tanh(v) - S·k)` |
| 16 | 39,796 | 1,282,804 | 1,285,876 | 40,436 | 1928 | `S' = (((S - 0) + (((v)⊗(k) + (v)⊗(k)) + (v)⊗(k))) - tanh((((tanh((S - 0)·k) ⊙ (S - 0)·k) ⊙ tanh((S - 0)·k)))⊗(tanh(k))))` |

- linear attention: reached by 16/16 seeds, median 18,548 candidates
- delta rule (beta=1): reached by 10/16 seeds, median 994,036 candidates
- delta rule (beta=0.5): reached by 9/16 seeds, median 998,644 candidates
- gated delta (alpha=0.9): reached by 16/16 seeds, median 19,828 candidates

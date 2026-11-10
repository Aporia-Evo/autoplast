# 5a-B: 16 seeds, budget 1500000, task v2 --extra-ops --evolve-readout --regime collision3, add-node on, local

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) | wall s | best rule |
|---|---|---|---|---|---|---|
| 1 | 86,900 | no | no | no | 1145 | `S' = tanh(tanh(0.947·((v)⊗(k) - (0 - S))))` |
| 2 | 6,260 | 1,355,892 | 1,356,788 | 51,188 | 3406 | `S' = (((v)⊗(k) + tanh(S)) + ((S ⊙ (v)⊗(k)) - (((v)⊗(k) + tanh(S))·tanh(k))⊗(σ(0)·k)))` |
| 3 | 384,628 | no | no | 472,180 | 1757 | `S' = tanh(((v)⊗((k + k)) + tanh(tanh(S))))` |
| 4 | 105,844 | 123,636 | 128,756 | 113,652 | 522 | `S' = ((((0 - S)·k + v))⊗((k ⊙ tanh(σ⃗(tanh(v))))) - (0 - S))` |
| 5 | 10,740 | no | no | 1,162,740 | 1679 | `S' = tanh(((σ(|(tanh(S) - ((tanh(S))(tanh(S)))ᵀ)·max(tanh((tanh(S))(tanh(S))·k), (v ⊙ (0 - σ⃗(k))))|)·(v)⊗(k) + (v)⊗(k))` |
| 6 | 15,860 | 1,189,236 | 1,225,332 | 114,676 | 4830 | `S' = tanh(((((v)⊗(tanh(k)) + (S - 0)) + (v)⊗(tanh(k))) - (tanh(tanh(norm(tanh((((v)⊗(tanh(k)) + (S - 0)) + (v)⊗(tanh(k))` |
| 7 | 131,956 | no | no | no | 1197 | `S' = tanh(((v)⊗((k + k)) + tanh(S)))` |
| 8 | 42,868 | no | no | 577,780 | 2347 | `S' = (tanh(tanh((((tanh(v))⊗(k) + tanh(S)) + (tanh(v))⊗(k)))) - (tanh((((tanh(v))⊗(k) + tanh(S)) + (tanh(v))⊗(k))) ⊙ (ta` |
| 9 | 157,044 | no | no | 1,374,964 | 1854 | `S' = ((v)⊗(k) + tanh((tanh((S + S)) - tanh(S))))` |
| 10 | 46,068 | no | no | 830,196 | 2226 | `S' = (((v)⊗(k) + (v)⊗(k)) - tanh(tanh((0 - S))))` |
| 11 | 28,916 | no | no | no | 4286 | `S' = tanh(tanh(tanh(tanh((tanh(tanh(tanh(tanh(S)))) + (v)⊗(k))))))` |
| 12 | 25,972 | 76,148 | 111,732 | 74,612 | 698 | `S' = (((v + S·(|S·tanh((0 - k))|·σ⃗((((norm(S·tanh((0 - k))) - tanh((0 - k))) + (norm(S·tanh((0 - k))) + v)) ⊙ (norm(S·t` |
| 13 | 39,284 | no | no | 1,040,500 | 1665 | `S' = (|tanh(k)|·tanh(tanh(S)) + <k, tanh(k)>·|tanh(k)|·(v)⊗(k))` |
| 14 | 240,628 | no | no | 522,740 | 1722 | `S' = (((v + v))⊗(k) - (0 - tanh(tanh(S))))` |
| 15 | 260,468 | no | no | 627,828 | 1773 | `S' = tanh((tanh(S) + ((v)⊗(k) + tanh((v)⊗(k)))))` |
| 16 | 17,396 | no | no | no | 1018 | `S' = tanh((((v + v))⊗(k) + tanh(S)))` |

- linear attention: reached by 16/16 seeds, median 46,068 candidates
- delta rule (beta=1): reached by 4/16 seeds, median 1,189,236 candidates
- delta rule (beta=0.5): reached by 4/16 seeds, median 1,225,332 candidates
- gated delta (alpha=0.9): reached by 12/16 seeds, median 577,780 candidates

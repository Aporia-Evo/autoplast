# l-downsample: 32 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 595862  time: 502s  pop: 500  tournament: 10
    commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | wall s | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|---|
| 1 | unclassified | 0.978 ±0.005 | 502.9 | unclassified (1,652), decayed linear attention (2,036), linear, not error-correcting (3,060), linear attention (8,052), delta rule (478,068) | `S' = (<(|S·k| + |S·k|)·(tanh(k) - k), tanh(k)>·(|S·k|·0.563·(tanh(S·k))⊗(k) - S) + ((v)⊗(k) - (|S·k|·0.563·(tanh(S` |
| 2 | gated delta rule | 0.973 ±0.006 | 382.9 | unclassified (3,188), decayed linear attention (3,956), linear attention (22,260), delta + Kronecker mix (92,916), delta rule (93,172), gated delta rule (104,948) | `S' = (0.553·(S + S) + ((v - 0.838·S·k))⊗(tanh(tanh(k))))` |
| 3 | linear attention | 0.819 ±0.013 | 676.9 | unclassified (4,468), decayed linear attention (5,748), linear, not error-correcting (6,260), linear attention (9,716) | `S' = ((S + (v)⊗(k)) + -0.042·((S + (v)⊗(k)) - ((v)⊗(k))((v)⊗(k))))` |
| 4 | unclassified | 0.955 ±0.007 | 432.6 | decayed linear attention (2,932), linear, not error-correcting (4,340), unclassified (5,748), linear attention (6,644), delta rule (355,700) | `S' = ((S - 0) - (((tanh(v) + v) - <(tanh(S·k) - norm(tanh(norm(tanh(S·k))))), tanh(S·k)>·tanh(norm(tanh(norm(tanh(` |
| 5 | gated delta rule | 0.975 ±0.005 | 302.6 | unclassified (1,140), decayed linear attention (22,900), linear attention (23,284), delta rule (985,716), linear, not error-correcting (1,012,596), gated delta rule (1,165,172) | `S' = ((|tanh(v)|·0.896·(v - S·k))⊗(tanh(tanh(k))) + 1.109·S)` |
| 6 | linear attention | 0.814 ±0.014 | 163.5 | unclassified (756), decayed linear attention (1,012), linear attention (19,956) | `S' = ((v)⊗(k) + 0.958·S)` |
| 7 | linear attention | 0.814 ±0.014 | 257.0 | unclassified (3,188), decayed linear attention (3,828), linear, not error-correcting (5,492), linear attention (7,412) | `S' = ((0.958·(S)ᵀ + (k)⊗(v)))ᵀ` |
| 8 | unclassified | 0.982 ±0.005 | 407.9 | unclassified (1,268), decayed linear attention (2,164), linear, not error-correcting (3,444), linear attention (118,260), delta rule (122,484), gated delta rule (284,532) | `S' = (σ(σ(0.938)·<S·k, S·k>) + 0.564)·((σ(σ(σ(0.938)·<S·k, S·k>))·(v - S·k))⊗(norm(tanh(k))) + S)` |
| 9 | unclassified | 0.949 ±0.008 | 1454.5 | unclassified (3,060), decayed linear attention (4,468), linear, not error-correcting (6,900), linear attention (18,164), delta rule (854,260) | `S' = (((S)(((tanh(v))⊗(k) + (k)⊗(v))))((σ(-0.348)·((tanh(v))⊗(k) + (k)⊗(v)) - (tanh(v))⊗(k))) - ((v)⊗(k) - ((S + (` |
| 10 | gated delta rule | 0.975 ±0.005 | 1144.7 | unclassified (4,212), decayed linear attention (4,468), linear, not error-correcting (5,108), linear attention (39,028), delta rule (345,844), gated delta rule (362,612) | `S' = (((σ(0.210)·S + σ(0.210)·S) - (σ(σ(1.352))·(σ(0.210)·S + σ(0.210)·S))((k)⊗(k))) + (v)⊗(tanh(tanh(k))))` |
| 11 | linear attention | 0.814 ±0.014 | 179.1 | decayed linear attention (2,548), linear, not error-correcting (3,060), unclassified (3,956), linear attention (24,308) | `S' = (0.958·S + (v)⊗(k))` |
| 12 | gated delta rule | 0.976 ±0.005 | 534.7 | unclassified (1,012), decayed linear attention (1,396), linear attention (5,108), linear, not error-correcting (515,956), delta rule (517,492), gated delta rule (775,156) | `S' = (((1.092·S)ᵀ + (k)⊗((tanh(v) - σ(|S·tanh(k)|)·S·k))))ᵀ` |
| 13 | gated delta rule | 0.970 ±0.006 | 568.2 | unclassified (2,420), decayed linear attention (3,828), linear attention (136,820), delta rule (302,068), gated delta rule (308,724) | `S' = ((0.629·S + -0.543·S) + (((v - 0.629·S·k))⊗(k) + S))` |
| 14 | delta rule | 0.825 ±0.013 | 244.3 | unclassified (884), decayed linear attention (1,012), linear, not error-correcting (2,036), linear attention (88,052), delta rule (1,499,380) | `S' = ((v)⊗(k) - 0.958·((S·k)⊗(k) - S))` |
| 15 | gated delta rule | 0.973 ±0.006 | 415.4 | unclassified (1,140), decayed linear attention (2,932), linear, not error-correcting (3,188), linear attention (11,636), delta rule (148,852), gated delta rule (258,036) | `S' = 1.109·((S + ((tanh(v) - S·0.377·tanh(k)))⊗(tanh(k))) + ((tanh(v) - S·0.377·tanh(k)))⊗(tanh(k)))` |
| 16 | gated delta rule | 0.975 ±0.005 | 439.3 | unclassified (2,036), linear attention (4,340), Kronecker delta rule (90,356), delta + Kronecker mix (90,868), delta rule (91,380), gated delta rule (187,892) | `S' = 1.098·((σ(1.098)·(v + (0 - S)·k))⊗(tanh(tanh(k))) - (0 - S))` |
| 17 | linear attention | 0.814 ±0.014 | 180.8 | unclassified (1,652), decayed linear attention (2,164), linear, not error-correcting (3,060), linear attention (57,972) | `S' = (0.958·S + (v)⊗(k))` |
| 18 | linear attention | 0.814 ±0.014 | 206.0 | unclassified (1,012), decayed linear attention (1,908), linear, not error-correcting (2,548), linear attention (17,652) | `S' = (0.458 + σ(0))·((v)⊗(k) + S)` |
| 19 | gated delta rule | 0.973 ±0.006 | 277.1 | unclassified (1,268), decayed linear attention (1,524), linear attention (9,716), delta rule (1,111,028), linear, not error-correcting (1,112,308), gated delta rule (1,282,164) | `S' = ((tanh((0.619·v - S·tanh(σ(|v|)·tanh(k)))))⊗(k) + 1.086·S)` |
| 20 | linear attention | 0.814 ±0.014 | 173.5 | unclassified (1,268), decayed linear attention (2,164), linear, not error-correcting (2,420), linear attention (12,276) | `S' = (0.958·S + (v)⊗(k))` |
| 21 | linear attention | 0.818 ±0.013 | 290.8 | decayed linear attention (2,420), linear, not error-correcting (3,828), unclassified (4,468), linear attention (57,716) | `S' = ((tanh(tanh(v)))⊗(((k + k) + tanh(k))) + |tanh(v)|·S)` |
| 22 | linear attention | 0.814 ±0.014 | 166.9 | decayed linear attention (628), linear, not error-correcting (1,268), unclassified (1,652), linear attention (41,204) | `S' = (0.958·S + (v)⊗(k))` |
| 23 | gated delta rule | 0.971 ±0.006 | 572.3 | decayed linear attention (884), linear, not error-correcting (2,548), unclassified (3,188), delta rule (15,988), gated delta rule (33,908) | `S' = (((tanh(v) + (0 - S)·tanh(tanh(k))))⊗(tanh(tanh(tanh(k)))) + 0.558·(S - (0 - S)))` |
| 24 | unclassified | 0.981 ±0.005 | 411.4 | unclassified (1,396), linear, not error-correcting (1,908), decayed linear attention (2,036), linear attention (7,668), delta rule (390,900), gated delta rule (995,572) | `S' = (σ((|tanh(S·k)| + 0.175)) + 0.423)·(((v - S·σ((|tanh(S·k)| + 0.175))·σ((|tanh(S·k)| + 0.175))·k))⊗(k) + S)` |
| 25 | gated delta rule | 0.973 ±0.006 | 571.4 | unclassified (1,780), decayed linear attention (2,676), linear, not error-correcting (3,828), linear attention (12,148), delta rule (160,500), gated delta rule (161,908) | `S' = (((v - 0.821·S·norm(tanh(k))))⊗(tanh(k)) - ((0 - 0.821·0.821·0.821·S) - 0.821·0.821·0.821·S))` |
| 26 | unclassified | 0.979 ±0.005 | 456.9 | decayed linear attention (2,036), linear, not error-correcting (2,932), unclassified (4,468), linear attention (7,028), delta rule (47,604), gated delta rule (227,444) | `S' = ((σ(|S·k|) + σ(σ(|S·k|)·σ(|S·k|)))·S + (((v - (S·k + S·k)) + ((σ(|S·k|)·σ(|S·k|)·v - σ(|S·k|)·σ(|S·k|)·k) ⊙ σ` |
| 27 | linear attention | 0.814 ±0.014 | 161.5 | unclassified (1,396), decayed linear attention (1,780), linear, not error-correcting (3,060), linear attention (9,588) | `S' = ((v)⊗(k) + 0.958·S)` |
| 28 | linear attention | 0.814 ±0.014 | 204.4 | unclassified (2,292), decayed linear attention (2,804), linear attention (7,796) | `S' = (0.958·S + (v)⊗(k))` |
| 29 | linear attention | 0.818 ±0.013 | 568.5 | unclassified (1,268), decayed linear attention (2,420), linear attention (47,860) | `S' = (|tanh(v)|·(((S - ((tanh(v) - norm(tanh(v))))⊗((tanh(v) - norm(tanh(v))))))ᵀ + (k)⊗(tanh(norm(tanh(v))))))ᵀ` |
| 30 | gated delta rule | 0.975 ±0.005 | 426.7 | unclassified (1,396), decayed linear attention (1,396), linear, not error-correcting (2,036), linear attention (25,716), delta rule (48,116), gated delta rule (1,103,476) | `S' = (0.551 + 0.551)·(((v - tanh((|S·k| + 0.551)·S·k)))⊗(0.551·k) + S)` |
| 31 | unclassified | 0.977 ±0.005 | 321.6 | decayed linear attention (2,932), linear, not error-correcting (3,572), unclassified (3,956), linear attention (6,388), delta rule (722,420), gated delta rule (797,428) | `S' = (σ(0.223)·(S + S) + (σ(<S·k, S·k>)·(v - S·k))⊗(k))` |
| 32 | delta rule | 0.928 ±0.009 | 380.8 | unclassified (628), decayed linear attention (1,268), linear, not error-correcting (2,164), linear attention (222,196), delta rule (1,391,092) | `S' = ((norm((S·norm(k) - S·k)))⊗(norm(k)) + ((<tanh(v), norm(v)>·tanh(v))⊗(k) + S))` |

- Kronecker delta rule: seen in 1/32 seeds (median 90,356 candidates), final rule in 0/32
- decayed linear attention: seen in 31/32 seeds (median 2,164 candidates), final rule in 0/32
- delta + Kronecker mix: seen in 2/32 seeds (median 92,916 candidates), final rule in 0/32
- delta rule: seen in 20/32 seeds (median 355,700 candidates), final rule in 2/32
- gated delta rule: seen in 15/32 seeds (median 308,724 candidates), final rule in 11/32
- linear attention: seen in 31/32 seeds (median 17,652 candidates), final rule in 12/32
- linear, not error-correcting: seen in 26/32 seeds (median 3,188 candidates), final rule in 0/32
- unclassified: seen in 32/32 seeds (median 1,652 candidates), final rule in 7/32

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 1 | 8,052 | 478,068 | 482,676 | 8,052 |
| 2 | 22,260 | 92,916 | 93,172 | 22,260 |
| 3 | 9,716 | – | – | 9,716 |
| 4 | 6,644 | 355,700 | 359,028 | 6,644 |
| 5 | 23,284 | 1,009,652 | 1,016,948 | 23,284 |
| 6 | 19,956 | – | – | 19,956 |
| 7 | 7,412 | – | – | 7,412 |
| 8 | 118,260 | 122,484 | 123,252 | 118,260 |
| 9 | 18,164 | 853,620 | 854,900 | 18,164 |
| 10 | 39,540 | 345,844 | 345,844 | 39,028 |
| 11 | 25,204 | – | – | 24,052 |
| 12 | 5,108 | 515,956 | 517,492 | 5,108 |
| 13 | 136,820 | 302,068 | 303,604 | 136,820 |
| 14 | 88,052 | – | – | 88,052 |
| 15 | 11,380 | 147,572 | 148,852 | 11,380 |
| 16 | 4,340 | 91,380 | 94,452 | 4,340 |
| 17 | 57,972 | – | – | 57,972 |
| 18 | 17,652 | – | – | 17,652 |
| 19 | 9,716 | 1,111,028 | 1,138,932 | 9,716 |
| 20 | 12,276 | – | – | 12,276 |
| 21 | 57,716 | – | – | 57,460 |
| 22 | 41,972 | – | – | 41,204 |
| 23 | 15,988 | 15,988 | 17,652 | 15,988 |
| 24 | 7,668 | 391,924 | 403,700 | 7,668 |
| 25 | 12,404 | 161,652 | 161,908 | 12,148 |
| 26 | 7,028 | 37,492 | 47,604 | 7,028 |
| 27 | 9,588 | – | – | 9,588 |
| 28 | 7,796 | – | – | 7,796 |
| 29 | 50,548 | – | – | 47,860 |
| 30 | 26,100 | 39,028 | 48,628 | 25,716 |
| 31 | 6,388 | 724,084 | 724,596 | 6,388 |
| 32 | 222,580 | 1,391,092 | 1,410,164 | 222,196 |

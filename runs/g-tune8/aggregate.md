# g-tune8: 32 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500036  real evaluations (after cache): 852910  time: 2793s  pop: 500  tournament: 10
    commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | wall s | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|---|
| 1 | delta rule | 0.624 ±0.014 | 2794.4 | unclassified (5,364), linear, not error-correcting (8,956), linear attention (51,252), decayed linear attention (73,036), delta rule (753,820) | `S' = (1.004·((tanh(v))⊗(k) - (0 - S)) - (1.004·((tanh(v))⊗(k) - (0 - S)))(0.596·(tanh(tanh(k)))⊗(tanh(tanh(k)))))` |
| 2 | unclassified | 0.608 ±0.014 | 3301.9 | unclassified (1,268), decayed linear attention (2,164), linear attention (4,596) | `S' = (((v)⊗(k) + S) - (P1)(0.177·S))` |
| 3 | unclassified | 0.728 ±0.013 | 4889.8 | unclassified (628), linear, not error-correcting (1,268), decayed linear attention (1,524), linear attention (6,164), delta rule (36,236) | `S' = ((((P1 + P2) + S) + (-0.906·((P1 + P2) + S))((k)⊗(tanh(k)))) + ((((tanh(v) + tanh(v)) + (tanh(v) + tanh(v))) ` |
| 4 | unclassified | 0.691 ±0.013 | 2993.5 | unclassified (3,828), decayed linear attention (4,468), linear attention (13,596), delta rule (880,668) | `S' = ((0 - P1) + ((S + (P1 - P2)) + ((v - (S + (P1 - P2))·k))⊗(1/(1.171)·k)))` |
| 5 | unclassified | 0.517 ±0.014 | 1932.5 | decayed linear attention (4,980), unclassified (993,116) | `S' = ((((tanh(0.852·v) + v))⊗((k)⊗(tanh(tanh(0.852·v)))·(tanh(0.852·v) + v)) + 0.852·S) + ((((tanh(0.852·v) + v))⊗` |
| 6 | unclassified | 0.641 ±0.014 | 4357.8 | decayed linear attention (628), unclassified (12,068) | `S' = (((((v)⊗(k) - ((v)⊗(k) + -0.506·P2)) - -0.506·(v)⊗(k)) - 1.933·-0.506·(v)⊗(k)) + ((((((v)⊗(k) - ((v)⊗(k) + -0` |
| 7 | unclassified | 0.624 ±0.014 | 2504.6 | unclassified (756), decayed linear attention (1,012), linear attention (7,804) | `S' = ((v)⊗(tanh(k)) + (S - 0.166·P1))` |
| 8 | unclassified | 0.628 ±0.014 | 5161.6 | unclassified (3,828), decayed linear attention (4,596), linear attention (8,612), delta rule (305,604) | `S' = (1/(σ(5.369))·S + (((v)⊗(tanh(tanh(tanh(tanh(tanh(k)))))) - (S)((tanh(tanh(tanh(tanh(k)))))⊗(tanh(tanh(tanh(t` |
| 9 | unclassified | 0.729 ±0.013 | 2473.7 | unclassified (3,708), decayed linear attention (19,956), linear attention (21,468), delta rule (347,412) | `S' = (σ(σ(0)·σ(0)·σ(σ(0)·σ(0)))·((v)⊗(((k + k) + (k + k))) + σ(σ(0)·σ(0))·σ(0)·P1) - ((σ(σ(0)·σ(0))·σ(0)·P1 - (P1 ` |
| 10 | unclassified | 0.667 ±0.013 | 2794.3 | decayed linear attention (2,036), unclassified (3,572), linear attention (6,524), gated delta rule (261,676), delta rule (262,148) | `S' = ((((0 - (P2 + (S - P1)))·tanh(tanh(k)))⊗(tanh(k)) + (P2 + (S - P1))) - -0.442·(tanh(v))⊗((tanh(tanh(k)) + tan` |
| 11 | unclassified | 0.510 ±0.014 | 1466.4 | unclassified (2,564), decayed linear attention (3,332) | `S' = (0.862·S - (v)⊗(tanh(((0 - k) + (0 - k)))))` |
| 12 | unclassified | 0.637 ±0.014 | 1861.2 | unclassified (3,572), decayed linear attention (4,212), gated delta rule (9,076), delta rule (10,628), delta + Kronecker mix (87,924) | `S' = ((0 + S) - (((S + P2)·k - v))⊗(|((S + P2)·k - v)|·0.398·k))` |
| 13 | unclassified | 0.514 ±0.014 | 2282.6 | decayed linear attention (1,780), unclassified (2,676) | `S' = ((((v)⊗(k))ᵀ + (1/(|tanh(tanh(v))|)·((((v)⊗(k) + (v)⊗(k)) + (v)⊗(k)) + (((v)⊗(k) + (v)⊗(k)) + (v)⊗(k))) + P1)` |
| 14 | unclassified | 0.686 ±0.013 | 4708.3 | unclassified (1,396), decayed linear attention (1,780), linear attention (4,852), gated delta rule (1,102,020), delta rule (1,105,788) | `S' = ((1/(1.958)·P2 + ((v)⊗((((tanh(tanh(tanh(k))) + tanh(k)) + (tanh(tanh(tanh(k))) + tanh(k))) + ((tanh(tanh(tan` |
| 15 | unclassified | 0.675 ±0.013 | 3475.3 | decayed linear attention (1,396), unclassified (3,852), linear attention (5,780) | `S' = …` |
| 16 | unclassified | 0.514 ±0.014 | 2135.2 | decayed linear attention (3,188), linear attention (5,372), unclassified (7,556) | `S' = ((v)⊗(norm(tanh((k + (k + k))))) + (P2)(S))` |
| 17 | delta + Kronecker mix | 0.631 ±0.014 | 2166.8 | decayed linear attention (884), linear attention (5,380), unclassified (7,556), delta rule (102,700), delta + Kronecker mix (279,292) | `S' = (S + (<tanh(v), v>·(v - S·tanh(tanh(tanh(tanh(σ(1.307)·k))))))⊗(σ(1.307)·(tanh(tanh(σ(1.307)·k)))⊗((v - S·tan` |
| 18 | unclassified | 0.511 ±0.014 | 1589.0 | decayed linear attention (2,676), unclassified (4,980), linear attention (6,772) | `S' = σ(<tanh((0 - norm(tanh(k)))), ((0 - norm(tanh(k))) - tanh(norm(tanh(k))))>)·((v)⊗(tanh(tanh(norm(tanh(norm(ta` |
| 19 | unclassified | 0.514 ±0.014 | 1845.5 | unclassified (756), decayed linear attention (1,140), linear attention (10,796) | `S' = 0.439·((S + (v)⊗(norm(tanh(tanh((tanh(tanh(k)) + tanh(tanh(tanh(k))))))))) + S)` |
| 20 | unclassified | 0.657 ±0.014 | 2729.8 | decayed linear attention (2,044), unclassified (10,300), delta rule (309,924), linear, not error-correcting (312,396), delta + Kronecker mix (417,316) | `S' = (((P2 + P2))((|tanh((v - S·tanh(tanh(k))))|·(v - S·tanh(tanh(k))))⊗(0.461·k)) + ((|tanh((v - S·tanh(tanh(k)))` |
| 21 | unclassified | 0.521 ±0.014 | 2024.1 | decayed linear attention (756), unclassified (3,196), linear attention (3,708) | `S' = (|tanh(tanh(tanh((k + σ(1.970)·v))))|·(σ(1.970)·v)⊗(tanh(k)) + σ(1.970)·S)` |
| 22 | unclassified | 0.633 ±0.014 | 3785.6 | unclassified (4,852), decayed linear attention (6,260), linear attention (17,460), delta rule (542,364) | `S' = (((v)⊗(((k + P1·k) + (k + P1·k))) - (P2)((tanh(tanh(k)))⊗(norm(tanh(tanh(k)))))) + (S + ((v)⊗(((k + P1·k) + (` |
| 23 | unclassified | 0.521 ±0.014 | 3030.1 | decayed linear attention (1,396), unclassified (6,132), linear attention (7,548) | `S' = (σ(σ(0.171))·(v)⊗((tanh(k) + tanh(((k ⊙ k) ⊙ (k ⊙ k))))) - σ(0.171)·σ(0.171)·((P2 + (0 - S)) + (0 - S)))` |
| 24 | decayed linear attention | 0.509 ±0.014 | 1049.7 | decayed linear attention (628), unclassified (12,676), linear attention (13,708) | `S' = 0.874·((v)⊗(tanh(tanh(k))) + S)` |
| 25 | unclassified | 0.730 ±0.013 | 2490.8 | decayed linear attention (1,140), linear, not error-correcting (2,036), unclassified (4,100), linear attention (15,588), delta rule (15,988) | `S' = ((S + P1) - (((S + P1)·tanh(tanh(k)) - (((v + v) + (v + v)) - ((tanh(tanh(k)) ⊙ (v + v)) - ((v + v) + (v + v)` |
| 26 | unclassified | 0.653 ±0.014 | 2540.2 | decayed linear attention (1,780), unclassified (2,804), linear attention (8,580), delta rule (368,500) | `S' = (((0 - P1) + S) + (tanh(0.720·0.720·(v - ((0 - P1) + S)·tanh(k))))⊗((k - 0)))` |
| 27 | unclassified | 0.510 ±0.014 | 1221.6 | decayed linear attention (1,396), unclassified (8,220), linear attention (11,188) | `S' = 0.862·((v)⊗(tanh((k + k))) + S)` |
| 28 | unclassified | 0.631 ±0.014 | 2681.9 | unclassified (884), decayed linear attention (1,524), delta rule (752,996) | `S' = (σ(0)·((((v)⊗(k) + S))((0.616·((tanh(k))⊗(tanh(k)) - P1))ᵀ)·v)⊗((tanh(k) ⊙ tanh(k))) + (((v)⊗(k) + S) - (((v)` |
| 29 | unclassified | 0.636 ±0.014 | 1647.4 | decayed linear attention (1,780), unclassified (5,500), linear attention (6,652) | `S' = ((S + (tanh(v))⊗(tanh(tanh(tanh(k))))) - ((S + (tanh(v))⊗(tanh(tanh(tanh(k))))))((tanh(tanh(tanh(k))))⊗(|S·ta` |
| 30 | unclassified | 0.686 ±0.013 | 3233.7 | decayed linear attention (2,164), unclassified (2,420), linear attention (5,876) | `S' = ((0.496·P2 + 1/(0.163)·((v)⊗(k) + (v)⊗(k))) - ((0.496·P2 + 1/(0.163)·((v)⊗(k) + (v)⊗(k))))((tanh(k))⊗(k)))` |
| 31 | unclassified | 0.515 ±0.014 | 1833.7 | decayed linear attention (2,164), unclassified (5,884), linear attention (9,060) | `S' = ((v)⊗(50.469·k) - σ((-1.911 + |tanh((v + 50.469·k))|))·((v)⊗(50.469·k) - P2))` |
| 32 | unclassified | 0.649 ±0.014 | 1990.0 | decayed linear attention (4,596), unclassified (10,244) | `S' = (((3.511·3.511·v + (k - ((P1 - -0.552·P2)·k - k))))⊗(k) + (-0.552·P2 + (P2 + S)))` |

- decayed linear attention: seen in 32/32 seeds (median 2,036 candidates), final rule in 1/32
- delta + Kronecker mix: seen in 3/32 seeds (median 279,292 candidates), final rule in 1/32
- delta rule: seen in 14/32 seeds (median 347,412 candidates), final rule in 1/32
- gated delta rule: seen in 3/32 seeds (median 261,676 candidates), final rule in 0/32
- linear attention: seen in 24/32 seeds (median 7,804 candidates), final rule in 0/32
- linear, not error-correcting: seen in 4/32 seeds (median 8,956 candidates), final rule in 0/32
- unclassified: seen in 32/32 seeds (median 3,852 candidates), final rule in 29/32

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 1 | 50,484 | 741,020 | 741,956 | 740,484 |
| 2 | 4,596 | 594,332 | – | 589,668 |
| 3 | 5,388 | 34,124 | 34,748 | 33,948 |
| 4 | 13,596 | 881,180 | 882,756 | 75,932 |
| 5 | 9,404 | – | – | 1,001,188 |
| 6 | 13,476 | 749,340 | 756,588 | 63,476 |
| 7 | 7,804 | 976,932 | 1,149,604 | 52,044 |
| 8 | 8,612 | 305,604 | 310,548 | 304,276 |
| 9 | 21,468 | 347,804 | 354,220 | 344,988 |
| 10 | 6,524 | 262,148 | 273,964 | 261,676 |
| 11 | 27,684 | – | – | – |
| 12 | 9,460 | 10,628 | 11,012 | 10,628 |
| 13 | 6,388 | – | – | – |
| 14 | 4,852 | 1,104,524 | 1,120,132 | 50,980 |
| 15 | 5,780 | 287,676 | 288,692 | 59,548 |
| 16 | 5,372 | – | – | – |
| 17 | 5,380 | 98,972 | 102,700 | 98,148 |
| 18 | 6,772 | – | – | – |
| 19 | 10,796 | – | – | – |
| 20 | 309,092 | 309,092 | 314,236 | 309,092 |
| 21 | 3,708 | – | – | 22,404 |
| 22 | 17,460 | 528,460 | 542,996 | 51,364 |
| 23 | 7,548 | – | – | 508,444 |
| 24 | 13,708 | – | – | – |
| 25 | 15,588 | 15,988 | 24,900 | 15,988 |
| 26 | 8,580 | 368,500 | 371,364 | 368,500 |
| 27 | 11,188 | – | – | – |
| 28 | 14,588 | 749,668 | 754,164 | 748,940 |
| 29 | 6,396 | 1,272,732 | 1,275,308 | 1,271,420 |
| 30 | 5,876 | 331,844 | 331,844 | 331,140 |
| 31 | 6,908 | – | – | 553,780 |
| 32 | 22,236 | 38,764 | 41,636 | 33,340 |

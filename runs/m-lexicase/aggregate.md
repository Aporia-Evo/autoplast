# m-lexicase: 8 seeds

Settings of the first seed (all seeds of a tag must share them except seed and task seed):

    task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 763131  time: 4707s  pop: 500  tournament: 10
    commit: dce11aa  task seed: 801  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery

| seed | family of final best rule | train acc | wall s | families seen as best rule (first candidate count) | best rule |
|---|---|---|---|---|---|
| 801 | unclassified | 0.675 ±0.013 | 4709.8 | decayed linear attention (756), unclassified (3,060), linear attention (3,700), delta rule (108,532) | `S' = (σ(σ(1.148))·((σ(1.148)·(v)⊗(k) + (v)⊗(k)) + (σ(1.148)·(v)⊗(k) + (v)⊗(k))) + (((S - P2) + S) - ((((S - P2) + ` |
| 802 | unclassified | 0.697 ±0.013 | 1159.5 | unclassified (1,524), decayed linear attention (2,164), linear attention (8,948), gated delta rule (65,908), delta rule (67,060) | `S' = (((σ(0)·P1·tanh(k) - 0.489·(S·tanh(k) - v)))⊗((tanh(k) + σ(0)·P1·tanh(k))) - (σ(0)·P1 - S))` |
| 803 | unclassified | 0.636 ±0.014 | 1580.4 | unclassified (6,388), decayed linear attention (34,420), gated Kronecker delta rule (476,404), delta rule (949,748) | `S' = (((S)ᵀ - 0.414·((P1·v - k))⊗((v - S·k))))ᵀ` |
| 804 | unclassified | 0.667 ±0.013 | 1779.6 | linear attention (1,524), decayed linear attention (6,388), unclassified (71,540), delta rule (78,068) | `S' = ((0.645·P1·(0 - k))⊗(k) + ((norm(tanh(v)))⊗(0.358·(k - (0.645·0.645·P1 - (0.645·P1·(0 - k))⊗(k))·0.645·P1·(0 ` |
| 805 | unclassified | 0.692 ±0.013 | 1434.4 | unclassified (3,060), decayed linear attention (21,492), delta rule (187,252) | `S' = (((v - ((S + P1) - ((P1)ᵀ)((S + P1)))·k))⊗(σ(0.728)·σ(0.728)·k) + ((S + P1) - ((P1)ᵀ)((S + P1))))` |
| 806 | unclassified | 0.581 ±0.014 | 1168.0 | decayed linear attention (756), unclassified (2,932), linear attention (5,748) | `S' = ((v)⊗(k) + P2)` |
| 807 | unclassified | 0.686 ±0.013 | 4313.5 | unclassified (756), decayed linear attention (1,012), linear attention (3,316) | `S' = ((S + (((P2 - P1) + S) + (tanh(v))⊗(k))) - (((S + (((P2 - P1) + S) + (tanh(v))⊗(k))))(((tanh(v))⊗(k))ᵀ))((v)⊗` |
| 808 | unclassified | 0.689 ±0.013 | 1607.9 | decayed linear attention (1,140), unclassified (5,364), delta rule (23,540) | `S' = (((S - P1) + (((v + v) + ((v + v) - (S - P1)·tanh(k))))⊗(k)) + σ(0)·P2)` |

- decayed linear attention: seen in 8/8 seeds (median 2,164 candidates), final rule in 0/8
- delta rule: seen in 6/8 seeds (median 108,532 candidates), final rule in 0/8
- gated Kronecker delta rule: seen in 1/8 seeds (median 476,404 candidates), final rule in 0/8
- gated delta rule: seen in 1/8 seeds (median 65,908 candidates), final rule in 0/8
- linear attention: seen in 5/8 seeds (median 3,700 candidates), final rule in 0/8
- unclassified: seen in 8/8 seeds (median 3,060 candidates), final rule in 8/8

## Accuracy levels (not rediscovery)

| seed | linear attention | delta rule (beta=1) | delta rule (beta=0.5) | gated delta (alpha=0.9) |
|---|---|---|---|---|
| 801 | 3,700 | 108,532 | 108,532 | 15,604 |
| 802 | 8,948 | 67,060 | 74,100 | 65,908 |
| 803 | 14,068 | 949,748 | 951,540 | 34,420 |
| 804 | 1,524 | 72,948 | 74,228 | 6,772 |
| 805 | 14,836 | 184,564 | 187,252 | 21,492 |
| 806 | 5,748 | – | – | 45,044 |
| 807 | 3,316 | 257,652 | 274,676 | 104,180 |
| 808 | 7,796 | 23,540 | 33,908 | 23,540 |

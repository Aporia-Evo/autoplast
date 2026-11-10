# Search seed 10

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: off  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 490788  time: 1883s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* unclassified: 3444 candidates
* linear attention: 13684 candidates
* delta rule: 425076 candidates
* gated delta rule: 425460 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 13684 candidates
- delta rule (beta=1) (acc 0.858): 425332 candidates
- delta rule (beta=0.5) (acc 0.932): 426100 candidates
- gated delta (alpha=0.9) (acc 0.729): 13684 candidates

## Best rule

```
S' = ((((0 - S))((tanh(k))⊗(tanh(k))))((tanh(k))⊗(tanh(k))) + ((v)⊗(tanh(k)) - -1.138·S))

Effective program (10 instructions):
  s1 = -1.1380
  M2 = MatSub(M1, M0)
  M1 = MatScale(s1, M0)
  V0 = Tanh(V0)
  M0 = Outer(V1, V0)
  M3 = Outer(V0, V0)
  M2 = MatMul(M2, M3)
  M2 = MatMul(M2, M3)
  M0 = MatSub(M0, M1)
  M0 = MatAdd(M2, M0)

structure: gated delta rule  [a=1.138 b=0.951 c=-0.819 g=0.009, erase c/a=0.720, R²=0.9982, 384 steps]

train acc 0.967 ±0.006
test d16 T12 ow0.3: acc 0.967 ±0.003  margin 0.307
test d16 T12 ow0.0: acc 0.954 ±0.003  margin 0.281
test d16 T12 ow0.6: acc 0.957 ±0.004  margin 0.297
test d32 T24 ow0.3: acc 0.923 ±0.004  margin 0.308
test d8 T6 ow0.3: acc 0.839 ±0.008  margin 0.137
full T24: acc 0.646 ±0.007  margin 0.051
overload T48: acc 0.133 ±0.004  margin -0.409
rewrite8 T96: acc 0.000 ±0.000  margin 0.000
rewrite14 T96: acc 0.000 ±0.000  margin 0.000
clustered T12: acc 0.231 ±0.006  margin -0.239
clustered8 T48: acc 0.033 ±0.004  margin -0.607
```

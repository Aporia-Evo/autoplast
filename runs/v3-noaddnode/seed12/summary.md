# Search seed 12

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: off  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 538020  time: 620s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 9460 candidates
* decayed linear attention: 9716 candidates
* linear, not error-correcting: 15988 candidates
* linear attention: 67700 candidates
* delta rule: 73716 candidates
* gated delta rule: 112628 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 67956 candidates
- delta rule (beta=1) (acc 0.858): 67956 candidates
- delta rule (beta=0.5) (acc 0.932): 74228 candidates
- gated delta (alpha=0.9) (acc 0.729): 67700 candidates

## Best rule

```
S' = (((v - tanh(S·tanh(k))))⊗(0.897·tanh(k)) + 1.107·S)

Effective program (10 instructions):
  V0 = Tanh(V0)
  s3 = 1.1072
  V2 = MatVec(M0, V0)
  s1 = 0.8967
  V0 = VecScale(s1, V0)
  V2 = Tanh(V2)
  V1 = VecSub(V1, V2)
  M0 = MatScale(s3, M0)
  M2 = Outer(V1, V0)
  M0 = MatAdd(M2, M0)

structure: gated delta rule  [a=1.107 b=0.853 c=-0.772 g=0.001, erase c/a=0.697, R²=0.9981, 384 steps]

train acc 0.973 ±0.006
test d16 T12 ow0.3: acc 0.967 ±0.003  margin 0.306
test d16 T12 ow0.0: acc 0.952 ±0.003  margin 0.281
test d16 T12 ow0.6: acc 0.961 ±0.004  margin 0.299
test d32 T24 ow0.3: acc 0.952 ±0.003  margin 0.342
test d8 T6 ow0.3: acc 0.836 ±0.008  margin 0.136
full T24: acc 0.729 ±0.007  margin 0.101
overload T48: acc 0.253 ±0.005  margin -0.279
rewrite8 T96: acc 0.020 ±0.003  margin -0.646
rewrite14 T96: acc 0.021 ±0.002  margin -0.661
clustered T12: acc 0.189 ±0.006  margin -0.280
clustered8 T48: acc 0.044 ±0.005  margin -0.564
```

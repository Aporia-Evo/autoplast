# Search seed 14

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: on  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 362466  time: 405s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1396 candidates
* decayed linear attention: 1780 candidates
* linear, not error-correcting: 2804 candidates
* linear attention: 13172 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 13172 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 13172 candidates

## Best rule

```
S' = ((tanh(tanh(v)))⊗(k) + <v, tanh(v)>·S)

Effective program (6 instructions):
  V3 = Tanh(V1)
  s3 = Dot(V1, V3)
  V2 = Tanh(V3)
  M0 = MatScale(s3, M0)
  M2 = Outer(V2, V0)
  M0 = MatAdd(M2, M0)

structure: linear attention  [a=0.951 b=0.911 c=-0.001 g=0.005, erase c/a=0.001, R²=0.9960, 384 steps]

train acc 0.817 ±0.013
test d16 T12 ow0.3: acc 0.789 ±0.006  margin 0.149
test d16 T12 ow0.0: acc 0.865 ±0.004  margin 0.185
test d16 T12 ow0.6: acc 0.648 ±0.009  margin 0.069
test d32 T24 ow0.3: acc 0.878 ±0.005  margin 0.226
test d8 T6 ow0.3: acc 0.637 ±0.010  margin 0.034
full T24: acc 0.588 ±0.007  margin 0.017
overload T48: acc 0.372 ±0.005  margin -0.150
rewrite8 T96: acc 0.431 ±0.011  margin -0.066
rewrite14 T96: acc 0.433 ±0.008  margin -0.091
clustered T12: acc 0.151 ±0.005  margin -0.272
clustered8 T48: acc 0.078 ±0.006  margin -0.362
```

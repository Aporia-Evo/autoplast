# Search seed 3

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: off  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 481203  time: 716s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1780 candidates
* decayed linear attention: 2804 candidates
* linear attention: 6900 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 6900 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 6900 candidates

## Best rule

```
S' = (|tanh(v)|·S + |tanh(norm(tanh(v)))|·(tanh(norm(tanh(v))))⊗(k))

Effective program (9 instructions):
  V5 = Tanh(V1)
  V3 = Normalize(V5)
  s2 = Norm(V5)
  V5 = Tanh(V3)
  M3 = Outer(V5, V0)
  s1 = Norm(V5)
  M0 = MatScale(s2, M0)
  M1 = MatScale(s1, M3)
  M0 = MatAdd(M0, M1)

structure: linear attention  [a=0.952 b=0.910 c=-0.001 g=0.005, erase c/a=0.001, R²=0.9957, 384 steps]

train acc 0.818 ±0.013
test d16 T12 ow0.3: acc 0.788 ±0.006  margin 0.149
test d16 T12 ow0.0: acc 0.866 ±0.004  margin 0.185
test d16 T12 ow0.6: acc 0.647 ±0.009  margin 0.069
test d32 T24 ow0.3: acc 0.879 ±0.005  margin 0.226
test d8 T6 ow0.3: acc 0.635 ±0.010  margin 0.033
full T24: acc 0.589 ±0.007  margin 0.017
overload T48: acc 0.372 ±0.005  margin -0.149
rewrite8 T96: acc 0.427 ±0.011  margin -0.068
rewrite14 T96: acc 0.433 ±0.008  margin -0.092
clustered T12: acc 0.151 ±0.005  margin -0.272
clustered8 T48: acc 0.078 ±0.006  margin -0.362
```

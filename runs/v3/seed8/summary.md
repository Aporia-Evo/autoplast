# Search seed 8

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: on  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 391446  time: 444s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3828 candidates
* decayed linear attention: 4596 candidates
* linear, not error-correcting: 5620 candidates
* linear attention: 16500 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 16500 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 16500 candidates

## Best rule

```
S' = |tanh(v)|·(S + (tanh(norm(tanh(v))))⊗(k))

Effective program (7 instructions):
  V1 = Tanh(V1)
  V2 = Normalize(V1)
  V2 = Tanh(V2)
  M2 = Outer(V2, V0)
  M0 = MatAdd(M0, M2)
  s2 = Norm(V1)
  M0 = MatScale(s2, M0)

structure: linear attention  [a=0.952 b=0.907 c=-0.001 g=0.006, erase c/a=0.001, R²=0.9956, 384 steps]

train acc 0.817 ±0.013
test d16 T12 ow0.3: acc 0.788 ±0.006  margin 0.149
test d16 T12 ow0.0: acc 0.866 ±0.004  margin 0.185
test d16 T12 ow0.6: acc 0.647 ±0.009  margin 0.069
test d32 T24 ow0.3: acc 0.878 ±0.005  margin 0.226
test d8 T6 ow0.3: acc 0.634 ±0.010  margin 0.033
full T24: acc 0.588 ±0.007  margin 0.017
overload T48: acc 0.372 ±0.005  margin -0.149
rewrite8 T96: acc 0.427 ±0.011  margin -0.068
rewrite14 T96: acc 0.433 ±0.008  margin -0.092
clustered T12: acc 0.151 ±0.005  margin -0.272
clustered8 T48: acc 0.079 ±0.006  margin -0.362
```

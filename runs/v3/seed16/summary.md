# Search seed 16

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: on  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 794534  time: 1619s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3188 candidates
* linear, not error-correcting: 3828 candidates
* unclassified: 5364 candidates
* linear attention: 46324 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 46324 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 45940 candidates

## Best rule

```
S' = (<k, tanh(k)>·S + (<k, tanh(k)>·v)⊗((((tanh(k))⊗((v ⊙ (tanh(k) + 0.569·v))))(<k, tanh(k)>·S)·norm(tanh(k)) + tanh(k))))

Effective program (15 instructions):
  V3 = Tanh(V0)
  s0 = Dot(V0, V3)
  V0 = Normalize(V3)
  M3 = MatScale(s0, M0)
  s3 = 0.5689
  V4 = VecScale(s3, V1)
  V2 = VecAdd(V3, V4)
  V5 = Hadamard(V1, V2)
  M0 = Outer(V3, V5)
  M2 = MatMul(M0, M3)
  V0 = MatVec(M2, V0)
  V5 = VecAdd(V0, V3)
  V3 = VecScale(s0, V1)
  M0 = Outer(V3, V5)
  M0 = MatAdd(M3, M0)

structure: linear attention  [a=0.951 b=0.908 c=-0.000 g=0.031, erase c/a=0.000, R²=0.9957, 384 steps]

train acc 0.829 ±0.013
test d16 T12 ow0.3: acc 0.789 ±0.006  margin 0.149
test d16 T12 ow0.0: acc 0.868 ±0.004  margin 0.186
test d16 T12 ow0.6: acc 0.647 ±0.009  margin 0.070
test d32 T24 ow0.3: acc 0.876 ±0.005  margin 0.225
test d8 T6 ow0.3: acc 0.635 ±0.010  margin 0.030
full T24: acc 0.588 ±0.007  margin 0.015
overload T48: acc 0.377 ±0.005  margin -0.141
rewrite8 T96: acc 0.436 ±0.011  margin -0.071
rewrite14 T96: acc 0.428 ±0.008  margin -0.096
clustered T12: acc 0.152 ±0.005  margin -0.287
clustered8 T48: acc 0.092 ±0.006  margin -0.348
```

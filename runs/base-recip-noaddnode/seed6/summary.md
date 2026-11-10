# Search seed 6

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: off  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 341850  time: 361s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 884 candidates
* linear, not error-correcting: 5492 candidates
* linear attention: 6004 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 6004 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 6004 candidates

## Best rule

```
S' = (σ((3.156 + <v, k>))·(S + (v)⊗(k)) - σ(0)·(v)⊗(k))

Effective program (10 instructions):
  M1 = Outer(V1, V0)
  s2 = Sigmoid(s1)
  M0 = MatAdd(M0, M1)
  s0 = Dot(V1, V0)
  s1 = 3.1563
  s1 = SAdd(s1, s0)
  s0 = Sigmoid(s1)
  M3 = MatScale(s2, M1)
  M0 = MatScale(s0, M0)
  M0 = MatSub(M0, M3)

structure: linear attention  [a=0.959 b=0.458 c=-0.001 g=0.001, erase c/a=0.001, R²=0.9991, 384 steps]

train acc 0.819 ±0.013
test d16 T12 ow0.3: acc 0.788 ±0.006  margin 0.149
test d16 T12 ow0.0: acc 0.884 ±0.004  margin 0.193
test d16 T12 ow0.6: acc 0.637 ±0.009  margin 0.064
test d32 T24 ow0.3: acc 0.874 ±0.005  margin 0.225
test d8 T6 ow0.3: acc 0.633 ±0.010  margin 0.029
full T24: acc 0.598 ±0.007  margin 0.020
overload T48: acc 0.382 ±0.005  margin -0.127
rewrite8 T96: acc 0.378 ±0.011  margin -0.093
rewrite14 T96: acc 0.414 ±0.008  margin -0.098
clustered T12: acc 0.153 ±0.005  margin -0.270
clustered8 T48: acc 0.077 ±0.006  margin -0.363
```

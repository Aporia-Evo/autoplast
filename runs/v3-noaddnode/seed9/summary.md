# Search seed 9

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: off  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 420583  time: 524s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3572 candidates
* linear, not error-correcting: 4468 candidates
* unclassified: 11380 candidates
* linear attention: 30836 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 30836 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 30836 candidates

## Best rule

```
S' = ((v)⊗((tanh(k) + k)) - <k, tanh(k)>·(0 - S))

Effective program (7 instructions):
  M2 = MatSub(M1, M0)
  V3 = Tanh(V0)
  V2 = VecAdd(V3, V0)
  s2 = Dot(V0, V3)
  M0 = Outer(V1, V2)
  M2 = MatScale(s2, M2)
  M0 = MatSub(M0, M2)

structure: linear attention  [a=0.951 b=1.951 c=0.000 g=-0.001, erase c/a=-0.000, R²=0.9992, 384 steps]

train acc 0.812 ±0.014
test d16 T12 ow0.3: acc 0.789 ±0.006  margin 0.150
test d16 T12 ow0.0: acc 0.871 ±0.004  margin 0.188
test d16 T12 ow0.6: acc 0.646 ±0.009  margin 0.072
test d32 T24 ow0.3: acc 0.878 ±0.005  margin 0.225
test d8 T6 ow0.3: acc 0.642 ±0.010  margin 0.035
full T24: acc 0.590 ±0.007  margin 0.017
overload T48: acc 0.377 ±0.005  margin -0.140
rewrite8 T96: acc 0.424 ±0.011  margin -0.069
rewrite14 T96: acc 0.436 ±0.008  margin -0.091
clustered T12: acc 0.151 ±0.005  margin -0.271
clustered8 T48: acc 0.092 ±0.006  margin -0.347
```

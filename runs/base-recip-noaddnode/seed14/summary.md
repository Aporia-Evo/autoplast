# Search seed 14

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: off  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 353777  time: 987s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1780 candidates
* linear, not error-correcting: 2932 candidates
* linear attention: 34292 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 34292 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 34292 candidates

## Best rule

```
S' = ((((((v)⊗(k) + σ(3.490)·S))((v)⊗(k)))((v)⊗(k)))((((v)⊗(k) + σ(3.490)·S))((v)⊗(k))) - (((((v)⊗(k) + σ(3.490)·S))((v)⊗(k)))((v)⊗(k)) - ((v)⊗(k) + σ(3.490)·S)))

Effective program (10 instructions):
  s0 = 3.4896
  s1 = Sigmoid(s0)
  M0 = MatScale(s1, M0)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M1, M0)
  M3 = MatMul(M0, M1)
  M1 = MatMul(M3, M1)
  M2 = MatMul(M1, M3)
  M1 = MatSub(M1, M0)
  M0 = MatSub(M2, M1)

structure: unclassified  [a=0.970 b=0.948 c=-0.052 g=-0.001, erase c/a=0.054, R²=0.9846, 384 steps]

train acc 0.824 ±0.013
test d16 T12 ow0.3: acc 0.802 ±0.006  margin 0.156
test d16 T12 ow0.0: acc 0.891 ±0.004  margin 0.197
test d16 T12 ow0.6: acc 0.659 ±0.009  margin 0.077
test d32 T24 ow0.3: acc 0.888 ±0.005  margin 0.232
test d8 T6 ow0.3: acc 0.645 ±0.010  margin 0.040
full T24: acc 0.609 ±0.007  margin 0.028
overload T48: acc 0.392 ±0.005  margin -0.111
rewrite8 T96: acc 0.371 ±0.011  margin -0.093
rewrite14 T96: acc 0.399 ±0.008  margin -0.098
clustered T12: acc 0.171 ±0.006  margin -0.259
clustered8 T48: acc 0.089 ±0.006  margin -0.342
```

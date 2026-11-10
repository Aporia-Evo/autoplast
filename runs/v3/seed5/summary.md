# Search seed 5

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: on  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 335716  time: 432s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4980 candidates
* linear, not error-correcting: 5492 candidates
* unclassified: 6388 candidates
* linear attention: 11252 candidates
* delta rule: 1106932 candidates
* gated delta rule: 1107572 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 11252 candidates
- delta rule (beta=1) (acc 0.858): 1107316 candidates
- delta rule (beta=0.5) (acc 0.932): 1107700 candidates
- gated delta (alpha=0.9) (acc 0.729): 11252 candidates

## Best rule

```
S' = 1.125·(S + (((norm(tanh(v)) - tanh(S·tanh(k))) - (tanh(tanh(k)) - tanh(tanh(tanh(k))))))⊗(tanh(tanh(tanh(k)))))

Effective program (14 instructions):
  V0 = Tanh(V0)
  V4 = MatVec(M0, V0)
  s0 = 1.1249
  V4 = Tanh(V4)
  V2 = Tanh(V1)
  V1 = Normalize(V2)
  V5 = VecSub(V1, V4)
  V0 = Tanh(V0)
  V2 = Tanh(V0)
  V4 = VecSub(V0, V2)
  V4 = VecSub(V5, V4)
  M2 = Outer(V4, V2)
  M0 = MatAdd(M0, M2)
  M0 = MatScale(s0, M0)

structure: gated delta rule  [a=1.125 b=0.985 c=-0.874 g=-0.000, erase c/a=0.777, R²=0.9908, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.963 ±0.003  margin 0.312
test d16 T12 ow0.0: acc 0.941 ±0.003  margin 0.278
test d16 T12 ow0.6: acc 0.961 ±0.004  margin 0.310
test d32 T24 ow0.3: acc 0.937 ±0.004  margin 0.328
test d8 T6 ow0.3: acc 0.833 ±0.008  margin 0.137
full T24: acc 0.674 ±0.007  margin 0.071
overload T48: acc 0.232 ±0.005  margin -0.326
rewrite8 T96: acc 0.000 ±0.000  margin 0.000
rewrite14 T96: acc 0.000 ±0.000  margin 0.000
clustered T12: acc 0.199 ±0.006  margin -0.282
clustered8 T48: acc 0.038 ±0.004  margin -0.593
```

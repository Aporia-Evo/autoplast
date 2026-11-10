# Search seed 6

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: on  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 394622  time: 1139s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 628 candidates
* linear, not error-correcting: 2292 candidates
* unclassified: 4596 candidates
* linear attention: 8692 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 8692 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 8692 candidates

## Best rule

```
S' = (((v)⊗(k) + 0.955·S) + (0.955·(((tanh(k) ⊙ tanh(k)) - k))⊗((tanh(k) ⊙ tanh(k))))(0.955·(((tanh(k) ⊙ tanh(k)) - k))⊗((tanh(k) ⊙ tanh(k)))))

Effective program (11 instructions):
  M1 = Outer(V1, V0)
  V3 = Tanh(V0)
  V4 = Hadamard(V3, V3)
  V3 = VecSub(V4, V0)
  s0 = 0.9555
  M0 = MatScale(s0, M0)
  M0 = MatAdd(M1, M0)
  M2 = Outer(V3, V4)
  M3 = MatScale(s0, M2)
  M1 = MatMul(M3, M3)
  M0 = MatAdd(M0, M1)

structure: linear attention  [a=0.956 b=1.000 c=0.002 g=-0.000, erase c/a=-0.002, R²=0.9958, 384 steps]

train acc 0.821 ±0.013
test d16 T12 ow0.3: acc 0.785 ±0.006  margin 0.146
test d16 T12 ow0.0: acc 0.879 ±0.004  margin 0.189
test d16 T12 ow0.6: acc 0.638 ±0.009  margin 0.063
test d32 T24 ow0.3: acc 0.870 ±0.005  margin 0.224
test d8 T6 ow0.3: acc 0.608 ±0.010  margin 0.019
full T24: acc 0.593 ±0.007  margin 0.017
overload T48: acc 0.375 ±0.005  margin -0.134
rewrite8 T96: acc 0.381 ±0.011  margin -0.089
rewrite14 T96: acc 0.418 ±0.008  margin -0.098
clustered T12: acc 0.156 ±0.005  margin -0.271
clustered8 T48: acc 0.055 ±0.005  margin -0.394
```

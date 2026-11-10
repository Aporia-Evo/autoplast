# Search seed 11

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: off  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 432555  time: 1151s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1524 candidates
* decayed linear attention: 1908 candidates
* linear, not error-correcting: 3956 candidates
* linear attention: 10996 candidates
* delta rule: 610932 candidates
* gated delta rule: 875252 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 10996 candidates
- delta rule (beta=1) (acc 0.858): 610292 candidates
- delta rule (beta=0.5) (acc 0.932): 611316 candidates
- gated delta (alpha=0.9) (acc 0.729): 10996 candidates

## Best rule

```
S' = (0.567·(((v)⊗(tanh(k)) + (S + 0)) - ((S + 0))((tanh(tanh(k)))⊗(tanh(tanh(k))))) + 0.567·(((v)⊗(tanh(k)) + (S + 0)) - ((S + 0))((tanh(tanh(k)))⊗(tanh(tanh(k))))))

Effective program (11 instructions):
  V0 = Tanh(V0)
  M2 = Outer(V1, V0)
  s3 = 0.5672
  V2 = Tanh(V0)
  M3 = MatAdd(M0, M1)
  M0 = MatAdd(M2, M3)
  M1 = Outer(V2, V2)
  M1 = MatMul(M3, M1)
  M0 = MatSub(M0, M1)
  M2 = MatScale(s3, M0)
  M0 = MatAdd(M2, M2)

structure: gated delta rule  [a=1.134 b=1.079 c=-0.941 g=0.010, erase c/a=0.829, R²=0.9968, 384 steps]

train acc 0.965 ±0.006
test d16 T12 ow0.3: acc 0.959 ±0.003  margin 0.317
test d16 T12 ow0.0: acc 0.938 ±0.003  margin 0.279
test d16 T12 ow0.6: acc 0.960 ±0.004  margin 0.322
test d32 T24 ow0.3: acc 0.947 ±0.003  margin 0.340
test d8 T6 ow0.3: acc 0.843 ±0.008  margin 0.142
full T24: acc 0.668 ±0.007  margin 0.066
overload T48: acc 0.117 ±0.003  margin -0.419
rewrite8 T96: acc 0.000 ±0.000  margin 0.000
rewrite14 T96: acc 0.000 ±0.000  margin 0.000
clustered T12: acc 0.213 ±0.006  margin -0.270
clustered8 T48: acc 0.034 ±0.004  margin -0.588
```

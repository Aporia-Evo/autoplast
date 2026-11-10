# Search seed 3

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: on  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 448145  time: 1284s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* linear, not error-correcting: 1268 candidates
* linear attention: 3188 candidates
* gated delta rule: 857588 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 3188 candidates
- delta rule (beta=1) (acc 0.858): 835572 candidates
- delta rule (beta=0.5) (acc 0.932): 836468 candidates
- gated delta (alpha=0.9) (acc 0.729): 3188 candidates

## Best rule

```
S' = 1.115·(((v)⊗(tanh(tanh(tanh(tanh(k))))) + S) - ((((v)⊗(tanh(tanh(tanh(tanh(k))))) + S))((tanh(tanh(tanh(k))))⊗(tanh(tanh(tanh(tanh(tanh(k))))))) - ((v)⊗(tanh(tanh(tanh(tanh(k))))) + (v)⊗(tanh(tanh(tanh(tanh(k))))))))

Effective program (14 instructions):
  V3 = Tanh(V0)
  V0 = Tanh(V3)
  V3 = Tanh(V0)
  V2 = Tanh(V3)
  M3 = Outer(V1, V2)
  M0 = MatAdd(M3, M0)
  M2 = MatAdd(M3, M3)
  V5 = Tanh(V2)
  M3 = Outer(V3, V5)
  M3 = MatMul(M0, M3)
  M3 = MatSub(M3, M2)
  M0 = MatSub(M0, M3)
  s3 = 1.1147
  M0 = MatScale(s3, M0)

structure: unclassified  [a=1.114 b=2.146 c=-0.803 g=0.015, erase c/a=0.720, R²=0.9895, 384 steps]

train acc 0.969 ±0.006
test d16 T12 ow0.3: acc 0.965 ±0.003  margin 0.309
test d16 T12 ow0.0: acc 0.948 ±0.003  margin 0.278
test d16 T12 ow0.6: acc 0.962 ±0.004  margin 0.304
test d32 T24 ow0.3: acc 0.973 ±0.002  margin 0.363
test d8 T6 ow0.3: acc 0.822 ±0.008  margin 0.130
full T24: acc 0.726 ±0.007  margin 0.098
overload T48: acc 0.165 ±0.004  margin -0.344
rewrite8 T96: acc 0.020 ±0.003  margin -0.636
rewrite14 T96: acc 0.000 ±0.000  margin 0.000
clustered T12: acc 0.193 ±0.006  margin -0.284
clustered8 T48: acc 0.041 ±0.004  margin -0.568
```

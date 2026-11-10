# Search seed 9

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: on  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 529701  time: 1392s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3700 candidates
* linear attention: 20468 candidates
* decayed linear attention: 541812 candidates
* delta rule: 735348 candidates
* gated delta rule: 951796 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 20852 candidates
- delta rule (beta=1) (acc 0.858): 734580 candidates
- delta rule (beta=0.5) (acc 0.932): 737908 candidates
- gated delta (alpha=0.9) (acc 0.729): 7924 candidates

## Best rule

```
S' = ((((v)⊗(tanh(tanh(k))) + S) - 0.675·(S)((k)⊗(k))) + 0.097·(((v)⊗(tanh(tanh(k))) + S) - 0.675·(S)((k)⊗(k))))

Effective program (12 instructions):
  V2 = Tanh(V0)
  V3 = Tanh(V2)
  s1 = 0.0966
  M3 = Outer(V1, V3)
  M3 = MatAdd(M3, M0)
  M1 = Outer(V0, V0)
  M1 = MatMul(M0, M1)
  s2 = 0.6750
  M0 = MatScale(s2, M1)
  M0 = MatSub(M3, M0)
  M2 = MatScale(s1, M0)
  M0 = MatAdd(M0, M2)

structure: gated delta rule  [a=1.097 b=0.999 c=-0.740 g=0.001, erase c/a=0.675, R²=0.9977, 384 steps]

train acc 0.973 ±0.006
test d16 T12 ow0.3: acc 0.967 ±0.003  margin 0.305
test d16 T12 ow0.0: acc 0.951 ±0.003  margin 0.279
test d16 T12 ow0.6: acc 0.963 ±0.004  margin 0.299
test d32 T24 ow0.3: acc 0.970 ±0.003  margin 0.350
test d8 T6 ow0.3: acc 0.835 ±0.008  margin 0.138
full T24: acc 0.776 ±0.006  margin 0.125
overload T48: acc 0.218 ±0.004  margin -0.265
rewrite8 T96: acc 0.026 ±0.004  margin -0.612
rewrite14 T96: acc 0.020 ±0.002  margin -0.632
clustered T12: acc 0.185 ±0.006  margin -0.288
clustered8 T48: acc 0.063 ±0.005  margin -0.520
```

# Search seed 4

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: on  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 901093  time: 1496s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 7284 candidates
* decayed linear attention: 9460 candidates
* linear, not error-correcting: 10996 candidates
* linear attention: 16372 candidates
* delta rule: 16884 candidates
* gated delta rule: 1448564 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 16372 candidates
- delta rule (beta=1) (acc 0.858): 16884 candidates
- delta rule (beta=0.5) (acc 0.932): 57716 candidates
- gated delta (alpha=0.9) (acc 0.729): 16244 candidates

## Best rule

```
S' = ((tanh((0.381·v + (0 - S)·tanh(k))))⊗(tanh(tanh(tanh(k)))) - 1/(|tanh(tanh(k))|)·(0 - S))

Effective program (15 instructions):
  M1 = MatSub(M2, M0)
  V2 = Tanh(V0)
  V3 = Tanh(V2)
  V2 = Tanh(V3)
  s3 = Norm(V3)
  V3 = Tanh(V0)
  s0 = 0.3813
  V1 = VecScale(s0, V1)
  s3 = Recip(s3)
  V4 = MatVec(M1, V3)
  V3 = VecAdd(V1, V4)
  V4 = Tanh(V3)
  M0 = Outer(V4, V2)
  M2 = MatScale(s3, M1)
  M0 = MatSub(M0, M2)

structure: gated delta rule  [a=1.097 b=0.330 c=-0.822 g=0.029, erase c/a=0.750, R²=0.9910, 384 steps]

train acc 0.967 ±0.006
test d16 T12 ow0.3: acc 0.961 ±0.003  margin 0.310
test d16 T12 ow0.0: acc 0.940 ±0.003  margin 0.277
test d16 T12 ow0.6: acc 0.961 ±0.004  margin 0.312
test d32 T24 ow0.3: acc 0.995 ±0.001  margin 0.406
test d8 T6 ow0.3: acc 0.826 ±0.008  margin 0.131
full T24: acc 0.770 ±0.006  margin 0.128
overload T48: acc 0.227 ±0.005  margin -0.266
rewrite8 T96: acc 0.018 ±0.003  margin -0.621
rewrite14 T96: acc 0.022 ±0.002  margin -0.638
clustered T12: acc 0.167 ±0.006  margin -0.331
clustered8 T48: acc 0.034 ±0.004  margin -0.628
```

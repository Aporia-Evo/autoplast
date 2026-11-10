# Search seed 2

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: off  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 364081  time: 398s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 1780 candidates
* linear, not error-correcting: 7540 candidates
* linear attention: 10100 candidates
* delta rule: 803188 candidates
* gated delta rule: 804212 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 10100 candidates
- delta rule (beta=1) (acc 0.858): 803956 candidates
- delta rule (beta=0.5) (acc 0.932): 804212 candidates
- gated delta (alpha=0.9) (acc 0.729): 10100 candidates

## Best rule

```
S' = (1.108·S + (|tanh(v)|·|tanh(v)|·(v - S·tanh(k)))⊗(tanh(tanh(k))))

Effective program (12 instructions):
  V0 = Tanh(V0)
  V2 = Tanh(V1)
  s1 = Norm(V2)
  V2 = MatVec(M0, V0)
  s3 = 1.1084
  V0 = Tanh(V0)
  M0 = MatScale(s3, M0)
  s2 = SMul(s1, s1)
  V1 = VecSub(V1, V2)
  V1 = VecScale(s2, V1)
  M2 = Outer(V1, V0)
  M0 = MatAdd(M0, M2)

structure: gated delta rule  [a=1.108 b=0.825 c=-0.786 g=0.017, erase c/a=0.709, R²=0.9959, 384 steps]

train acc 0.973 ±0.006
test d16 T12 ow0.3: acc 0.967 ±0.003  margin 0.308
test d16 T12 ow0.0: acc 0.953 ±0.003  margin 0.280
test d16 T12 ow0.6: acc 0.963 ±0.004  margin 0.303
test d32 T24 ow0.3: acc 0.977 ±0.002  margin 0.366
test d8 T6 ow0.3: acc 0.827 ±0.008  margin 0.130
full T24: acc 0.743 ±0.007  margin 0.110
overload T48: acc 0.178 ±0.004  margin -0.317
rewrite8 T96: acc 0.023 ±0.003  margin -0.627
rewrite14 T96: acc 0.020 ±0.002  margin -0.640
clustered T12: acc 0.188 ±0.006  margin -0.283
clustered8 T48: acc 0.047 ±0.005  margin -0.550
```

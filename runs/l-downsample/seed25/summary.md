# Search seed 25

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 643231  time: 571s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1780 candidates
* decayed linear attention: 2676 candidates
* linear, not error-correcting: 3828 candidates
* linear attention: 12148 candidates
* delta rule: 160500 candidates
* gated delta rule: 161908 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 12404 candidates
- delta rule (beta=1) (acc 0.858): 161652 candidates
- delta rule (beta=0.5) (acc 0.932): 161908 candidates
- gated delta (alpha=0.9) (acc 0.729): 12148 candidates

## Best rule

```
S' = (((v - 0.821·S·norm(tanh(k))))⊗(tanh(k)) - ((0 - 0.821·0.821·0.821·S) - 0.821·0.821·0.821·S))

Effective program (12 instructions):
  s3 = 0.8208
  M0 = MatScale(s3, M0)
  s0 = SMul(s3, s3)
  M3 = MatScale(s0, M0)
  M1 = MatSub(M1, M3)
  M2 = MatSub(M1, M3)
  V0 = Tanh(V0)
  V3 = Normalize(V0)
  V4 = MatVec(M0, V3)
  V1 = VecSub(V1, V4)
  M0 = Outer(V1, V0)
  M0 = MatSub(M0, M2)

structure: gated delta rule  [a=1.106 b=0.951 c=-0.780 g=0.003, erase c/a=0.706, R²=0.9988, 384 steps]

train acc 0.973 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.309  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.281  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.305  ±0.004
test d32 T24 ow0.3: acc 0.969  margin 0.351  ±0.003
test d8 T6 ow0.3: acc 0.840  margin 0.139  ±0.008
test d16 T64 K8 ow0.3: acc 0.063  margin -0.528  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

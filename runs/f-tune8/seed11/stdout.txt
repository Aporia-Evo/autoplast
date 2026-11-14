# Search seed 11

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500004  real evaluations (after cache): 922866  time: 470s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 8

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1908 candidates
* linear, not error-correcting: 3060 candidates
* unclassified: 3060 candidates
* linear attention: 15196 candidates
* delta rule: 115340 candidates
* gated delta rule: 116332 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 15196 candidates
- delta rule (beta=1) (acc 0.858): 116332 candidates
- delta rule (beta=0.5) (acc 0.932): 116636 candidates
- gated delta (alpha=0.9) (acc 0.729): 15196 candidates

## Best rule

```
S' = (((v - S·tanh(k)))⊗(tanh(tanh(tanh(norm(tanh(tanh(k))))))) + 1.141·S)

Effective program (12 instructions):
  V5 = Tanh(V0)
  V3 = MatVec(M0, V5)
  V4 = Tanh(V5)
  V0 = Normalize(V4)
  V1 = VecSub(V1, V3)
  V2 = Tanh(V0)
  V5 = Tanh(V2)
  V0 = Tanh(V5)
  M3 = Outer(V1, V0)
  s3 = 1.1407
  M1 = MatScale(s3, M0)
  M0 = MatAdd(M3, M1)

structure: unclassified  [a=1.140 b=0.883 c=-0.840 g=0.009, erase c/a=0.737, R²=0.9865, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.967  margin 0.309  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.961  margin 0.302  ±0.004
test d32 T24 ow0.3: acc 0.918  margin 0.303  ±0.004
test d8 T6 ow0.3: acc 0.836  margin 0.138  ±0.008
test d16 T64 K8 ow0.3: acc 0.028  margin -0.626  ±0.004
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

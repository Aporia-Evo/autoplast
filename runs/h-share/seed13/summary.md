# Search seed 13

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 910042  time: 602s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 5748 candidates
* unclassified: 8692 candidates
* linear attention: 79476 candidates
* delta rule: 84468 candidates
* gated delta rule: 1053428 candidates
* linear, not error-correcting: 1304180 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 79476 candidates
- delta rule (beta=1) (acc 0.858): 84468 candidates
- delta rule (beta=0.5) (acc 0.932): 110068 candidates
- gated delta (alpha=0.9) (acc 0.729): 79476 candidates

## Best rule

```
S' = (0.139·S + ((tanh(((v + 0) - S·k)))⊗(k) + S))

Effective program (9 instructions):
  V5 = VecAdd(V1, V4)
  V1 = MatVec(M0, V0)
  V4 = VecSub(V5, V1)
  V3 = Tanh(V4)
  M2 = Outer(V3, V0)
  s3 = 0.1388
  M1 = MatScale(s3, M0)
  M0 = MatAdd(M2, M0)
  M0 = MatAdd(M1, M0)

structure: linear, not error-correcting  [a=1.139 b=0.918 c=-0.885 g=0.073, erase c/a=0.777, R²=0.9934, 384 steps]

train acc 0.957 ±0.007
test d16 T12 ow0.3: acc 0.958  margin 0.307  ±0.003
test d16 T12 ow0.0: acc 0.947  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.945  margin 0.302  ±0.004
test d32 T24 ow0.3: acc 0.855  margin 0.261  ±0.005
test d8 T6 ow0.3: acc 0.837  margin 0.142  ±0.008
test d16 T64 K8 ow0.3: acc 0.024  margin -0.663  ±0.003
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

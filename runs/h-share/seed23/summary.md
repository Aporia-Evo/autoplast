# Search seed 23

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 919380  time: 894s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 13300 candidates
* decayed linear attention: 14196 candidates
* linear attention: 19956 candidates
* delta rule: 66548 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 19956 candidates
- delta rule (beta=1) (acc 0.858): 73716 candidates
- delta rule (beta=0.5) (acc 0.932): 121332 candidates
- gated delta (alpha=0.9) (acc 0.729): 19956 candidates

## Best rule

```
S' = (((((k)⊗(v))ᵀ + (k)⊗(v)) + (((k)⊗(v) - S))((k)⊗(norm((k - (0 + 0)))))) + (-0.607 + -0.607)·((k)⊗(v) - S))

Effective program (14 instructions):
  M2 = Outer(V0, V1)
  M1 = Transpose(M2)
  V4 = VecAdd(V3, V3)
  V3 = VecSub(V0, V4)
  V4 = Normalize(V3)
  M0 = MatSub(M2, M0)
  s0 = -0.6075
  s0 = SAdd(s0, s0)
  M1 = MatAdd(M1, M2)
  M3 = Outer(V0, V4)
  M3 = MatMul(M0, M3)
  M3 = MatAdd(M1, M3)
  M2 = MatScale(s0, M0)
  M0 = MatAdd(M3, M2)

structure: unclassified  [a=1.215 b=1.049 c=-1.003 g=0.011, erase c/a=0.825, R²=0.9727, 384 steps]

train acc 0.948 ±0.008
test d16 T12 ow0.3: acc 0.937  margin 0.281  ±0.004
test d16 T12 ow0.0: acc 0.922  margin 0.250  ±0.003
test d16 T12 ow0.6: acc 0.935  margin 0.279  ±0.005
test d32 T24 ow0.3: acc 0.638  margin 0.086  ±0.007
test d8 T6 ow0.3: acc 0.836  margin 0.135  ±0.008
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

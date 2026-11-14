# Search seed 21

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 933605  time: 800s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 6004 candidates
* decayed linear attention: 6516 candidates
* linear attention: 7028 candidates
* delta rule: 19188 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 7028 candidates
- delta rule (beta=1) (acc 0.858): 19188 candidates
- delta rule (beta=0.5) (acc 0.932): 153076 candidates
- gated delta (alpha=0.9) (acc 0.729): 7028 candidates

## Best rule

```
S' = (0.093·S - ((((0 - v))⊗(k) + (S·tanh((k + (k ⊙ (0 - v)))))⊗(norm(tanh((k + (k ⊙ (0 - v))))))) - S))

Effective program (13 instructions):
  V1 = VecSub(V2, V1)
  V4 = Hadamard(V0, V1)
  V3 = VecAdd(V0, V4)
  V3 = Tanh(V3)
  M2 = Outer(V1, V0)
  V4 = Normalize(V3)
  s0 = 0.0931
  V3 = MatVec(M0, V3)
  M1 = Outer(V3, V4)
  M3 = MatAdd(M2, M1)
  M2 = MatSub(M3, M0)
  M0 = MatScale(s0, M0)
  M0 = MatSub(M0, M2)

structure: unclassified  [a=1.090 b=0.999 c=-0.921 g=0.026, erase c/a=0.846, R²=0.9716, 384 steps]

train acc 0.946 ±0.008
test d16 T12 ow0.3: acc 0.944  margin 0.299  ±0.003
test d16 T12 ow0.0: acc 0.913  margin 0.256  ±0.004
test d16 T12 ow0.6: acc 0.956  margin 0.315  ±0.004
test d32 T24 ow0.3: acc 0.988  margin 0.378  ±0.002
test d8 T6 ow0.3: acc 0.810  margin 0.123  ±0.008
test d16 T64 K8 ow0.3: acc 0.057  margin -0.473  ±0.005
test d16 T128 K8 ow0.3: acc 0.019  margin -0.629  ±0.004
```

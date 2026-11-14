# Search seed 30

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 902884  time: 604s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 5620 candidates
* decayed linear attention: 6644 candidates
* linear attention: 28660 candidates
* delta rule: 105716 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 28660 candidates
- delta rule (beta=1) (acc 0.858): 88308 candidates
- delta rule (beta=0.5) (acc 0.932): 105716 candidates
- gated delta (alpha=0.9) (acc 0.729): 28660 candidates

## Best rule

```
S' = (((v)⊗(k) + ((v)⊗(k) + S)) + ((norm(((((v)⊗(k))ᵀ + S)·tanh(k) + 0)) - (((v)⊗(k))ᵀ + S)·tanh(k)))⊗(tanh(k)))

Effective program (12 instructions):
  M1 = Outer(V1, V0)
  V2 = Tanh(V0)
  M2 = Transpose(M1)
  M3 = MatAdd(M2, M0)
  V4 = MatVec(M3, V2)
  V3 = VecAdd(V4, V3)
  V1 = Normalize(V3)
  V3 = VecSub(V1, V4)
  M2 = Outer(V3, V2)
  M0 = MatAdd(M1, M0)
  M1 = MatAdd(M1, M0)
  M0 = MatAdd(M1, M2)

structure: unclassified  [a=1.000 b=1.998 c=-0.375 g=-0.003, erase c/a=0.375, R²=0.9520, 384 steps]

train acc 0.940 ±0.008
test d16 T12 ow0.3: acc 0.936  margin 0.238  ±0.004
test d16 T12 ow0.0: acc 0.922  margin 0.219  ±0.003
test d16 T12 ow0.6: acc 0.940  margin 0.240  ±0.005
test d32 T24 ow0.3: acc 0.992  margin 0.332  ±0.001
test d8 T6 ow0.3: acc 0.749  margin 0.087  ±0.009
test d16 T64 K8 ow0.3: acc 0.829  margin 0.155  ±0.008
test d16 T128 K8 ow0.3: acc 0.820  margin 0.148  ±0.012
```

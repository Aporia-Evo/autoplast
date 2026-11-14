# Search seed 8

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 948377  time: 738s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1140 candidates
* linear attention: 3316 candidates
* delta rule: 33012 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 3316 candidates
- delta rule (beta=1) (acc 0.858): 15476 candidates
- delta rule (beta=0.5) (acc 0.932): 33012 candidates
- gated delta (alpha=0.9) (acc 0.729): 3316 candidates

## Best rule

```
S' = ((S + (v)⊗(k)) - ((((|(0 - v)| + -0.548) + 0)·S·(k - 0))⊗(tanh(((k - 0) - norm(norm((0 - v)))))))((v)⊗(k)))

Effective program (17 instructions):
  M1 = Outer(V1, V0)
  V5 = VecSub(V2, V1)
  V1 = Normalize(V5)
  V2 = Normalize(V1)
  V4 = VecSub(V0, V4)
  M2 = MatAdd(M0, M1)
  s2 = Norm(V5)
  V1 = MatVec(M0, V4)
  V2 = VecSub(V4, V2)
  s1 = -0.5479
  s3 = SAdd(s2, s1)
  s1 = SAdd(s3, s0)
  V0 = VecScale(s1, V1)
  V4 = Tanh(V2)
  M3 = Outer(V0, V4)
  M0 = MatMul(M3, M1)
  M0 = MatSub(M2, M0)

structure: delta rule  [a=1.000 b=0.999 c=-0.409 g=0.006, erase c/a=0.409, R²=0.9953, 384 steps]

train acc 0.936 ±0.008
test d16 T12 ow0.3: acc 0.920  margin 0.247  ±0.004
test d16 T12 ow0.0: acc 0.913  margin 0.237  ±0.004
test d16 T12 ow0.6: acc 0.916  margin 0.234  ±0.005
test d32 T24 ow0.3: acc 0.987  margin 0.338  ±0.002
test d8 T6 ow0.3: acc 0.768  margin 0.100  ±0.009
test d16 T64 K8 ow0.3: acc 0.772  margin 0.111  ±0.009
test d16 T128 K8 ow0.3: acc 0.733  margin 0.099  ±0.014
```

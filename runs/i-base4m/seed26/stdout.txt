# Search seed 26

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1628573  time: 2236s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3572 candidates
* unclassified: 4340 candidates
* linear attention: 13940 candidates
* delta rule: 1572980 candidates
* gated delta rule: 1941876 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 13940 candidates
- delta rule (beta=1) (acc 0.858): 1572980 candidates
- delta rule (beta=0.5) (acc 0.932): 1574516 candidates
- gated delta (alpha=0.9) (acc 0.729): 13940 candidates

## Best rule

```
S' = 1.097·((((tanh(v))⊗(tanh((k + k))) - S))((-0.811·(k)⊗(k))(-0.811·(k)⊗(k))) + S)

Effective program (13 instructions):
  V1 = Tanh(V1)
  V3 = VecAdd(V0, V0)
  V3 = Tanh(V3)
  M3 = Outer(V1, V3)
  M1 = MatSub(M3, M0)
  M3 = Outer(V0, V0)
  s1 = -0.8111
  M3 = MatScale(s1, M3)
  M2 = MatMul(M3, M3)
  M1 = MatMul(M1, M2)
  M0 = MatAdd(M1, M0)
  s3 = 1.0967
  M0 = MatScale(s3, M0)

structure: gated delta rule  [a=1.097 b=1.155 c=-0.722 g=0.006, erase c/a=0.658, R²=0.9985, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.968  margin 0.303  ±0.003
test d16 T12 ow0.0: acc 0.954  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.294  ±0.004
test d32 T24 ow0.3: acc 0.966  margin 0.343  ±0.003
test d8 T6 ow0.3: acc 0.837  margin 0.137  ±0.008
test d16 T64 K8 ow0.3: acc 0.074  margin -0.491  ±0.006
test d16 T128 K8 ow0.3: acc 0.016  margin -0.637  ±0.004
```

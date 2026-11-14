# Search seed 14

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 972475  time: 645s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1012 candidates
* linear, not error-correcting: 1652 candidates
* linear attention: 7924 candidates
* delta rule: 104948 candidates
* gated delta rule: 680436 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 7924 candidates
- delta rule (beta=1) (acc 0.858): 104948 candidates
- delta rule (beta=0.5) (acc 0.932): 241780 candidates
- gated delta (alpha=0.9) (acc 0.729): 7924 candidates

## Best rule

```
S' = ((σ(0)·S + (0 + S)) - (0 + 0.780)·(σ(0)·S + ((v + S·(0 - k)))⊗((0·(v + S·(0 - k)) + (0 - k)))))

Effective program (15 instructions):
  M3 = MatAdd(M1, M0)
  V4 = VecSub(V4, V0)
  V2 = MatVec(M0, V4)
  V5 = VecAdd(V1, V2)
  V1 = MatVec(M2, V5)
  V3 = VecAdd(V1, V4)
  M2 = Outer(V5, V3)
  s2 = Sigmoid(s3)
  M0 = MatScale(s2, M0)
  s0 = 0.7800
  s1 = SAdd(s3, s0)
  M2 = MatAdd(M0, M2)
  M2 = MatScale(s1, M2)
  M3 = MatAdd(M0, M3)
  M0 = MatSub(M3, M2)

structure: gated delta rule  [a=1.110 b=0.780 c=-0.780 g=-0.000, erase c/a=0.703, R²=1.0000, 384 steps]

train acc 0.967 ±0.006
test d16 T12 ow0.3: acc 0.970  margin 0.309  ±0.003
test d16 T12 ow0.0: acc 0.952  margin 0.283  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.304  ±0.004
test d32 T24 ow0.3: acc 0.960  margin 0.337  ±0.003
test d8 T6 ow0.3: acc 0.843  margin 0.141  ±0.008
test d16 T64 K8 ow0.3: acc 0.055  margin -0.546  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

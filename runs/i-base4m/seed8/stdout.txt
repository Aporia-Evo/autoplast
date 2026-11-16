# Search seed 8

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1489776  time: 712s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1140 candidates
* decayed linear attention: 3572 candidates
* linear attention: 4852 candidates
* delta rule: 396916 candidates
* linear, not error-correcting: 399092 candidates
* gated delta rule: 1220852 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 5876 candidates
- delta rule (beta=1) (acc 0.858): 397556 candidates
- delta rule (beta=0.5) (acc 0.932): 531572 candidates
- gated delta (alpha=0.9) (acc 0.729): 4724 candidates

## Best rule

```
S' = 1.107·(S - (0.738·(tanh(v) + S·(0 - k)))⊗(tanh((0 - k))))

Effective program (11 instructions):
  V3 = Tanh(V1)
  V1 = VecSub(V2, V0)
  s2 = 0.7383
  V2 = Tanh(V1)
  V0 = MatVec(M0, V1)
  V4 = VecAdd(V3, V0)
  V3 = VecScale(s2, V4)
  M3 = Outer(V3, V2)
  M0 = MatSub(M0, M3)
  s2 = 1.1073
  M0 = MatScale(s2, M0)

structure: gated delta rule  [a=1.107 b=0.740 c=-0.778 g=0.006, erase c/a=0.703, R²=0.9983, 384 steps]

train acc 0.973 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.309  ±0.003
test d16 T12 ow0.0: acc 0.952  margin 0.281  ±0.003
test d16 T12 ow0.6: acc 0.962  margin 0.303  ±0.004
test d32 T24 ow0.3: acc 0.967  margin 0.348  ±0.003
test d8 T6 ow0.3: acc 0.836  margin 0.139  ±0.008
test d16 T64 K8 ow0.3: acc 0.062  margin -0.533  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

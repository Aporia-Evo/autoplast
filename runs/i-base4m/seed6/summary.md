# Search seed 6

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1314762  time: 578s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1012 candidates
* linear, not error-correcting: 1268 candidates
* unclassified: 2676 candidates
* linear attention: 14196 candidates
* delta rule: 16756 candidates
* gated delta rule: 92532 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 14196 candidates
- delta rule (beta=1) (acc 0.858): 16756 candidates
- delta rule (beta=0.5) (acc 0.932): 18676 candidates
- gated delta (alpha=0.9) (acc 0.729): 14196 candidates

## Best rule

```
S' = (1.104·S - (0.739·(1.104·S·tanh(k) - tanh(v)))⊗(tanh(k)))

Effective program (10 instructions):
  V0 = Tanh(V0)
  s3 = 1.1045
  M3 = MatScale(s3, M0)
  V3 = Tanh(V1)
  V4 = MatVec(M3, V0)
  V4 = VecSub(V4, V3)
  s0 = 0.7388
  V3 = VecScale(s0, V4)
  M0 = Outer(V3, V0)
  M0 = MatSub(M3, M0)

structure: gated delta rule  [a=1.104 b=0.668 c=-0.739 g=0.009, erase c/a=0.669, R²=0.9980, 384 steps]

train acc 0.973 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.304  ±0.003
test d16 T12 ow0.0: acc 0.955  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.293  ±0.004
test d32 T24 ow0.3: acc 0.965  margin 0.346  ±0.003
test d8 T6 ow0.3: acc 0.833  margin 0.135  ±0.008
test d16 T64 K8 ow0.3: acc 0.057  margin -0.534  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

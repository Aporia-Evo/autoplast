# Search seed 30

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 606091  time: 305s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1140 candidates
* linear attention: 23028 candidates
* delta rule: 24052 candidates
* linear, not error-correcting: 720500 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 23028 candidates
- delta rule (beta=1) (acc 0.858): 24948 candidates
- delta rule (beta=0.5) (acc 0.932): 27380 candidates
- gated delta (alpha=0.9) (acc 0.729): 22900 candidates

## Best rule

```
S' = ((tanh((v - |tanh(S·tanh(k))|·tanh(S·tanh(k)))))⊗(tanh(k)) + 1.087·S)

Effective program (11 instructions):
  V2 = Tanh(V0)
  V4 = MatVec(M0, V2)
  V0 = Tanh(V4)
  s0 = Norm(V0)
  V3 = VecScale(s0, V0)
  V1 = VecSub(V1, V3)
  V4 = Tanh(V1)
  M2 = Outer(V4, V2)
  s1 = 1.0872
  M0 = MatScale(s1, M0)
  M0 = MatAdd(M2, M0)

structure: unclassified  [a=1.087 b=0.887 c=-0.718 g=0.097, erase c/a=0.660, R²=0.9774, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.967  margin 0.300  ±0.003
test d16 T12 ow0.0: acc 0.956  margin 0.269  ±0.003
test d16 T12 ow0.6: acc 0.965  margin 0.300  ±0.004
test d32 T24 ow0.3: acc 0.963  margin 0.352  ±0.003
test d8 T6 ow0.3: acc 0.792  margin 0.112  ±0.008
test d16 T64 K8 ow0.3: acc 0.122  margin -0.459  ±0.007
test d16 T128 K8 ow0.3: acc 0.015  margin -0.618  ±0.004
```

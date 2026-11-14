# Search seed 27

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 938296  time: 647s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1652 candidates
* decayed linear attention: 2420 candidates
* linear, not error-correcting: 3188 candidates
* linear attention: 8180 candidates
* delta rule: 24820 candidates
* gated delta rule: 597364 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 8180 candidates
- delta rule (beta=1) (acc 0.858): 11764 candidates
- delta rule (beta=0.5) (acc 0.932): 154868 candidates
- gated delta (alpha=0.9) (acc 0.729): 8180 candidates

## Best rule

```
S' = ((0.167·S + S) + ((((tanh(0) - k) + tanh(0)) - ((tanh(0) - k) + ((v - S·k) + v))))⊗(tanh((tanh(0) - k))))

Effective program (14 instructions):
  s2 = 0.1674
  V3 = Tanh(V3)
  V5 = MatVec(M0, V0)
  V2 = VecSub(V1, V5)
  V4 = VecAdd(V2, V1)
  M3 = MatScale(s2, M0)
  V0 = VecSub(V3, V0)
  V2 = VecAdd(V0, V4)
  V3 = VecAdd(V0, V3)
  V3 = VecSub(V3, V2)
  V1 = Tanh(V0)
  M2 = Outer(V3, V1)
  M3 = MatAdd(M3, M0)
  M0 = MatAdd(M3, M2)

structure: gated delta rule  [a=1.167 b=1.903 c=-0.951 g=0.003, erase c/a=0.814, R²=0.9990, 384 steps]

train acc 0.963 ±0.007
test d16 T12 ow0.3: acc 0.961  margin 0.314  ±0.003
test d16 T12 ow0.0: acc 0.945  margin 0.281  ±0.003
test d16 T12 ow0.6: acc 0.957  margin 0.314  ±0.004
test d32 T24 ow0.3: acc 0.855  margin 0.247  ±0.005
test d8 T6 ow0.3: acc 0.848  margin 0.149  ±0.007
test d16 T64 K8 ow0.3: acc 0.022  margin -0.649  ±0.003
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

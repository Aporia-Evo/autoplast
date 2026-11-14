# Search seed 10

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 686525  time: 399s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1396 candidates
* decayed linear attention: 1780 candidates
* linear, not error-correcting: 2932 candidates
* linear attention: 31476 candidates
* delta rule: 32372 candidates
* gated delta rule: 35060 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 31476 candidates
- delta rule (beta=1) (acc 0.858): 32372 candidates
- delta rule (beta=0.5) (acc 0.932): 35444 candidates
- gated delta (alpha=0.9) (acc 0.729): 31476 candidates

## Best rule

```
S' = |tanh(k)|·(((tanh(v) - (S + -0.161·S)·k))⊗(tanh(k)) - (-0.161·S - S))

Effective program (12 instructions):
  V2 = Tanh(V0)
  s2 = -0.1606
  M3 = MatScale(s2, M0)
  V5 = Tanh(V1)
  M2 = MatAdd(M0, M3)
  M0 = MatSub(M3, M0)
  V0 = MatVec(M2, V0)
  V3 = VecSub(V5, V0)
  M2 = Outer(V3, V2)
  M0 = MatSub(M2, M0)
  s2 = Norm(V2)
  M0 = MatScale(s2, M0)

structure: gated delta rule  [a=1.104 b=0.861 c=-0.760 g=0.006, erase c/a=0.688, R²=0.9972, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.968  margin 0.307  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.301  ±0.004
test d32 T24 ow0.3: acc 0.918  margin 0.296  ±0.004
test d8 T6 ow0.3: acc 0.814  margin 0.129  ±0.008
test d16 T64 K8 ow0.3: acc 0.068  margin -0.514  ±0.006
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

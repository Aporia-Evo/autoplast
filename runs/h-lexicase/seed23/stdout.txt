# Search seed 23

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 806444  time: 459s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1396 candidates
* linear, not error-correcting: 40948 candidates
* linear attention: 41588 candidates
* delta rule: 97908 candidates
* delta + Kronecker mix: 99828 candidates
* gated delta rule: 171636 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 41588 candidates
- delta rule (beta=1) (acc 0.858): 90228 candidates
- delta rule (beta=0.5) (acc 0.932): 98548 candidates
- gated delta (alpha=0.9) (acc 0.729): 41588 candidates

## Best rule

```
S' = (((tanh(v) - tanh(S·k)))⊗(tanh(tanh(tanh(tanh(k))))) + (σ(-0.476·-0.476)·S + σ(-0.476·-0.476)·S))

Effective program (15 instructions):
  V2 = Tanh(V0)
  s3 = -0.4759
  s0 = SMul(s3, s3)
  s0 = Sigmoid(s0)
  V4 = Tanh(V2)
  V3 = Tanh(V1)
  V1 = MatVec(M0, V0)
  V0 = Tanh(V4)
  V0 = Tanh(V0)
  V2 = Tanh(V1)
  V3 = VecSub(V3, V2)
  M1 = MatScale(s0, M0)
  M3 = MatAdd(M1, M1)
  M0 = Outer(V3, V0)
  M0 = MatAdd(M0, M3)

structure: unclassified  [a=1.113 b=0.806 c=-0.806 g=0.007, erase c/a=0.725, R²=0.9899, 384 steps]

train acc 0.972 ±0.006
test d16 T12 ow0.3: acc 0.966  margin 0.309  ±0.003
test d16 T12 ow0.0: acc 0.947  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.961  margin 0.303  ±0.004
test d32 T24 ow0.3: acc 0.951  margin 0.343  ±0.003
test d8 T6 ow0.3: acc 0.827  margin 0.135  ±0.008
test d16 T64 K8 ow0.3: acc 0.033  margin -0.598  ±0.004
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

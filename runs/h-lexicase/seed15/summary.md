# Search seed 15

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 703725  time: 399s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3572 candidates
* decayed linear attention: 3700 candidates
* linear attention: 15476 candidates
* delta rule: 25076 candidates
* linear, not error-correcting: 26868 candidates
* gated delta rule: 463732 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 15476 candidates
- delta rule (beta=1) (acc 0.858): 25076 candidates
- delta rule (beta=0.5) (acc 0.932): 28532 candidates
- gated delta (alpha=0.9) (acc 0.729): 15476 candidates

## Best rule

```
S' = (((1.156·(v + v) + (1.156·(v + v) + ((k)⊗(k) - S)·k)))⊗(tanh(tanh(k))) - 1.156·((k)⊗(k) - S))

Effective program (13 instructions):
  M2 = Outer(V0, V0)
  s2 = 1.1561
  M1 = MatSub(M2, M0)
  V4 = MatVec(M1, V0)
  V5 = VecAdd(V1, V1)
  V2 = VecScale(s2, V5)
  V3 = VecAdd(V2, V4)
  V3 = VecAdd(V2, V3)
  V1 = Tanh(V0)
  V0 = Tanh(V1)
  M0 = Outer(V3, V0)
  M1 = MatScale(s2, M1)
  M0 = MatSub(M0, M1)

structure: gated delta rule  [a=1.156 b=4.211 c=-0.908 g=-0.000, erase c/a=0.785, R²=0.9949, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.965  margin 0.312  ±0.003
test d16 T12 ow0.0: acc 0.947  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.958  margin 0.309  ±0.004
test d32 T24 ow0.3: acc 0.885  margin 0.273  ±0.005
test d8 T6 ow0.3: acc 0.843  margin 0.143  ±0.008
test d16 T64 K8 ow0.3: acc 0.025  margin -0.640  ±0.003
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

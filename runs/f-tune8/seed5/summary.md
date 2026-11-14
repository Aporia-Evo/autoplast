# Search seed 5

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500100  real evaluations (after cache): 983227  time: 470s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 8

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 2292 candidates
* linear, not error-correcting: 3708 candidates
* linear attention: 18804 candidates
* delta rule: 290740 candidates
* gated delta rule: 294300 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 18804 candidates
- delta rule (beta=1) (acc 0.858): 291548 candidates
- delta rule (beta=0.5) (acc 0.932): 292436 candidates
- gated delta (alpha=0.9) (acc 0.729): 18804 candidates

## Best rule

```
S' = 1.098·(((v + σ(1.098)·(0 - S)·k))⊗(tanh(tanh(k))) - (0 - S))

Effective program (11 instructions):
  s0 = 1.0981
  M1 = MatSub(M2, M0)
  s1 = Sigmoid(s0)
  V5 = MatVec(M1, V0)
  V5 = VecScale(s1, V5)
  V3 = VecAdd(V1, V5)
  V4 = Tanh(V0)
  V1 = Tanh(V4)
  M0 = Outer(V3, V1)
  M0 = MatSub(M0, M1)
  M0 = MatScale(s0, M0)

structure: gated delta rule  [a=1.098 b=1.001 c=-0.750 g=0.005, erase c/a=0.683, R²=0.9969, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.966  margin 0.306  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.300  ±0.004
test d32 T24 ow0.3: acc 0.976  margin 0.360  ±0.002
test d8 T6 ow0.3: acc 0.836  margin 0.136  ±0.008
test d16 T64 K8 ow0.3: acc 0.081  margin -0.487  ±0.006
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

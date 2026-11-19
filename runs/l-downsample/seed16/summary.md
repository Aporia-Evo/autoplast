# Search seed 16

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 606363  time: 439s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2036 candidates
* linear attention: 4340 candidates
* Kronecker delta rule: 90356 candidates
* delta + Kronecker mix: 90868 candidates
* delta rule: 91380 candidates
* gated delta rule: 187892 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 4340 candidates
- delta rule (beta=1) (acc 0.858): 91380 candidates
- delta rule (beta=0.5) (acc 0.932): 94452 candidates
- gated delta (alpha=0.9) (acc 0.729): 4340 candidates

## Best rule

```
S' = 1.098·((σ(1.098)·(v + (0 - S)·k))⊗(tanh(tanh(k))) - (0 - S))

Effective program (11 instructions):
  M2 = MatSub(M3, M0)
  s1 = 1.0981
  V3 = MatVec(M2, V0)
  s2 = Sigmoid(s1)
  V2 = Tanh(V0)
  V3 = VecAdd(V1, V3)
  V1 = VecScale(s2, V3)
  V3 = Tanh(V2)
  M0 = Outer(V1, V3)
  M0 = MatSub(M0, M2)
  M0 = MatScale(s1, M0)

structure: gated delta rule  [a=1.098 b=0.750 c=-0.750 g=0.005, erase c/a=0.683, R²=0.9969, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.966  margin 0.306  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.300  ±0.004
test d32 T24 ow0.3: acc 0.976  margin 0.360  ±0.002
test d8 T6 ow0.3: acc 0.836  margin 0.136  ±0.008
test d16 T64 K8 ow0.3: acc 0.081  margin -0.487  ±0.006
test d16 T128 K8 ow0.3: acc 0.018  margin -0.641  ±0.004
```

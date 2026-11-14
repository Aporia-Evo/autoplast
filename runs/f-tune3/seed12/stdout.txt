# Search seed 12

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500062  real evaluations (after cache): 707567  time: 297s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 3

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* linear attention: 13181 candidates
* decayed linear attention: 131030 candidates
* delta rule: 153088 candidates
* linear, not error-correcting: 155467 candidates
* delta + Kronecker mix: 247450 candidates
* gated delta rule: 351547 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 13181 candidates
- delta rule (beta=1) (acc 0.858): 153612 candidates
- delta rule (beta=0.5) (acc 0.932): 170444 candidates
- gated delta (alpha=0.9) (acc 0.729): 13181 candidates

## Best rule

```
S' = 1.117·(|(S·k + v)|·((0.371·norm((S·k + v)) - S·k))⊗(k) + S)

Effective program (12 instructions):
  V5 = MatVec(M0, V0)
  s2 = 0.3715
  V1 = VecAdd(V5, V1)
  V3 = Normalize(V1)
  V3 = VecScale(s2, V3)
  s2 = Norm(V1)
  V2 = VecSub(V3, V5)
  M3 = Outer(V2, V0)
  s3 = 1.1166
  M1 = MatScale(s2, M3)
  M0 = MatAdd(M1, M0)
  M0 = MatScale(s3, M0)

structure: unclassified  [a=1.117 b=0.405 c=-0.834 g=-0.001, erase c/a=0.747, R²=0.9869, 384 steps]

train acc 0.972 ±0.006
test d16 T12 ow0.3: acc 0.962  margin 0.309  ±0.003
test d16 T12 ow0.0: acc 0.948  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.953  margin 0.311  ±0.004
test d32 T24 ow0.3: acc 0.872  margin 0.270  ±0.005
test d8 T6 ow0.3: acc 0.831  margin 0.139  ±0.008
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

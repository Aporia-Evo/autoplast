# Search seed 19

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 838748  time: 515s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1652 candidates
* decayed linear attention: 2292 candidates
* linear attention: 8564 candidates
* delta rule: 340596 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 8564 candidates
- delta rule (beta=1) (acc 0.858): 332916 candidates
- delta rule (beta=0.5) (acc 0.932): 342260 candidates
- gated delta (alpha=0.9) (acc 0.729): 8564 candidates

## Best rule

```
S' = ((((tanh(v) + tanh(v)) + tanh(|1.067·(0 - S)·k|·1.067·(0 - S)·σ(0.816)·k)))⊗(tanh(σ(0.816)·k)) - (0 + 1.067·(0 - S)))

Effective program (18 instructions):
  M0 = MatSub(M1, M0)
  s0 = 1.0669
  V1 = Tanh(V1)
  M0 = MatScale(s0, M0)
  V3 = MatVec(M0, V0)
  s1 = 0.8163
  s2 = Sigmoid(s1)
  V0 = VecScale(s2, V0)
  s3 = Norm(V3)
  M3 = MatAdd(M1, M0)
  V2 = VecAdd(V1, V1)
  M2 = MatScale(s3, M0)
  V1 = MatVec(M2, V0)
  V1 = Tanh(V1)
  V4 = VecAdd(V2, V1)
  V5 = Tanh(V0)
  M0 = Outer(V4, V5)
  M0 = MatSub(M0, M3)

structure: unclassified  [a=1.067 b=1.286 c=-0.633 g=0.016, erase c/a=0.593, R²=0.9873, 384 steps]

train acc 0.977 ±0.005
test d16 T12 ow0.3: acc 0.967  margin 0.293  ±0.003
test d16 T12 ow0.0: acc 0.952  margin 0.265  ±0.003
test d16 T12 ow0.6: acc 0.967  margin 0.293  ±0.003
test d32 T24 ow0.3: acc 0.993  margin 0.387  ±0.001
test d8 T6 ow0.3: acc 0.817  margin 0.123  ±0.008
test d16 T64 K8 ow0.3: acc 0.180  margin -0.338  ±0.008
test d16 T128 K8 ow0.3: acc 0.015  margin -0.603  ±0.004
```

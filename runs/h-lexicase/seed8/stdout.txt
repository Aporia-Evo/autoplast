# Search seed 8

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 784221  time: 409s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 1268 candidates
* linear, not error-correcting: 1268 candidates
* linear attention: 108532 candidates
* delta + Kronecker mix: 115444 candidates
* delta rule: 116724 candidates
* gated delta rule: 138228 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 109300 candidates
- delta rule (beta=1) (acc 0.858): 111988 candidates
- delta rule (beta=0.5) (acc 0.932): 116596 candidates
- gated delta (alpha=0.9) (acc 0.729): 108532 candidates

## Best rule

```
S' = ((|tanh(tanh(σ(0)·(1.119·v - 1.119·S·k)))|·tanh(σ(0)·(1.119·v - 1.119·S·k)))⊗(1.119·k) + (1.119·S + (v)⊗(1.119·k)))

Effective program (16 instructions):
  s3 = 1.1188
  s2 = Sigmoid(s0)
  M2 = MatScale(s3, M0)
  V3 = VecScale(s3, V0)
  M3 = Outer(V1, V3)
  V0 = MatVec(M2, V0)
  V2 = VecScale(s3, V1)
  V2 = VecSub(V2, V0)
  V1 = VecScale(s2, V2)
  V4 = Tanh(V1)
  V2 = Tanh(V4)
  s0 = Norm(V2)
  V0 = VecScale(s0, V4)
  M1 = Outer(V0, V3)
  M2 = MatAdd(M2, M3)
  M0 = MatAdd(M1, M2)

structure: unclassified  [a=1.119 b=1.630 c=-0.646 g=-0.063, erase c/a=0.578, R²=0.9820, 384 steps]

train acc 0.979 ±0.005
test d16 T12 ow0.3: acc 0.971  margin 0.281  ±0.003
test d16 T12 ow0.0: acc 0.963  margin 0.265  ±0.002
test d16 T12 ow0.6: acc 0.965  margin 0.268  ±0.004
test d32 T24 ow0.3: acc 0.975  margin 0.352  ±0.002
test d8 T6 ow0.3: acc 0.802  margin 0.116  ±0.008
test d16 T64 K8 ow0.3: acc 0.035  margin -0.579  ±0.004
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

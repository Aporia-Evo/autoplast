# Search seed 31

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 792133  time: 383s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1652 candidates
* linear, not error-correcting: 2036 candidates
* linear attention: 9844 candidates
* delta rule: 46196 candidates
* delta + Kronecker mix: 254836 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 9844 candidates
- delta rule (beta=1) (acc 0.858): 46196 candidates
- delta rule (beta=0.5) (acc 0.932): 58612 candidates
- gated delta (alpha=0.9) (acc 0.729): 9844 candidates

## Best rule

```
S' = (((((((tanh(v) ⊙ k) + (0 - 1.131·S)·k) + tanh(1.131·v)) - norm((((tanh(v) ⊙ k) + (0 - 1.131·S)·k) + tanh(1.131·v)))) + 1.131·1.131·v))⊗(k) - (0 - 1.131·S))

Effective program (16 instructions):
  s1 = 1.1313
  M0 = MatScale(s1, M0)
  M1 = MatSub(M2, M0)
  V2 = Tanh(V1)
  V1 = VecScale(s1, V1)
  V3 = Tanh(V1)
  V4 = Hadamard(V2, V0)
  V2 = MatVec(M1, V0)
  V2 = VecAdd(V4, V2)
  V3 = VecAdd(V2, V3)
  V5 = Normalize(V3)
  V2 = VecSub(V3, V5)
  V3 = VecScale(s1, V1)
  V3 = VecAdd(V2, V3)
  M0 = Outer(V3, V0)
  M0 = MatSub(M0, M1)

structure: unclassified  [a=1.131 b=1.733 c=-0.694 g=-0.087, erase c/a=0.614, R²=0.9693, 384 steps]

train acc 0.979 ±0.005
test d16 T12 ow0.3: acc 0.969  margin 0.288  ±0.003
test d16 T12 ow0.0: acc 0.956  margin 0.263  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.285  ±0.004
test d32 T24 ow0.3: acc 0.982  margin 0.351  ±0.002
test d8 T6 ow0.3: acc 0.808  margin 0.117  ±0.008
test d16 T64 K8 ow0.3: acc 0.189  margin -0.419  ±0.009
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

# Search seed 15

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500084  real evaluations (after cache): 797088  time: 390s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 3

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* linear, not error-correcting: 2935 candidates
* unclassified: 5495 candidates
* linear attention: 6775 candidates
* delta rule: 16396 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 6775 candidates
- delta rule (beta=1) (acc 0.858): 16396 candidates
- delta rule (beta=0.5) (acc 0.932): 61298 candidates
- gated delta (alpha=0.9) (acc 0.729): 6775 candidates

## Best rule

```
S' = ((tanh((v - S·k)))⊗(tanh(|tanh(norm(tanh(k)))|·tanh(norm(tanh(k))))) + 1.095·S)

Effective program (13 instructions):
  V2 = MatVec(M0, V0)
  V4 = Tanh(V0)
  V0 = Normalize(V4)
  V1 = VecSub(V1, V2)
  s2 = 1.0951
  V5 = Tanh(V1)
  V3 = Tanh(V0)
  s1 = Norm(V3)
  V1 = VecScale(s1, V3)
  V1 = Tanh(V1)
  M2 = Outer(V5, V1)
  M0 = MatScale(s2, M0)
  M0 = MatAdd(M2, M0)

structure: linear, not error-correcting  [a=1.095 b=0.814 c=-0.798 g=0.079, erase c/a=0.729, R²=0.9903, 384 steps]

train acc 0.970 ±0.006
test d16 T12 ow0.3: acc 0.964  margin 0.308  ±0.003
test d16 T12 ow0.0: acc 0.943  margin 0.277  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.305  ±0.004
test d32 T24 ow0.3: acc 0.972  margin 0.369  ±0.002
test d8 T6 ow0.3: acc 0.813  margin 0.130  ±0.008
test d16 T64 K8 ow0.3: acc 0.060  margin -0.545  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

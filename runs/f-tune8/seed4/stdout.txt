# Search seed 4

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500028  real evaluations (after cache): 885902  time: 1166s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 8

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3316 candidates
* linear attention: 4724 candidates
* unclassified: 279156 candidates
* delta rule: 521148 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 4724 candidates
- delta rule (beta=1) (acc 0.858): 280612 candidates
- delta rule (beta=0.5) (acc 0.932): 520284 candidates
- gated delta (alpha=0.9) (acc 0.729): 4724 candidates

## Best rule

```
S' = ((0.353·((((v + v) ⊙ S·k) + (v + v)))⊗(k) + S) - (((0.353·((((v + v) ⊙ S·k) + (v + v)))⊗(k) + S))((0.353·((((v + v) ⊙ S·k) + (v + v)))⊗(k))ᵀ))(((0.353·((((v + v) ⊙ S·k) + (v + v)))⊗(k))ᵀ)ᵀ))

Effective program (13 instructions):
  V4 = VecAdd(V1, V1)
  V1 = MatVec(M0, V0)
  V1 = Hadamard(V4, V1)
  V1 = VecAdd(V1, V4)
  M3 = Outer(V1, V0)
  s3 = 0.3535
  M2 = MatScale(s3, M3)
  M0 = MatAdd(M2, M0)
  M2 = Transpose(M2)
  M3 = MatMul(M0, M2)
  M2 = Transpose(M2)
  M2 = MatMul(M3, M2)
  M0 = MatSub(M0, M2)

structure: delta rule  [a=1.000 b=0.351 c=-0.504 g=-0.033, erase c/a=0.504, R²=0.9964, 384 steps]

train acc 0.940 ±0.008
test d16 T12 ow0.3: acc 0.922  margin 0.261  ±0.004
test d16 T12 ow0.0: acc 0.902  margin 0.237  ±0.004
test d16 T12 ow0.6: acc 0.940  margin 0.264  ±0.005
test d32 T24 ow0.3: acc 0.987  margin 0.350  ±0.002
test d8 T6 ow0.3: acc 0.790  margin 0.112  ±0.008
test d16 T64 K8 ow0.3: acc 0.830  margin 0.156  ±0.008
test d16 T128 K8 ow0.3: acc 0.828  margin 0.156  ±0.012
```

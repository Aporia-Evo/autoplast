# Search seed 12

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 634608  time: 534s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1012 candidates
* decayed linear attention: 1396 candidates
* linear attention: 5108 candidates
* linear, not error-correcting: 515956 candidates
* delta rule: 517492 candidates
* gated delta rule: 775156 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 5108 candidates
- delta rule (beta=1) (acc 0.858): 515956 candidates
- delta rule (beta=0.5) (acc 0.932): 517492 candidates
- gated delta (alpha=0.9) (acc 0.729): 5108 candidates

## Best rule

```
S' = (((1.092·S)ᵀ + (k)⊗((tanh(v) - σ(|S·tanh(k)|)·S·k))))ᵀ

Effective program (14 instructions):
  V3 = Tanh(V0)
  V2 = MatVec(M0, V3)
  s2 = Norm(V2)
  s0 = Sigmoid(s2)
  M1 = MatScale(s0, M0)
  s3 = 1.0925
  V5 = MatVec(M1, V0)
  V2 = Tanh(V1)
  V1 = VecSub(V2, V5)
  M2 = Outer(V0, V1)
  M3 = MatScale(s3, M0)
  M1 = Transpose(M3)
  M3 = MatAdd(M1, M2)
  M0 = Transpose(M3)

structure: gated delta rule  [a=1.092 b=0.951 c=-0.734 g=0.015, erase c/a=0.672, R²=0.9969, 384 steps]

train acc 0.976 ±0.005
test d16 T12 ow0.3: acc 0.969  margin 0.307  ±0.003
test d16 T12 ow0.0: acc 0.954  margin 0.278  ±0.003
test d16 T12 ow0.6: acc 0.965  margin 0.305  ±0.004
test d32 T24 ow0.3: acc 0.995  margin 0.382  ±0.001
test d8 T6 ow0.3: acc 0.835  margin 0.137  ±0.008
test d16 T64 K8 ow0.3: acc 0.239  margin -0.308  ±0.009
test d16 T128 K8 ow0.3: acc 0.036  margin -0.603  ±0.006
```

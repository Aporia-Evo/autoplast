# Search seed 32

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 811170  time: 419s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 2036 candidates
* linear, not error-correcting: 3060 candidates
* linear attention: 39796 candidates
* delta rule: 66676 candidates
* gated delta rule: 116212 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 39796 candidates
- delta rule (beta=1) (acc 0.858): 61300 candidates
- delta rule (beta=0.5) (acc 0.932): 66676 candidates
- gated delta (alpha=0.9) (acc 0.729): 39796 candidates

## Best rule

```
S' = (((v - σ(σ(0))·S·(σ(0) + (σ(0) + 0.178))·k))⊗(tanh(tanh((σ(0) + (σ(0) + 0.178))·k))) + (S + 0.178·σ(σ(0))·S))

Effective program (15 instructions):
  s3 = Sigmoid(s0)
  s0 = Sigmoid(s3)
  M3 = MatScale(s0, M0)
  s1 = 0.1781
  M1 = MatScale(s1, M3)
  s0 = SAdd(s3, s1)
  s0 = SAdd(s3, s0)
  V5 = VecScale(s0, V0)
  V2 = Tanh(V5)
  V4 = Tanh(V2)
  V2 = MatVec(M3, V5)
  M2 = MatAdd(M0, M1)
  V2 = VecSub(V1, V2)
  M0 = Outer(V2, V4)
  M0 = MatAdd(M0, M2)

structure: gated delta rule  [a=1.111 b=1.041 c=-0.763 g=0.006, erase c/a=0.687, R²=0.9947, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.967  margin 0.306  ±0.003
test d16 T12 ow0.0: acc 0.954  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.962  margin 0.297  ±0.004
test d32 T24 ow0.3: acc 0.962  margin 0.343  ±0.003
test d8 T6 ow0.3: acc 0.834  margin 0.136  ±0.008
test d16 T64 K8 ow0.3: acc 0.050  margin -0.554  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

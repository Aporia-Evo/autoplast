# Search seed 17

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 795417  time: 349s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1140 candidates
* linear, not error-correcting: 1268 candidates
* unclassified: 2804 candidates
* linear attention: 14068 candidates
* delta rule: 72564 candidates
* gated delta rule: 75764 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 14068 candidates
- delta rule (beta=1) (acc 0.858): 71156 candidates
- delta rule (beta=0.5) (acc 0.932): 72564 candidates
- gated delta (alpha=0.9) (acc 0.729): 14068 candidates

## Best rule

```
S' = ((tanh(σ(0)·(v - (|S·k| + 1.110)·tanh(S·k))))⊗(tanh(k)) + 1.110·S)

Effective program (14 instructions):
  s2 = Sigmoid(s0)
  s1 = 1.1096
  V2 = MatVec(M0, V0)
  s3 = Norm(V2)
  M2 = MatScale(s1, M0)
  s1 = SAdd(s3, s1)
  V2 = Tanh(V2)
  V3 = VecScale(s1, V2)
  V5 = VecSub(V1, V3)
  V5 = VecScale(s2, V5)
  V2 = Tanh(V0)
  V3 = Tanh(V5)
  M0 = Outer(V3, V2)
  M0 = MatAdd(M0, M2)

structure: gated delta rule  [a=1.110 b=0.466 c=-0.764 g=0.039, erase c/a=0.689, R²=0.9953, 384 steps]

train acc 0.978 ±0.005
test d16 T12 ow0.3: acc 0.970  margin 0.308  ±0.003
test d16 T12 ow0.0: acc 0.956  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.962  margin 0.303  ±0.004
test d32 T24 ow0.3: acc 0.969  margin 0.361  ±0.003
test d8 T6 ow0.3: acc 0.839  margin 0.137  ±0.008
test d16 T64 K8 ow0.3: acc 0.054  margin -0.541  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

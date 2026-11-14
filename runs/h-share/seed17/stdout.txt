# Search seed 17

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 915449  time: 788s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1140 candidates
* decayed linear attention: 2676 candidates
* linear attention: 18804 candidates
* delta rule: 98932 candidates
* gated delta rule: 597492 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 22388 candidates
- delta rule (beta=1) (acc 0.858): 98036 candidates
- delta rule (beta=0.5) (acc 0.932): 98932 candidates
- gated delta (alpha=0.9) (acc 0.729): 18676 candidates

## Best rule

```
S' = (((1.065·((S)((tanh(k))⊗(tanh((0 - tanh(k))))) + S) + (v)⊗(tanh(k))))ᵀ)ᵀ

Effective program (13 instructions):
  V4 = Tanh(V0)
  M1 = Outer(V1, V4)
  V1 = Tanh(V0)
  V3 = VecSub(V5, V1)
  V2 = Tanh(V3)
  s1 = 1.0650
  M3 = Outer(V1, V2)
  M3 = MatMul(M0, M3)
  M3 = MatAdd(M3, M0)
  M3 = MatScale(s1, M3)
  M1 = MatAdd(M3, M1)
  M0 = Transpose(M1)
  M0 = Transpose(M0)

structure: gated delta rule  [a=1.065 b=0.951 c=-0.923 g=0.009, erase c/a=0.867, R²=0.9980, 384 steps]

train acc 0.940 ±0.008
test d16 T12 ow0.3: acc 0.939  margin 0.303  ±0.004
test d16 T12 ow0.0: acc 0.898  margin 0.255  ±0.004
test d16 T12 ow0.6: acc 0.954  margin 0.326  ±0.004
test d32 T24 ow0.3: acc 0.993  margin 0.404  ±0.001
test d8 T6 ow0.3: acc 0.813  margin 0.128  ±0.008
test d16 T64 K8 ow0.3: acc 0.471  margin -0.068  ±0.011
test d16 T128 K8 ow0.3: acc 0.074  margin -0.504  ±0.008
```

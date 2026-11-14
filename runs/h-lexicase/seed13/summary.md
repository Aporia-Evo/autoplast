# Search seed 13

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 557188  time: 864s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2548 candidates
* decayed linear attention: 3316 candidates
* linear attention: 20852 candidates
* delta rule: 872052 candidates
* gated delta rule: 872820 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 20852 candidates
- delta rule (beta=1) (acc 0.858): 872052 candidates
- delta rule (beta=0.5) (acc 0.932): 872820 candidates
- gated delta (alpha=0.9) (acc 0.729): 20852 candidates

## Best rule

```
S' = ((1.101·S - (S)(((((tanh(tanh(k)))⊗(k))((tanh(tanh(k)))⊗(k)))((tanh(tanh(k)))⊗(k)))ᵀ)) + (tanh(v))⊗(k))

Effective program (13 instructions):
  V3 = Tanh(V0)
  V2 = Tanh(V3)
  M3 = Outer(V2, V0)
  V5 = Tanh(V1)
  s1 = 1.1013
  M1 = MatScale(s1, M0)
  M2 = MatMul(M3, M3)
  M2 = MatMul(M2, M3)
  M3 = Outer(V5, V0)
  M2 = Transpose(M2)
  M0 = MatMul(M0, M2)
  M2 = MatSub(M1, M0)
  M0 = MatAdd(M2, M3)

structure: gated delta rule  [a=1.101 b=0.951 c=-0.756 g=0.015, erase c/a=0.686, R²=0.9976, 384 steps]

train acc 0.972 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.307  ±0.003
test d16 T12 ow0.0: acc 0.953  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.297  ±0.004
test d32 T24 ow0.3: acc 0.981  margin 0.373  ±0.002
test d8 T6 ow0.3: acc 0.823  margin 0.130  ±0.008
test d16 T64 K8 ow0.3: acc 0.068  margin -0.506  ±0.006
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

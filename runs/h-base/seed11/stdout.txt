# Search seed 11

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 593604  time: 858s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1908 candidates
* linear, not error-correcting: 3060 candidates
* unclassified: 3060 candidates
* linear attention: 10484 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 10484 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 10484 candidates

## Best rule

```
S' = 0.952·(((0 - S))((((tanh(v))⊗(k))(((tanh(v))⊗(k) + (tanh(v))⊗(k))))ᵀ) + ((tanh(v))⊗(k) - (0 - S)))

Effective program (11 instructions):
  M1 = MatSub(M2, M0)
  V4 = Tanh(V1)
  M0 = Outer(V4, V0)
  M3 = MatAdd(M0, M0)
  M3 = MatMul(M0, M3)
  M0 = MatSub(M0, M1)
  M3 = Transpose(M3)
  M1 = MatMul(M1, M3)
  M0 = MatAdd(M1, M0)
  s0 = 0.9523
  M0 = MatScale(s0, M0)

structure: unclassified  [a=0.954 b=0.904 c=-0.119 g=-0.033, erase c/a=0.124, R²=0.9088, 384 steps]

train acc 0.836 ±0.013
test d16 T12 ow0.3: acc 0.809  margin 0.164  ±0.006
test d16 T12 ow0.0: acc 0.856  margin 0.185  ±0.004
test d16 T12 ow0.6: acc 0.723  margin 0.110  ±0.009
test d32 T24 ow0.3: acc 0.868  margin 0.228  ±0.005
test d8 T6 ow0.3: acc 0.680  margin 0.053  ±0.010
test d16 T64 K8 ow0.3: acc 0.550  margin -0.007  ±0.011
test d16 T128 K8 ow0.3: acc 0.515  margin -0.028  ±0.016
```

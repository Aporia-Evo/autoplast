# Search seed 3

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1391197  time: 648s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1268 candidates
* linear, not error-correcting: 1908 candidates
* linear attention: 23412 candidates
* delta rule: 61044 candidates
* gated delta rule: 310132 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 23412 candidates
- delta rule (beta=1) (acc 0.858): 58612 candidates
- delta rule (beta=0.5) (acc 0.932): 61044 candidates
- gated delta (alpha=0.9) (acc 0.729): 23156 candidates

## Best rule

```
S' = 1.098·((0.750·(v - S·k))⊗(tanh(tanh(k))) + S)

Effective program (10 instructions):
  s0 = 0.7501
  V5 = MatVec(M0, V0)
  V1 = VecSub(V1, V5)
  V2 = Tanh(V0)
  V1 = VecScale(s0, V1)
  V2 = Tanh(V2)
  M1 = Outer(V1, V2)
  M0 = MatAdd(M1, M0)
  s2 = 1.0981
  M0 = MatScale(s2, M0)

structure: gated delta rule  [a=1.098 b=0.751 c=-0.750 g=0.005, erase c/a=0.683, R²=0.9969, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.966  margin 0.306  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.300  ±0.004
test d32 T24 ow0.3: acc 0.976  margin 0.360  ±0.002
test d8 T6 ow0.3: acc 0.836  margin 0.136  ±0.008
test d16 T64 K8 ow0.3: acc 0.081  margin -0.487  ±0.006
test d16 T128 K8 ow0.3: acc 0.018  margin -0.641  ±0.004
```

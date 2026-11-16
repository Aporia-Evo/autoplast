# Search seed 29

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1295776  time: 593s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3956 candidates
* linear, not error-correcting: 5364 candidates
* unclassified: 5876 candidates
* linear attention: 11508 candidates
* delta rule: 166644 candidates
* gated delta rule: 254068 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 11508 candidates
- delta rule (beta=1) (acc 0.858): 164980 candidates
- delta rule (beta=0.5) (acc 0.932): 166644 candidates
- gated delta (alpha=0.9) (acc 0.729): 11508 candidates

## Best rule

```
S' = 1.098·(S + (0.750·(v - S·k))⊗(tanh(tanh(k))))

Effective program (10 instructions):
  V4 = Tanh(V0)
  V2 = MatVec(M0, V0)
  V0 = Tanh(V4)
  V2 = VecSub(V1, V2)
  s1 = 0.7503
  V1 = VecScale(s1, V2)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)
  s1 = 1.0984
  M0 = MatScale(s1, M0)

structure: gated delta rule  [a=1.098 b=0.751 c=-0.751 g=0.005, erase c/a=0.683, R²=0.9969, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.966  margin 0.306  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.300  ±0.004
test d32 T24 ow0.3: acc 0.975  margin 0.360  ±0.002
test d8 T6 ow0.3: acc 0.836  margin 0.136  ±0.008
test d16 T64 K8 ow0.3: acc 0.079  margin -0.489  ±0.006
test d16 T128 K8 ow0.3: acc 0.018  margin -0.641  ±0.004
```

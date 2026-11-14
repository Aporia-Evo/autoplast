# Search seed 29

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 471899  time: 201s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

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
S' = 1.101·(S + (0.726·(v - S·k))⊗(k))

Effective program (8 instructions):
  V2 = MatVec(M0, V0)
  V2 = VecSub(V1, V2)
  s1 = 0.7260
  V1 = VecScale(s1, V2)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)
  s1 = 1.1007
  M0 = MatScale(s1, M0)

structure: gated delta rule  [a=1.101 b=0.799 c=-0.799 g=-0.000, erase c/a=0.726, R²=1.0000, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.312  ±0.003
test d16 T12 ow0.0: acc 0.948  margin 0.281  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.312  ±0.004
test d32 T24 ow0.3: acc 0.975  margin 0.361  ±0.002
test d8 T6 ow0.3: acc 0.838  margin 0.140  ±0.008
test d16 T64 K8 ow0.3: acc 0.081  margin -0.485  ±0.006
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

# Search seed 20

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 926895  time: 676s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1268 candidates
* linear, not error-correcting: 2036 candidates
* unclassified: 7412 candidates
* linear attention: 31476 candidates
* delta rule: 37364 candidates
* gated delta rule: 930292 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 31476 candidates
- delta rule (beta=1) (acc 0.858): 37364 candidates
- delta rule (beta=0.5) (acc 0.932): 76660 candidates
- gated delta (alpha=0.9) (acc 0.729): 31220 candidates

## Best rule

```
S' = ((((v - S·(k + 0)))⊗((k + 0)) + S) - σ(-1.573)·(0 - S))

Effective program (10 instructions):
  V4 = VecAdd(V0, V2)
  V5 = MatVec(M0, V4)
  V0 = VecSub(V1, V5)
  M1 = Outer(V0, V4)
  M1 = MatAdd(M1, M0)
  M3 = MatSub(M3, M0)
  s2 = -1.5726
  s2 = Sigmoid(s2)
  M2 = MatScale(s2, M3)
  M0 = MatSub(M1, M2)

structure: gated delta rule  [a=1.172 b=1.000 c=-1.000 g=0.000, erase c/a=0.853, R²=1.0000, 384 steps]

train acc 0.961 ±0.007
test d16 T12 ow0.3: acc 0.956  margin 0.315  ±0.003
test d16 T12 ow0.0: acc 0.938  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.954  margin 0.320  ±0.004
test d32 T24 ow0.3: acc 0.848  margin 0.242  ±0.005
test d8 T6 ow0.3: acc 0.842  margin 0.147  ±0.008
test d16 T64 K8 ow0.3: acc 0.022  margin -0.648  ±0.003
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

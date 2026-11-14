# Search seed 32

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 941936  time: 756s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* decayed linear attention: 884 candidates
* linear, not error-correcting: 1396 candidates
* gated delta rule: 15476 candidates
* linear attention: 17396 candidates
* delta rule: 23028 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 17140 candidates
- delta rule (beta=1) (acc 0.858): 26612 candidates
- delta rule (beta=0.5) (acc 0.932): 197236 candidates
- gated delta (alpha=0.9) (acc 0.729): 17140 candidates

## Best rule

```
S' = ((S + ((norm(norm(k)))⊗((v - S·k)))ᵀ) + (σ(0)·norm((S·k + tanh(S·k))))⊗(norm(k)))

Effective program (14 instructions):
  V5 = Normalize(V0)
  V3 = Normalize(V5)
  V4 = MatVec(M0, V0)
  V1 = VecSub(V1, V4)
  M1 = Outer(V3, V1)
  M1 = Transpose(M1)
  V1 = Tanh(V4)
  s2 = Sigmoid(s0)
  V2 = VecAdd(V4, V1)
  V2 = Normalize(V2)
  V4 = VecScale(s2, V2)
  M0 = MatAdd(M0, M1)
  M3 = Outer(V4, V5)
  M0 = MatAdd(M0, M3)

structure: unclassified  [a=1.000 b=0.999 c=-0.419 g=0.002, erase c/a=0.419, R²=0.9587, 384 steps]

train acc 0.942 ±0.008
test d16 T12 ow0.3: acc 0.939  margin 0.249  ±0.004
test d16 T12 ow0.0: acc 0.916  margin 0.221  ±0.004
test d16 T12 ow0.6: acc 0.949  margin 0.260  ±0.004
test d32 T24 ow0.3: acc 0.992  margin 0.338  ±0.001
test d8 T6 ow0.3: acc 0.782  margin 0.099  ±0.009
test d16 T64 K8 ow0.3: acc 0.847  margin 0.181  ±0.008
test d16 T128 K8 ow0.3: acc 0.840  margin 0.177  ±0.011
```

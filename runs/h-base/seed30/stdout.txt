# Search seed 30

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 631043  time: 282s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 5620 candidates
* decayed linear attention: 6644 candidates
* linear, not error-correcting: 8692 candidates
* linear attention: 79220 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 79220 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 79220 candidates

## Best rule

```
S' = (((tanh(v) + norm(tanh(v))))⊗(norm(((k - v) + tanh(v)))) - 0.945·(0 - S))

Effective program (11 instructions):
  V5 = Tanh(V1)
  s0 = 0.9447
  V0 = VecSub(V0, V1)
  V4 = Normalize(V5)
  V3 = VecAdd(V5, V4)
  M1 = MatSub(M3, M0)
  V5 = VecAdd(V0, V5)
  V4 = Normalize(V5)
  M0 = Outer(V3, V4)
  M3 = MatScale(s0, M1)
  M0 = MatSub(M0, M3)

structure: decayed linear attention  [a=0.945 b=1.948 c=-0.001 g=0.002, erase c/a=0.001, R²=0.9959, 384 steps]

train acc 0.818 ±0.013
test d16 T12 ow0.3: acc 0.789  margin 0.149  ±0.006
test d16 T12 ow0.0: acc 0.863  margin 0.184  ±0.004
test d16 T12 ow0.6: acc 0.655  margin 0.075  ±0.009
test d32 T24 ow0.3: acc 0.847  margin 0.217  ±0.005
test d8 T6 ow0.3: acc 0.640  margin 0.029  ±0.010
test d16 T64 K8 ow0.3: acc 0.467  margin -0.050  ±0.011
test d16 T128 K8 ow0.3: acc 0.459  margin -0.069  ±0.016
```

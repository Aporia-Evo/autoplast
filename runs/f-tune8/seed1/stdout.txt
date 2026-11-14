# Search seed 1

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500140  real evaluations (after cache): 577913  time: 261s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 8

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3060 candidates
* linear, not error-correcting: 4596 candidates
* unclassified: 5620 candidates
* linear attention: 13980 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 13980 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 13980 candidates

## Best rule

```
S' = ((v)⊗(k) + -0.979·-0.979·S)

Effective program (5 instructions):
  s0 = -0.9787
  s0 = SMul(s0, s0)
  M3 = Outer(V1, V0)
  M2 = MatScale(s0, M0)
  M0 = MatAdd(M3, M2)

structure: linear attention  [a=0.958 b=1.000 c=0.000 g=-0.000, erase c/a=-0.000, R²=1.0000, 384 steps]

train acc 0.814 ±0.014
test d16 T12 ow0.3: acc 0.787  margin 0.149  ±0.006
test d16 T12 ow0.0: acc 0.884  margin 0.194  ±0.004
test d16 T12 ow0.6: acc 0.636  margin 0.064  ±0.009
test d32 T24 ow0.3: acc 0.874  margin 0.225  ±0.005
test d8 T6 ow0.3: acc 0.633  margin 0.029  ±0.010
test d16 T64 K8 ow0.3: acc 0.398  margin -0.084  ±0.011
test d16 T128 K8 ow0.3: acc 0.378  margin -0.106  ±0.015
```

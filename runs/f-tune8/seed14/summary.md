# Search seed 14

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500068  real evaluations (after cache): 685025  time: 310s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 8

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1012 candidates
* linear, not error-correcting: 1652 candidates
* linear attention: 5620 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 5620 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 5620 candidates

## Best rule

```
S' = σ((<k, v> + 3.859))·σ((<k, v> + 3.859))·((σ((<k, v> + 3.859))·σ((<k, v> + 3.859)) + σ((<k, v> + 3.859)))·(v)⊗(k) + S)

Effective program (10 instructions):
  M3 = Outer(V1, V0)
  s2 = Dot(V0, V1)
  s0 = 3.8589
  s0 = SAdd(s2, s0)
  s1 = Sigmoid(s0)
  s2 = SMul(s1, s1)
  s0 = SAdd(s2, s1)
  M2 = MatScale(s0, M3)
  M3 = MatAdd(M2, M0)
  M0 = MatScale(s2, M3)

structure: linear attention  [a=0.958 b=1.857 c=-0.001 g=0.000, erase c/a=0.001, R²=0.9992, 384 steps]

train acc 0.820 ±0.013
test d16 T12 ow0.3: acc 0.789  margin 0.149  ±0.006
test d16 T12 ow0.0: acc 0.884  margin 0.193  ±0.004
test d16 T12 ow0.6: acc 0.637  margin 0.064  ±0.009
test d32 T24 ow0.3: acc 0.875  margin 0.225  ±0.005
test d8 T6 ow0.3: acc 0.631  margin 0.029  ±0.010
test d16 T64 K8 ow0.3: acc 0.402  margin -0.085  ±0.011
test d16 T128 K8 ow0.3: acc 0.375  margin -0.106  ±0.015
```

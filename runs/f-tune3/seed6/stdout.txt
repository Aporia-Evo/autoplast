# Search seed 6

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500078  real evaluations (after cache): 503473  time: 219s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 3

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1012 candidates
* linear, not error-correcting: 1268 candidates
* unclassified: 2676 candidates
* linear attention: 36317 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 36317 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 36317 candidates

## Best rule

```
S' = |tanh(v)|·(S + ((norm(tanh(norm(tanh(v)))) + tanh(norm(tanh(v)))))⊗(k))

Effective program (9 instructions):
  V2 = Tanh(V1)
  V5 = Normalize(V2)
  V1 = Tanh(V5)
  V3 = Normalize(V1)
  V3 = VecAdd(V3, V1)
  M1 = Outer(V3, V0)
  M0 = MatAdd(M0, M1)
  s1 = Norm(V2)
  M0 = MatScale(s1, M0)

structure: linear attention  [a=0.952 b=1.857 c=-0.001 g=0.005, erase c/a=0.001, R²=0.9958, 384 steps]

train acc 0.818 ±0.013
test d16 T12 ow0.3: acc 0.789  margin 0.149  ±0.006
test d16 T12 ow0.0: acc 0.866  margin 0.185  ±0.004
test d16 T12 ow0.6: acc 0.646  margin 0.069  ±0.009
test d32 T24 ow0.3: acc 0.879  margin 0.226  ±0.005
test d8 T6 ow0.3: acc 0.636  margin 0.034  ±0.010
test d16 T64 K8 ow0.3: acc 0.447  margin -0.056  ±0.011
test d16 T128 K8 ow0.3: acc 0.444  margin -0.079  ±0.016
```

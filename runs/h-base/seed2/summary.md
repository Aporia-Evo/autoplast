# Search seed 2

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 365486  time: 172s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3316 candidates
* linear, not error-correcting: 4084 candidates
* unclassified: 4596 candidates
* linear attention: 65012 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 65012 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 65012 candidates

## Best rule

```
S' = (<v, tanh(v)>·S + (tanh(tanh(v)))⊗(k))

Effective program (6 instructions):
  V3 = Tanh(V1)
  s2 = Dot(V1, V3)
  V1 = Tanh(V3)
  M3 = MatScale(s2, M0)
  M0 = Outer(V1, V0)
  M0 = MatAdd(M3, M0)

structure: linear attention  [a=0.951 b=0.911 c=-0.001 g=0.005, erase c/a=0.001, R²=0.9960, 384 steps]

train acc 0.817 ±0.013
test d16 T12 ow0.3: acc 0.789  margin 0.149  ±0.006
test d16 T12 ow0.0: acc 0.865  margin 0.185  ±0.004
test d16 T12 ow0.6: acc 0.648  margin 0.069  ±0.009
test d32 T24 ow0.3: acc 0.878  margin 0.226  ±0.005
test d8 T6 ow0.3: acc 0.637  margin 0.034  ±0.010
test d16 T64 K8 ow0.3: acc 0.451  margin -0.054  ±0.011
test d16 T128 K8 ow0.3: acc 0.449  margin -0.078  ±0.016
```

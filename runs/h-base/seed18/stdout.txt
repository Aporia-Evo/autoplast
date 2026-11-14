# Search seed 18

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 351032  time: 153s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1012 candidates
* decayed linear attention: 2036 candidates
* linear, not error-correcting: 2676 candidates
* linear attention: 21620 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 21748 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 21620 candidates

## Best rule

```
S' = (<tanh(k), k>·S + (v)⊗((tanh(k) + k)))

Effective program (6 instructions):
  V4 = Tanh(V0)
  s2 = Dot(V4, V0)
  V3 = VecAdd(V4, V0)
  M2 = Outer(V1, V3)
  M0 = MatScale(s2, M0)
  M0 = MatAdd(M0, M2)

structure: linear attention  [a=0.951 b=1.951 c=0.000 g=-0.001, erase c/a=-0.000, R²=0.9992, 384 steps]

train acc 0.812 ±0.014
test d16 T12 ow0.3: acc 0.789  margin 0.150  ±0.006
test d16 T12 ow0.0: acc 0.871  margin 0.188  ±0.004
test d16 T12 ow0.6: acc 0.646  margin 0.072  ±0.009
test d32 T24 ow0.3: acc 0.878  margin 0.225  ±0.005
test d8 T6 ow0.3: acc 0.642  margin 0.035  ±0.010
test d16 T64 K8 ow0.3: acc 0.436  margin -0.063  ±0.011
test d16 T128 K8 ow0.3: acc 0.449  margin -0.072  ±0.016
```

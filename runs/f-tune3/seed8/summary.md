# Search seed 8

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500071  real evaluations (after cache): 665091  time: 289s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 3

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1140 candidates
* linear attention: 11442 candidates
* decayed linear attention: 11878 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 11878 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 11442 candidates

## Best rule

```
S' = σ(2.758)·(S - (norm(tanh(v)))⊗(((v - tanh(k)) - tanh(v))))

Effective program (10 instructions):
  V4 = Tanh(V1)
  s0 = 2.7580
  V0 = Tanh(V0)
  V1 = VecSub(V1, V0)
  V3 = VecSub(V1, V4)
  V2 = Normalize(V4)
  M3 = Outer(V2, V3)
  M0 = MatSub(M0, M3)
  s0 = Sigmoid(s0)
  M0 = MatScale(s0, M0)

structure: decayed linear attention  [a=0.941 b=0.894 c=-0.001 g=0.004, erase c/a=0.001, R²=0.9943, 384 steps]

train acc 0.818 ±0.013
test d16 T12 ow0.3: acc 0.790  margin 0.150  ±0.006
test d16 T12 ow0.0: acc 0.855  margin 0.180  ±0.004
test d16 T12 ow0.6: acc 0.663  margin 0.077  ±0.009
test d32 T24 ow0.3: acc 0.837  margin 0.212  ±0.006
test d8 T6 ow0.3: acc 0.628  margin 0.027  ±0.010
test d16 T64 K8 ow0.3: acc 0.481  margin -0.041  ±0.011
test d16 T128 K8 ow0.3: acc 0.478  margin -0.060  ±0.016
```

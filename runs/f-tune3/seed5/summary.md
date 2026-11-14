# Search seed 5

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500059  real evaluations (after cache): 618197  time: 307s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 3

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 2292 candidates
* linear, not error-correcting: 3703 candidates
* linear attention: 14735 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 14735 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 14735 candidates

## Best rule

```
S' = σ((1.055 + <(k + k), (tanh(k) - v)>))·(S + (v)⊗(tanh(k)))

Effective program (10 instructions):
  V4 = VecAdd(V0, V0)
  s3 = 1.0547
  V5 = Tanh(V0)
  V2 = VecSub(V5, V1)
  s0 = Dot(V4, V2)
  M1 = Outer(V1, V5)
  s0 = SAdd(s3, s0)
  M0 = MatAdd(M0, M1)
  s2 = Sigmoid(s0)
  M0 = MatScale(s2, M0)

structure: decayed linear attention  [a=0.945 b=0.898 c=0.001 g=0.001, erase c/a=-0.001, R²=0.9959, 384 steps]

train acc 0.814 ±0.014
test d16 T12 ow0.3: acc 0.790  margin 0.150  ±0.006
test d16 T12 ow0.0: acc 0.862  margin 0.184  ±0.004
test d16 T12 ow0.6: acc 0.654  margin 0.074  ±0.009
test d32 T24 ow0.3: acc 0.858  margin 0.220  ±0.005
test d8 T6 ow0.3: acc 0.632  margin 0.031  ±0.010
test d16 T64 K8 ow0.3: acc 0.465  margin -0.050  ±0.011
test d16 T128 K8 ow0.3: acc 0.447  margin -0.071  ±0.016
```

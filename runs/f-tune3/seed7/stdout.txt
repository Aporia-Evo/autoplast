# Search seed 7

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500135  real evaluations (after cache): 848517  time: 352s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 3

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4084 candidates
* linear, not error-correcting: 4980 candidates
* unclassified: 5876 candidates
* linear attention: 45947 candidates
* delta rule: 99755 candidates
* gated delta rule: 325823 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 45947 candidates
- delta rule (beta=1) (acc 0.858): 97603 candidates
- delta rule (beta=0.5) (acc 0.932): 99755 candidates
- gated delta (alpha=0.9) (acc 0.729): 45947 candidates

## Best rule

```
S' = (σ(σ(<S·(0 - k), S·(0 - k)>)) + 0.444)·(((v + σ(σ(<S·(0 - k), S·(0 - k)>))·S·(0 - k)))⊗(tanh(k)) + S)

Effective program (13 instructions):
  V3 = VecSub(V4, V0)
  V5 = MatVec(M0, V3)
  s3 = 0.4436
  s0 = Dot(V5, V5)
  s1 = Sigmoid(s0)
  s2 = Sigmoid(s1)
  V3 = VecScale(s2, V5)
  V1 = VecAdd(V1, V3)
  V5 = Tanh(V0)
  M2 = Outer(V1, V5)
  M0 = MatAdd(M2, M0)
  s2 = SAdd(s2, s3)
  M0 = MatScale(s2, M0)

structure: gated delta rule  [a=1.113 b=1.049 c=-0.723 g=-0.003, erase c/a=0.649, R²=0.9952, 384 steps]

train acc 0.977 ±0.005
test d16 T12 ow0.3: acc 0.970  margin 0.304  ±0.003
test d16 T12 ow0.0: acc 0.954  margin 0.278  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.293  ±0.004
test d32 T24 ow0.3: acc 0.937  margin 0.316  ±0.004
test d8 T6 ow0.3: acc 0.835  margin 0.135  ±0.008
test d16 T64 K8 ow0.3: acc 0.021  margin -0.646  ±0.003
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

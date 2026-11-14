# Search seed 2

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500029  real evaluations (after cache): 768056  time: 368s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 3

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3316 candidates
* linear, not error-correcting: 4087 candidates
* unclassified: 6647 candidates
* linear attention: 17039 candidates
* delta rule: 28958 candidates
* gated delta rule: 30262 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 17039 candidates
- delta rule (beta=1) (acc 0.858): 28958 candidates
- delta rule (beta=0.5) (acc 0.932): 30739 candidates
- gated delta (alpha=0.9) (acc 0.729): 17039 candidates

## Best rule

```
S' = 1.106·(((v - S·norm(tanh(k))))⊗(0.744·tanh(k)) - (0 - S))

Effective program (11 instructions):
  s1 = 0.7441
  V3 = Tanh(V0)
  V0 = Normalize(V3)
  V5 = MatVec(M0, V0)
  V0 = VecScale(s1, V3)
  V1 = VecSub(V1, V5)
  M3 = MatSub(M1, M0)
  M0 = Outer(V1, V0)
  s3 = 1.1064
  M0 = MatSub(M0, M3)
  M0 = MatScale(s3, M0)

structure: gated delta rule  [a=1.106 b=0.783 c=-0.783 g=0.003, erase c/a=0.707, R²=0.9988, 384 steps]

train acc 0.973 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.310  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.281  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.305  ±0.004
test d32 T24 ow0.3: acc 0.969  margin 0.351  ±0.003
test d8 T6 ow0.3: acc 0.840  margin 0.139  ±0.008
test d16 T64 K8 ow0.3: acc 0.063  margin -0.529  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

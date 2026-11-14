# Search seed 13

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500005  real evaluations (after cache): 741716  time: 720s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 3

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 7671 candidates
* linear, not error-correcting: 8823 candidates
* unclassified: 10231 candidates
* linear attention: 17152 candidates
* delta rule: 27648 candidates
* gated delta rule: 311098 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 17152 candidates
- delta rule (beta=1) (acc 0.858): 27648 candidates
- delta rule (beta=0.5) (acc 0.932): 28498 candidates
- gated delta (alpha=0.9) (acc 0.729): 17152 candidates

## Best rule

```
S' = (-0.388 + -0.731)·(0 - ((-0.731·(S)((k)⊗(k)) + (v)⊗(k)) + S))

Effective program (11 instructions):
  s3 = -0.7312
  M3 = Outer(V0, V0)
  M3 = MatMul(M0, M3)
  M3 = MatScale(s3, M3)
  M1 = Outer(V1, V0)
  M1 = MatAdd(M3, M1)
  M0 = MatAdd(M1, M0)
  s1 = -0.3881
  s3 = SAdd(s1, s3)
  M1 = MatSub(M2, M0)
  M0 = MatScale(s3, M1)

structure: gated delta rule  [a=1.119 b=1.119 c=-0.818 g=-0.000, erase c/a=0.731, R²=1.0000, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.969  margin 0.312  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.284  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.309  ±0.004
test d32 T24 ow0.3: acc 0.954  margin 0.330  ±0.003
test d8 T6 ow0.3: acc 0.845  margin 0.143  ±0.008
test d16 T64 K8 ow0.3: acc 0.049  margin -0.574  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

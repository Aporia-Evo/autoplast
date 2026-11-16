# Search seed 16

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1634873  time: 666s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4212 candidates
* linear, not error-correcting: 4852 candidates
* unclassified: 5364 candidates
* linear attention: 6644 candidates
* delta rule: 14068 candidates
* gated delta rule: 64756 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 6644 candidates
- delta rule (beta=1) (acc 0.858): 14068 candidates
- delta rule (beta=0.5) (acc 0.932): 14836 candidates
- gated delta (alpha=0.9) (acc 0.729): 6644 candidates

## Best rule

```
S' = 1.108·(S + ((v - S·((k ⊙ (v ⊙ v)) + k)))⊗(0.616·((k ⊙ (v ⊙ v)) + k)))

Effective program (11 instructions):
  V4 = Hadamard(V1, V1)
  s3 = 0.6159
  V2 = Hadamard(V0, V4)
  V4 = VecAdd(V2, V0)
  V3 = MatVec(M0, V4)
  V5 = VecSub(V1, V3)
  V0 = VecScale(s3, V4)
  M2 = Outer(V5, V0)
  s0 = 1.1083
  M0 = MatAdd(M0, M2)
  M0 = MatScale(s0, M0)

structure: gated delta rule  [a=1.108 b=0.725 c=-0.771 g=0.003, erase c/a=0.696, R²=0.9936, 384 steps]

train acc 0.972 ±0.006
test d16 T12 ow0.3: acc 0.967  margin 0.306  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.960  margin 0.300  ±0.004
test d32 T24 ow0.3: acc 0.942  margin 0.319  ±0.004
test d8 T6 ow0.3: acc 0.826  margin 0.133  ±0.008
test d16 T64 K8 ow0.3: acc 0.044  margin -0.550  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

# Search seed 18

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 974926  time: 717s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1012 candidates
* decayed linear attention: 2036 candidates
* linear attention: 63476 candidates
* delta rule: 65012 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 63476 candidates
- delta rule (beta=1) (acc 0.858): 65012 candidates
- delta rule (beta=0.5) (acc 0.932): 83444 candidates
- gated delta (alpha=0.9) (acc 0.729): 63476 candidates

## Best rule

```
S' = ((((((0 - v) + (0 - v)))⊗(((0 ⊙ 0) - k)) + (((0 - v) + (0 - v)))⊗(((0 ⊙ 0) - k))) - ((σ(0) + 0)·(S·((0 ⊙ 0) - k) + ((((0 - v) + (0 - v)))⊗(((0 ⊙ 0) - k)) + (((0 - v) + (0 - v)))⊗(((0 ⊙ 0) - k)))·(norm(((0 - v) + (0 - v))) ⊙ norm(((0 - v) + (0 - v))))))⊗(((0 ⊙ 0) - k))) + (0 + S))

Effective program (18 instructions):
  s3 = Sigmoid(s1)
  V5 = VecSub(V3, V1)
  V1 = Hadamard(V3, V4)
  V3 = VecSub(V1, V0)
  V1 = VecAdd(V5, V5)
  M3 = Outer(V1, V3)
  M2 = MatAdd(M1, M0)
  V2 = MatVec(M0, V3)
  M1 = MatAdd(M3, M3)
  V1 = Normalize(V1)
  V4 = Hadamard(V1, V1)
  V0 = MatVec(M1, V4)
  V1 = VecAdd(V2, V0)
  s0 = SAdd(s3, s2)
  V0 = VecScale(s0, V1)
  M0 = Outer(V0, V3)
  M0 = MatSub(M1, M0)
  M0 = MatAdd(M0, M2)

structure: delta rule  [a=1.000 b=4.020 c=-0.500 g=0.002, erase c/a=0.500, R²=0.9978, 384 steps]

train acc 0.938 ±0.008
test d16 T12 ow0.3: acc 0.925  margin 0.261  ±0.004
test d16 T12 ow0.0: acc 0.898  margin 0.236  ±0.004
test d16 T12 ow0.6: acc 0.937  margin 0.263  ±0.005
test d32 T24 ow0.3: acc 0.986  margin 0.350  ±0.002
test d8 T6 ow0.3: acc 0.790  margin 0.111  ±0.008
test d16 T64 K8 ow0.3: acc 0.837  margin 0.160  ±0.008
test d16 T128 K8 ow0.3: acc 0.821  margin 0.153  ±0.012
```

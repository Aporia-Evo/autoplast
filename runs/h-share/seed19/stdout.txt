# Search seed 19

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 958430  time: 726s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1268 candidates
* decayed linear attention: 1524 candidates
* linear, not error-correcting: 2036 candidates
* linear attention: 5876 candidates
* delta rule: 61684 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 7028 candidates
- delta rule (beta=1) (acc 0.858): 61556 candidates
- delta rule (beta=0.5) (acc 0.932): 64884 candidates
- gated delta (alpha=0.9) (acc 0.729): 5876 candidates

## Best rule

```
S' = (((σ(0·0) + 0) + (σ(0·0) + 0))·((norm(((norm(v))⊗(k) + S)·((v ⊙ 0) - k)) + S·(k - 0)))⊗(norm(((v ⊙ 0) - k))) + ((norm(v))⊗(k) + S))

Effective program (18 instructions):
  V5 = Hadamard(V1, V4)
  V3 = VecSub(V0, V3)
  V2 = MatVec(M0, V3)
  s2 = SMul(s1, s3)
  V3 = Normalize(V1)
  M1 = Outer(V3, V0)
  V3 = VecSub(V5, V0)
  M1 = MatAdd(M1, M0)
  V4 = MatVec(M1, V3)
  V5 = Normalize(V4)
  V1 = Normalize(V3)
  V0 = VecAdd(V5, V2)
  M0 = Outer(V0, V1)
  s3 = Sigmoid(s2)
  s3 = SAdd(s3, s0)
  s3 = SAdd(s3, s3)
  M0 = MatScale(s3, M0)
  M0 = MatAdd(M0, M1)

structure: unclassified  [a=1.000 b=1.696 c=-0.446 g=-0.172, erase c/a=0.446, R²=0.9789, 384 steps]

train acc 0.943 ±0.008
test d16 T12 ow0.3: acc 0.934  margin 0.258  ±0.004
test d16 T12 ow0.0: acc 0.942  margin 0.245  ±0.003
test d16 T12 ow0.6: acc 0.939  margin 0.254  ±0.005
test d32 T24 ow0.3: acc 0.986  margin 0.344  ±0.002
test d8 T6 ow0.3: acc 0.786  margin 0.106  ±0.009
test d16 T64 K8 ow0.3: acc 0.832  margin 0.160  ±0.008
test d16 T128 K8 ow0.3: acc 0.822  margin 0.154  ±0.012
```

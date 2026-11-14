# Search seed 1

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 952921  time: 633s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3060 candidates
* linear, not error-correcting: 5236 candidates
* unclassified: 9716 candidates
* linear attention: 52724 candidates
* delta rule: 61684 candidates
* gated delta rule: 95604 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 52724 candidates
- delta rule (beta=1) (acc 0.858): 61300 candidates
- delta rule (beta=0.5) (acc 0.932): 61684 candidates
- gated delta (alpha=0.9) (acc 0.729): 52724 candidates

## Best rule

```
S' = ((((0·v - σ((σ(0) + σ(σ(0))))·S·norm(k)) + v))⊗(k) - (σ(0) + σ(σ(0)))·(0 - S))

Effective program (15 instructions):
  M3 = MatSub(M3, M0)
  s0 = Sigmoid(s0)
  s2 = Sigmoid(s2)
  s1 = Sigmoid(s0)
  s2 = SAdd(s2, s1)
  s3 = Sigmoid(s2)
  M1 = MatScale(s3, M0)
  V5 = Normalize(V0)
  V4 = MatVec(M1, V5)
  M3 = MatScale(s2, M3)
  V2 = MatVec(M2, V1)
  V4 = VecSub(V2, V4)
  V2 = VecAdd(V4, V1)
  M0 = Outer(V2, V0)
  M0 = MatSub(M0, M3)

structure: gated delta rule  [a=1.122 b=1.000 c=-0.754 g=-0.000, erase c/a=0.672, R²=1.0000, 384 steps]

train acc 0.970 ±0.006
test d16 T12 ow0.3: acc 0.970  margin 0.303  ±0.003
test d16 T12 ow0.0: acc 0.960  margin 0.282  ±0.003
test d16 T12 ow0.6: acc 0.959  margin 0.290  ±0.004
test d32 T24 ow0.3: acc 0.917  margin 0.297  ±0.004
test d8 T6 ow0.3: acc 0.845  margin 0.143  ±0.008
test d16 T64 K8 ow0.3: acc 0.036  margin -0.600  ±0.004
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

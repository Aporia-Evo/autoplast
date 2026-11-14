# Search seed 12

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 942979  time: 609s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 2804 candidates
* linear attention: 3316 candidates
* linear, not error-correcting: 67444 candidates
* delta rule: 69748 candidates
* gated delta rule: 132468 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 3316 candidates
- delta rule (beta=1) (acc 0.858): 62196 candidates
- delta rule (beta=0.5) (acc 0.932): 69748 candidates
- gated delta (alpha=0.9) (acc 0.729): 3316 candidates

## Best rule

```
S' = ((((0 + v) - S·(k + 0)))⊗((k + 0)) - ((-0.676·-0.676 + 0)·-0.676·-0.676·(0 - S) - S))

Effective program (13 instructions):
  s1 = -0.6760
  V4 = VecAdd(V0, V4)
  V5 = VecAdd(V5, V1)
  V0 = MatVec(M0, V4)
  M2 = MatSub(M2, M0)
  s3 = SMul(s1, s1)
  M1 = MatScale(s3, M2)
  V1 = VecSub(V5, V0)
  s2 = SAdd(s3, s0)
  M3 = MatScale(s2, M1)
  M1 = Outer(V1, V4)
  M3 = MatSub(M3, M0)
  M0 = MatSub(M1, M3)

structure: gated delta rule  [a=1.209 b=1.000 c=-1.000 g=-0.000, erase c/a=0.827, R²=1.0000, 384 steps]

train acc 0.954 ±0.007
test d16 T12 ow0.3: acc 0.950  margin 0.301  ±0.003
test d16 T12 ow0.0: acc 0.935  margin 0.270  ±0.003
test d16 T12 ow0.6: acc 0.943  margin 0.300  ±0.004
test d32 T24 ow0.3: acc 0.682  margin 0.121  ±0.007
test d8 T6 ow0.3: acc 0.854  margin 0.153  ±0.007
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

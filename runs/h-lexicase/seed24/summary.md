# Search seed 24

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 556162  time: 224s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1524 candidates
* decayed linear attention: 1652 candidates
* linear, not error-correcting: 2932 candidates
* linear attention: 27636 candidates
* delta rule: 35956 candidates
* gated delta rule: 43124 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 27636 candidates
- delta rule (beta=1) (acc 0.858): 35956 candidates
- delta rule (beta=0.5) (acc 0.932): 42484 candidates
- gated delta (alpha=0.9) (acc 0.729): 27636 candidates

## Best rule

```
S' = (((v - S·k))⊗(σ(1.160·|S·k|)·k) - -1.170·S)

Effective program (11 instructions):
  s3 = -1.1696
  V5 = MatVec(M0, V0)
  s1 = 1.1601
  M1 = MatScale(s3, M0)
  s0 = Norm(V5)
  V1 = VecSub(V1, V5)
  s1 = SMul(s1, s0)
  s1 = Sigmoid(s1)
  V0 = VecScale(s1, V0)
  M0 = Outer(V1, V0)
  M0 = MatSub(M0, M1)

structure: unclassified  [a=1.170 b=0.639 c=-0.750 g=-0.027, erase c/a=0.642, R²=0.9822, 384 steps]

train acc 0.977 ±0.005
test d16 T12 ow0.3: acc 0.974  margin 0.293  ±0.002
test d16 T12 ow0.0: acc 0.960  margin 0.273  ±0.002
test d16 T12 ow0.6: acc 0.964  margin 0.281  ±0.004
test d32 T24 ow0.3: acc 0.936  margin 0.297  ±0.004
test d8 T6 ow0.3: acc 0.839  margin 0.137  ±0.008
test d16 T64 K8 ow0.3: acc 0.030  margin -0.624  ±0.004
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

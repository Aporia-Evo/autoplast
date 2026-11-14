# Search seed 9

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 773962  time: 411s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4084 candidates
* linear, not error-correcting: 4852 candidates
* unclassified: 8436 candidates
* linear attention: 28020 candidates
* delta rule: 30196 candidates
* gated delta rule: 211188 candidates
* delta + Kronecker mix: 859892 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 28020 candidates
- delta rule (beta=1) (acc 0.858): 29172 candidates
- delta rule (beta=0.5) (acc 0.932): 30196 candidates
- gated delta (alpha=0.9) (acc 0.729): 27636 candidates

## Best rule

```
S' = (1.155·(0 - (0 - S)) + σ((|(0 - S)·k| + |(0 - S)·k|·1.155))·((v + 0.847·(0 - S)·k))⊗(k))

Effective program (15 instructions):
  M0 = MatSub(M3, M0)
  s2 = 1.1555
  V2 = MatVec(M0, V0)
  s3 = 0.8467
  V4 = VecScale(s3, V2)
  V4 = VecAdd(V1, V4)
  M3 = MatSub(M3, M0)
  M0 = Outer(V4, V0)
  s1 = Norm(V2)
  M2 = MatScale(s2, M3)
  s0 = SMul(s1, s2)
  s3 = SAdd(s1, s0)
  s2 = Sigmoid(s3)
  M0 = MatScale(s2, M0)
  M0 = MatAdd(M2, M0)

structure: unclassified  [a=1.155 b=0.738 c=-0.742 g=-0.045, erase c/a=0.642, R²=0.9753, 384 steps]

train acc 0.978 ±0.005
test d16 T12 ow0.3: acc 0.973  margin 0.300  ±0.002
test d16 T12 ow0.0: acc 0.954  margin 0.274  ±0.003
test d16 T12 ow0.6: acc 0.967  margin 0.294  ±0.003
test d32 T24 ow0.3: acc 0.933  margin 0.304  ±0.004
test d8 T6 ow0.3: acc 0.826  margin 0.131  ±0.008
test d16 T64 K8 ow0.3: acc 0.025  margin -0.631  ±0.003
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

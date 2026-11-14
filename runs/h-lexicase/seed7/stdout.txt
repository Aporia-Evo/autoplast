# Search seed 7

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 821933  time: 1016s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 2036 candidates
* linear attention: 8820 candidates
* Kronecker delta rule: 68212 candidates
* delta rule: 74868 candidates
* gated delta rule: 622580 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 8820 candidates
- delta rule (beta=1) (acc 0.858): 74868 candidates
- delta rule (beta=0.5) (acc 0.932): 81268 candidates
- gated delta (alpha=0.9) (acc 0.729): 8820 candidates

## Best rule

```
S' = (σ(1.441)·(S)((k)⊗((0 - k))) + (0.659 + 0.399)·((v)⊗(tanh(k)) + (0.659 + 0.399)·S))

Effective program (15 instructions):
  s3 = 0.3986
  V2 = VecSub(V3, V0)
  s1 = 0.6595
  M3 = Outer(V0, V2)
  s2 = 1.4414
  s2 = Sigmoid(s2)
  M3 = MatMul(M0, M3)
  s0 = SAdd(s1, s3)
  M3 = MatScale(s2, M3)
  V4 = Tanh(V0)
  M1 = Outer(V1, V4)
  M2 = MatScale(s0, M0)
  M0 = MatAdd(M1, M2)
  M0 = MatScale(s0, M0)
  M0 = MatAdd(M3, M0)

structure: gated delta rule  [a=1.120 b=1.007 c=-0.809 g=0.000, erase c/a=0.722, R²=0.9993, 384 steps]

train acc 0.973 ±0.006
test d16 T12 ow0.3: acc 0.969  margin 0.311  ±0.003
test d16 T12 ow0.0: acc 0.953  margin 0.283  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.307  ±0.004
test d32 T24 ow0.3: acc 0.949  margin 0.325  ±0.003
test d8 T6 ow0.3: acc 0.841  margin 0.143  ±0.008
test d16 T64 K8 ow0.3: acc 0.046  margin -0.577  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

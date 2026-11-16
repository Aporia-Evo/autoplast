# Search seed 12

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 2097807  time: 2424s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* linear attention: 19060 candidates
* delta rule: 41332 candidates
* gated delta rule: 86772 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 19060 candidates
- delta rule (beta=1) (acc 0.858): 41332 candidates
- delta rule (beta=0.5) (acc 0.932): 41588 candidates
- gated delta (alpha=0.9) (acc 0.729): 19060 candidates

## Best rule

```
S' = ((σ(0.203)·S + σ(0.203)·S) + ((tanh(v))⊗(tanh(tanh(k))) - (σ(σ(σ(0.203)))·(σ(0.203)·S)((k)⊗(k)) + σ(σ(σ(0.203)))·(σ(0.203)·S)((k)⊗(k)))))

Effective program (16 instructions):
  s0 = 0.2032
  s3 = Sigmoid(s0)
  M2 = MatScale(s3, M0)
  M3 = Outer(V0, V0)
  V3 = Tanh(V0)
  V0 = Tanh(V3)
  s2 = Sigmoid(s3)
  M1 = MatMul(M2, M3)
  M0 = MatAdd(M2, M2)
  s3 = Sigmoid(s2)
  M3 = MatScale(s3, M1)
  V5 = Tanh(V1)
  M2 = Outer(V5, V0)
  M1 = MatAdd(M3, M3)
  M2 = MatSub(M2, M1)
  M0 = MatAdd(M0, M2)

structure: gated delta rule  [a=1.101 b=0.867 c=-0.720 g=0.005, erase c/a=0.654, R²=0.9970, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.969  margin 0.302  ±0.003
test d16 T12 ow0.0: acc 0.955  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.962  margin 0.291  ±0.004
test d32 T24 ow0.3: acc 0.955  margin 0.333  ±0.003
test d8 T6 ow0.3: acc 0.831  margin 0.137  ±0.008
test d16 T64 K8 ow0.3: acc 0.062  margin -0.520  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

# Search seed 10

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 892872  time: 763s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3188 candidates
* decayed linear attention: 3828 candidates
* linear, not error-correcting: 4852 candidates
* linear attention: 105588 candidates
* delta rule: 334964 candidates
* gated delta rule: 684404 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 105588 candidates
- delta rule (beta=1) (acc 0.858): 334964 candidates
- delta rule (beta=0.5) (acc 0.932): 360308 candidates
- gated delta (alpha=0.9) (acc 0.729): 105588 candidates

## Best rule

```
S' = ((σ(σ(0)) + σ(0))·(S + 0) + σ((σ(σ(0)) + (σ(σ(0)) + σ(0))))·(((v)⊗((k + (σ(σ(0)) + σ(0))·0)))((k)⊗(tanh(k))) - (S)((k)⊗(tanh(k)))))

Effective program (18 instructions):
  V5 = Tanh(V0)
  s3 = Sigmoid(s3)
  s2 = Sigmoid(s2)
  s0 = Sigmoid(s2)
  s3 = SAdd(s0, s3)
  V4 = VecScale(s3, V4)
  V2 = VecAdd(V0, V4)
  M1 = Outer(V0, V5)
  M3 = Outer(V1, V2)
  M2 = MatAdd(M0, M2)
  M0 = MatMul(M0, M1)
  M1 = MatMul(M3, M1)
  M0 = MatSub(M1, M0)
  s0 = SAdd(s0, s3)
  s1 = Sigmoid(s0)
  M3 = MatScale(s1, M0)
  M1 = MatScale(s3, M2)
  M0 = MatAdd(M1, M3)

structure: gated delta rule  [a=1.123 b=0.810 c=-0.810 g=0.002, erase c/a=0.721, R²=0.9990, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.969  margin 0.311  ±0.003
test d16 T12 ow0.0: acc 0.954  margin 0.283  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.305  ±0.004
test d32 T24 ow0.3: acc 0.949  margin 0.325  ±0.003
test d8 T6 ow0.3: acc 0.846  margin 0.142  ±0.008
test d16 T64 K8 ow0.3: acc 0.042  margin -0.587  ±0.004
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

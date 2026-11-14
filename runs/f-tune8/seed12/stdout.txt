# Search seed 12

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500068  real evaluations (after cache): 559882  time: 280s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 8

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* linear attention: 35540 candidates
* decayed linear attention: 56324 candidates
* gated delta rule: 1269540 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 35540 candidates
- delta rule (beta=1) (acc 0.858): 1269540 candidates
- delta rule (beta=0.5) (acc 0.932): 1269540 candidates
- gated delta (alpha=0.9) (acc 0.729): 35540 candidates

## Best rule

```
S' = 1.117·((S + (v)⊗(k)) - (σ(1.037·|S·<k, tanh(k)>·k|)·S·<k, tanh(k)>·k)⊗(<k, tanh(k)>·k))

Effective program (15 instructions):
  M1 = Outer(V1, V0)
  M1 = MatAdd(M0, M1)
  s3 = 1.0366
  V1 = Tanh(V0)
  s0 = Dot(V0, V1)
  V3 = VecScale(s0, V0)
  V1 = MatVec(M0, V3)
  s2 = Norm(V1)
  s3 = SMul(s3, s2)
  s3 = Sigmoid(s3)
  V0 = VecScale(s3, V1)
  M3 = Outer(V0, V3)
  M1 = MatSub(M1, M3)
  s3 = 1.1171
  M0 = MatScale(s3, M1)

structure: gated delta rule  [a=1.117 b=1.117 c=-0.797 g=0.019, erase c/a=0.713, R²=0.9967, 384 steps]

train acc 0.972 ±0.006
test d16 T12 ow0.3: acc 0.970  margin 0.312  ±0.003
test d16 T12 ow0.0: acc 0.955  margin 0.282  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.310  ±0.004
test d32 T24 ow0.3: acc 0.974  margin 0.367  ±0.002
test d8 T6 ow0.3: acc 0.843  margin 0.140  ±0.008
test d16 T64 K8 ow0.3: acc 0.105  margin -0.484  ±0.007
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

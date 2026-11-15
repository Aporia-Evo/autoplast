# Search seed 16

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1012274  time: 921s  pop: 500  tournament: 10

commit: 1d58ceb+cachefix  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4212 candidates
* linear, not error-correcting: 4852 candidates
* unclassified: 6772 candidates
* linear attention: 17268 candidates
* gated delta rule: 38772 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 18548 candidates
- delta rule (beta=1) (acc 0.858): 39284 candidates
- delta rule (beta=0.5) (acc 0.932): 39284 candidates
- gated delta (alpha=0.9) (acc 0.729): 13172 candidates

## Best rule

```
S' = ((-1.438 + σ(σ(0)))·-0.371·(0 + S) + (-1.438 + σ(σ(0)))·((((0 + S)·k + (0 - ((v + v) + v))))⊗(k) - (0 + S)))

Effective program (17 instructions):
  V3 = VecAdd(V1, V1)
  V4 = VecAdd(V3, V1)
  V2 = VecSub(V2, V4)
  M1 = MatAdd(M1, M0)
  s0 = -0.3711
  V5 = MatVec(M1, V0)
  V3 = VecAdd(V5, V2)
  M2 = Outer(V3, V0)
  s2 = -1.4377
  M0 = MatSub(M2, M1)
  s3 = Sigmoid(s1)
  s1 = Sigmoid(s3)
  s2 = SAdd(s2, s1)
  M3 = MatScale(s2, M0)
  s3 = SMul(s2, s0)
  M0 = MatScale(s3, M1)
  M0 = MatAdd(M0, M3)

structure: gated delta rule  [a=1.118 b=2.446 c=-0.815 g=-0.000, erase c/a=0.729, R²=1.0000, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.312  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.284  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.309  ±0.004
test d32 T24 ow0.3: acc 0.956  margin 0.332  ±0.003
test d8 T6 ow0.3: acc 0.844  margin 0.143  ±0.008
test d16 T64 K8 ow0.3: acc 0.050  margin -0.570  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

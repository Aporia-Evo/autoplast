# Search seed 5

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 917400  time: 589s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 2420 candidates
* linear attention: 25844 candidates
* delta rule: 41076 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 25844 candidates
- delta rule (beta=1) (acc 0.858): 29556 candidates
- delta rule (beta=0.5) (acc 0.932): 41076 candidates
- gated delta (alpha=0.9) (acc 0.729): 25844 candidates

## Best rule

```
S' = (((norm(σ(0)·(v + S·(0 + tanh(k)))) - S·(0 + tanh(k))))⊗((0 + tanh(k))) + ((((v)⊗(tanh(tanh(k))) - 0) + S) + ((v)⊗(tanh(tanh(k))) - 0)))

Effective program (15 instructions):
  V3 = Tanh(V0)
  V4 = VecAdd(V4, V3)
  V2 = MatVec(M0, V4)
  V5 = Tanh(V3)
  M3 = Outer(V1, V5)
  s3 = Sigmoid(s0)
  V5 = VecAdd(V1, V2)
  M3 = MatSub(M3, M1)
  V1 = VecScale(s3, V5)
  V0 = Normalize(V1)
  V1 = VecSub(V0, V2)
  M2 = Outer(V1, V4)
  M1 = MatAdd(M3, M0)
  M1 = MatAdd(M1, M3)
  M0 = MatAdd(M2, M1)

structure: unclassified  [a=1.000 b=2.403 c=-0.497 g=-0.077, erase c/a=0.497, R²=0.9839, 384 steps]

train acc 0.945 ±0.008
test d16 T12 ow0.3: acc 0.936  margin 0.268  ±0.004
test d16 T12 ow0.0: acc 0.931  margin 0.245  ±0.003
test d16 T12 ow0.6: acc 0.946  margin 0.270  ±0.004
test d32 T24 ow0.3: acc 0.989  margin 0.361  ±0.002
test d8 T6 ow0.3: acc 0.779  margin 0.105  ±0.009
test d16 T64 K8 ow0.3: acc 0.847  margin 0.179  ±0.008
test d16 T128 K8 ow0.3: acc 0.841  margin 0.173  ±0.011
```

# Search seed 2

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 966385  time: 553s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3316 candidates
* unclassified: 4084 candidates
* linear attention: 13812 candidates
* delta rule: 39412 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 14196 candidates
- delta rule (beta=1) (acc 0.858): 39412 candidates
- delta rule (beta=0.5) (acc 0.932): 90100 candidates
- gated delta (alpha=0.9) (acc 0.729): 13812 candidates

## Best rule

```
S' = (((norm(v) + (0 + (σ(|S·k|) + 0))·(0 - S)·σ(|S·k|)·k))⊗(tanh((0 + k))) - (0 - S))

Effective program (15 instructions):
  V5 = MatVec(M0, V0)
  s3 = Norm(V5)
  s2 = Sigmoid(s3)
  s3 = SAdd(s2, s0)
  M2 = MatSub(M3, M0)
  V3 = Normalize(V1)
  s0 = SAdd(s1, s3)
  V1 = VecAdd(V2, V0)
  V5 = VecScale(s2, V0)
  V4 = MatVec(M2, V5)
  V4 = VecScale(s0, V4)
  V3 = VecAdd(V3, V4)
  V0 = Tanh(V1)
  M0 = Outer(V3, V0)
  M0 = MatSub(M0, M2)

structure: delta rule  [a=1.000 b=0.951 c=-0.474 g=0.003, erase c/a=0.474, R²=0.9970, 384 steps]

train acc 0.941 ±0.008
test d16 T12 ow0.3: acc 0.934  margin 0.262  ±0.004
test d16 T12 ow0.0: acc 0.913  margin 0.237  ±0.004
test d16 T12 ow0.6: acc 0.947  margin 0.268  ±0.004
test d32 T24 ow0.3: acc 0.989  margin 0.352  ±0.002
test d8 T6 ow0.3: acc 0.791  margin 0.110  ±0.008
test d16 T64 K8 ow0.3: acc 0.849  margin 0.174  ±0.008
test d16 T128 K8 ow0.3: acc 0.839  margin 0.168  ±0.011
```

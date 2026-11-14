# Search seed 25

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 928808  time: 897s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1780 candidates
* decayed linear attention: 2932 candidates
* linear attention: 78068 candidates
* delta rule: 150004 candidates
* gated delta rule: 160884 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 78068 candidates
- delta rule (beta=1) (acc 0.858): 150004 candidates
- delta rule (beta=0.5) (acc 0.932): 150004 candidates
- gated delta (alpha=0.9) (acc 0.729): 78068 candidates

## Best rule

```
S' = (((1.101·(S + σ(σ(1.101))·((v - S·k))⊗(tanh(k))) - (tanh(k))⊗(0)) + S) - S)

Effective program (14 instructions):
  V5 = MatVec(M0, V0)
  s3 = 1.1005
  V4 = Tanh(V0)
  V1 = VecSub(V1, V5)
  s2 = Sigmoid(s3)
  s0 = Sigmoid(s2)
  M3 = Outer(V1, V4)
  M1 = MatScale(s0, M3)
  M3 = MatAdd(M0, M1)
  M1 = Outer(V4, V3)
  M3 = MatScale(s3, M3)
  M2 = MatSub(M3, M1)
  M1 = MatAdd(M2, M0)
  M0 = MatSub(M1, M0)

structure: gated delta rule  [a=1.101 b=0.711 c=-0.711 g=0.002, erase c/a=0.646, R²=0.9990, 384 steps]

train acc 0.970 ±0.006
test d16 T12 ow0.3: acc 0.967  margin 0.301  ±0.003
test d16 T12 ow0.0: acc 0.957  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.961  margin 0.289  ±0.004
test d32 T24 ow0.3: acc 0.961  margin 0.338  ±0.003
test d8 T6 ow0.3: acc 0.838  margin 0.136  ±0.008
test d16 T64 K8 ow0.3: acc 0.062  margin -0.519  ±0.005
test d16 T128 K8 ow0.3: acc 0.018  margin -0.640  ±0.004
```

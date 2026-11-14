# Search seed 31

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 719015  time: 820s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 6388 candidates
* decayed linear attention: 10484 candidates
* linear, not error-correcting: 11764 candidates
* linear attention: 31220 candidates
* delta rule: 206580 candidates
* gated delta rule: 209396 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 31220 candidates
- delta rule (beta=1) (acc 0.858): 205684 candidates
- delta rule (beta=0.5) (acc 0.932): 207348 candidates
- gated delta (alpha=0.9) (acc 0.729): 31220 candidates

## Best rule

```
S' = 1.092·(((tanh(v))⊗(k) - (0 - S)) - σ(σ(0))·(((tanh(v))⊗(k) - (0 - S)))((norm(tanh(k)))⊗(k)))

Effective program (14 instructions):
  M0 = MatSub(M1, M0)
  V2 = Tanh(V1)
  M2 = Outer(V2, V0)
  M0 = MatSub(M2, M0)
  s0 = Sigmoid(s3)
  V3 = Tanh(V0)
  V2 = Normalize(V3)
  M1 = Outer(V2, V0)
  M3 = MatMul(M0, M1)
  s0 = Sigmoid(s0)
  M3 = MatScale(s0, M3)
  M1 = MatSub(M0, M3)
  s0 = 1.0919
  M0 = MatScale(s0, M1)

structure: gated delta rule  [a=1.092 b=0.392 c=-0.680 g=0.005, erase c/a=0.622, R²=0.9990, 384 steps]

train acc 0.972 ±0.006
test d16 T12 ow0.3: acc 0.966  margin 0.297  ±0.003
test d16 T12 ow0.0: acc 0.957  margin 0.278  ±0.003
test d16 T12 ow0.6: acc 0.961  margin 0.284  ±0.004
test d32 T24 ow0.3: acc 0.962  margin 0.337  ±0.003
test d8 T6 ow0.3: acc 0.833  margin 0.135  ±0.008
test d16 T64 K8 ow0.3: acc 0.076  margin -0.477  ±0.006
test d16 T128 K8 ow0.3: acc 0.018  margin -0.630  ±0.004
```

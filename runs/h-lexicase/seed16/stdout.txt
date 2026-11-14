# Search seed 16

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 923864  time: 388s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1140 candidates
* linear, not error-correcting: 2164 candidates
* unclassified: 4084 candidates
* linear attention: 4468 candidates
* delta rule: 70004 candidates
* gated delta rule: 76020 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 4468 candidates
- delta rule (beta=1) (acc 0.858): 70388 candidates
- delta rule (beta=0.5) (acc 0.932): 76532 candidates
- gated delta (alpha=0.9) (acc 0.729): 4468 candidates

## Best rule

```
S' = (|k| + (0.061·(<(((0 - S)·k + (0 - S)·k) + k), (0 - S)·k> + σ(σ(<(((0 - S)·k + (0 - S)·k) + k), (0 - S)·k>))) + 0.061))·(((v + (0 - S)·k))⊗(σ(σ(<(((0 - S)·k + (0 - S)·k) + k), (0 - S)·k>))·k) - (0 - S))

Effective program (18 instructions):
  M1 = MatSub(M3, M0)
  V5 = MatVec(M1, V0)
  s0 = 0.0606
  V1 = VecAdd(V1, V5)
  V4 = VecAdd(V5, V5)
  V4 = VecAdd(V4, V0)
  s1 = Dot(V4, V5)
  s2 = Sigmoid(s1)
  s3 = Sigmoid(s2)
  V2 = VecScale(s3, V0)
  s3 = SAdd(s1, s3)
  s1 = Norm(V0)
  M0 = Outer(V1, V2)
  M0 = MatSub(M0, M1)
  s3 = SMul(s0, s3)
  s2 = SAdd(s3, s0)
  s0 = SAdd(s1, s2)
  M0 = MatScale(s0, M0)

structure: unclassified  [a=1.211 b=0.777 c=-0.830 g=-0.054, erase c/a=0.685, R²=0.9385, 384 steps]

train acc 0.982 ±0.005
test d16 T12 ow0.3: acc 0.974  margin 0.307  ±0.002
test d16 T12 ow0.0: acc 0.955  margin 0.283  ±0.003
test d16 T12 ow0.6: acc 0.952  margin 0.285  ±0.004
test d32 T24 ow0.3: acc 0.000  margin 0.000  ±0.000
test d8 T6 ow0.3: acc 0.849  margin 0.142  ±0.007
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

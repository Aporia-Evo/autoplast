# Search seed 6

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 506183  time: 222s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1012 candidates
* linear, not error-correcting: 1268 candidates
* unclassified: 2676 candidates
* linear attention: 14196 candidates
* delta rule: 16756 candidates
* gated delta rule: 92532 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 14196 candidates
- delta rule (beta=1) (acc 0.858): 16756 candidates
- delta rule (beta=0.5) (acc 0.932): 18676 candidates
- gated delta (alpha=0.9) (acc 0.729): 14196 candidates

## Best rule

```
S' = (1.125·S - (0.672·(1.125·S·k - tanh(v)))⊗(k))

Effective program (9 instructions):
  s3 = 1.1248
  V3 = Tanh(V1)
  M3 = MatScale(s3, M0)
  V4 = MatVec(M3, V0)
  V4 = VecSub(V4, V3)
  s0 = 0.6718
  V3 = VecScale(s0, V4)
  M0 = Outer(V3, V0)
  M0 = MatSub(M3, M0)

structure: gated delta rule  [a=1.125 b=0.639 c=-0.756 g=0.003, erase c/a=0.672, R²=0.9993, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.970  margin 0.302  ±0.003
test d16 T12 ow0.0: acc 0.960  margin 0.281  ±0.003
test d16 T12 ow0.6: acc 0.959  margin 0.289  ±0.004
test d32 T24 ow0.3: acc 0.907  margin 0.291  ±0.004
test d8 T6 ow0.3: acc 0.841  margin 0.143  ±0.008
test d16 T64 K8 ow0.3: acc 0.034  margin -0.606  ±0.004
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

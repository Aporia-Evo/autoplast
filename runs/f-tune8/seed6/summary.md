# Search seed 6

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500092  real evaluations (after cache): 907633  time: 490s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 8

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1012 candidates
* linear, not error-correcting: 1268 candidates
* unclassified: 2676 candidates
* linear attention: 62812 candidates
* delta rule: 220212 candidates
* gated delta rule: 221140 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 62812 candidates
- delta rule (beta=1) (acc 0.858): 220212 candidates
- delta rule (beta=0.5) (acc 0.932): 221140 candidates
- gated delta (alpha=0.9) (acc 0.729): 62812 candidates

## Best rule

```
S' = ((tanh((0.664·v - S·k)))⊗(tanh(tanh(tanh(k)))) - 1.118·(0 - S))

Effective program (13 instructions):
  s1 = 0.6644
  V5 = MatVec(M0, V0)
  V0 = Tanh(V0)
  V0 = Tanh(V0)
  M1 = MatSub(M3, M0)
  s3 = 1.1176
  M1 = MatScale(s3, M1)
  V1 = VecScale(s1, V1)
  V3 = VecSub(V1, V5)
  V3 = Tanh(V3)
  V4 = Tanh(V0)
  M0 = Outer(V3, V4)
  M0 = MatSub(M0, M1)

structure: gated delta rule  [a=1.118 b=0.562 c=-0.834 g=0.044, erase c/a=0.746, R²=0.9930, 384 steps]

train acc 0.972 ±0.006
test d16 T12 ow0.3: acc 0.966  margin 0.312  ±0.003
test d16 T12 ow0.0: acc 0.948  margin 0.281  ±0.003
test d16 T12 ow0.6: acc 0.962  margin 0.308  ±0.004
test d32 T24 ow0.3: acc 0.949  margin 0.338  ±0.003
test d8 T6 ow0.3: acc 0.832  margin 0.138  ±0.008
test d16 T64 K8 ow0.3: acc 0.031  margin -0.610  ±0.004
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

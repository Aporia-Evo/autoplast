# Search seed 5

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 505417  time: 302s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1140 candidates
* decayed linear attention: 22900 candidates
* linear attention: 23284 candidates
* delta rule: 985716 candidates
* linear, not error-correcting: 1012596 candidates
* gated delta rule: 1165172 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 23284 candidates
- delta rule (beta=1) (acc 0.858): 1009652 candidates
- delta rule (beta=0.5) (acc 0.932): 1016948 candidates
- gated delta (alpha=0.9) (acc 0.729): 23284 candidates

## Best rule

```
S' = ((|tanh(v)|·0.896·(v - S·k))⊗(tanh(tanh(k))) + 1.109·S)

Effective program (13 instructions):
  s1 = 0.8957
  V3 = Tanh(V0)
  s0 = 1.1094
  V4 = MatVec(M0, V0)
  V2 = VecSub(V1, V4)
  V2 = VecScale(s1, V2)
  V5 = Tanh(V3)
  V3 = Tanh(V1)
  s1 = Norm(V3)
  V2 = VecScale(s1, V2)
  M3 = Outer(V2, V5)
  M0 = MatScale(s0, M0)
  M0 = MatAdd(M3, M0)

structure: gated delta rule  [a=1.109 b=0.776 c=-0.777 g=0.010, erase c/a=0.700, R²=0.9967, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.969  margin 0.308  ±0.003
test d16 T12 ow0.0: acc 0.953  margin 0.281  ±0.003
test d16 T12 ow0.6: acc 0.962  margin 0.302  ±0.004
test d32 T24 ow0.3: acc 0.969  margin 0.352  ±0.003
test d8 T6 ow0.3: acc 0.832  margin 0.136  ±0.008
test d16 T64 K8 ow0.3: acc 0.054  margin -0.545  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

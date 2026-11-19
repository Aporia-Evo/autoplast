# Search seed 23

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 657401  time: 571s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 884 candidates
* linear, not error-correcting: 2548 candidates
* unclassified: 3188 candidates
* delta rule: 15988 candidates
* gated delta rule: 33908 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 15988 candidates
- delta rule (beta=1) (acc 0.858): 15988 candidates
- delta rule (beta=0.5) (acc 0.932): 17652 candidates
- gated delta (alpha=0.9) (acc 0.729): 15988 candidates

## Best rule

```
S' = (((tanh(v) + (0 - S)·tanh(tanh(k))))⊗(tanh(tanh(tanh(k)))) + 0.558·(S - (0 - S)))

Effective program (12 instructions):
  M3 = MatSub(M3, M0)
  V4 = Tanh(V0)
  V1 = Tanh(V1)
  V0 = Tanh(V4)
  V3 = MatVec(M3, V0)
  M0 = MatSub(M0, M3)
  s1 = 0.5584
  V1 = VecAdd(V1, V3)
  V3 = Tanh(V0)
  M1 = Outer(V1, V3)
  M3 = MatScale(s1, M0)
  M0 = MatAdd(M1, M3)

structure: gated delta rule  [a=1.116 b=0.834 c=-0.800 g=0.016, erase c/a=0.716, R²=0.9925, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.967  margin 0.309  ±0.003
test d16 T12 ow0.0: acc 0.950  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.962  margin 0.302  ±0.004
test d32 T24 ow0.3: acc 0.967  margin 0.352  ±0.003
test d8 T6 ow0.3: acc 0.829  margin 0.133  ±0.008
test d16 T64 K8 ow0.3: acc 0.041  margin -0.576  ±0.004
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

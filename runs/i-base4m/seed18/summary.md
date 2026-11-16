# Search seed 18

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 987625  time: 508s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1012 candidates
* decayed linear attention: 2036 candidates
* linear, not error-correcting: 2676 candidates
* linear attention: 21620 candidates
* delta rule: 3785972 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 21748 candidates
- delta rule (beta=1) (acc 0.858): 3786996 candidates
- delta rule (beta=0.5) (acc 0.932): 3788532 candidates
- gated delta (alpha=0.9) (acc 0.729): 21620 candidates

## Best rule

```
S' = ((S + (tanh(v))⊗(0.223·norm((k + S·k)))) - ((S + (tanh(v))⊗(0.223·norm((k + S·k)))))(((norm((k + S·k)) + (0.223·norm((k + S·k)) + norm((k + S·k)))))⊗(0.223·norm((k + S·k)))))

Effective program (13 instructions):
  s1 = 0.2233
  V5 = MatVec(M0, V0)
  V2 = VecAdd(V0, V5)
  V4 = Normalize(V2)
  V2 = VecScale(s1, V4)
  V0 = VecAdd(V2, V4)
  V3 = VecAdd(V4, V0)
  V4 = Tanh(V1)
  M2 = Outer(V4, V2)
  M1 = MatAdd(M0, M2)
  M2 = Outer(V3, V2)
  M3 = MatMul(M1, M2)
  M0 = MatSub(M1, M3)

structure: delta rule  [a=1.000 b=0.107 c=-0.493 g=0.007, erase c/a=0.493, R²=0.9932, 384 steps]

train acc 0.938 ±0.008
test d16 T12 ow0.3: acc 0.921  margin 0.259  ±0.004
test d16 T12 ow0.0: acc 0.900  margin 0.236  ±0.004
test d16 T12 ow0.6: acc 0.939  margin 0.259  ±0.005
test d32 T24 ow0.3: acc 0.985  margin 0.347  ±0.002
test d8 T6 ow0.3: acc 0.786  margin 0.110  ±0.009
test d16 T64 K8 ow0.3: acc 0.814  margin 0.147  ±0.009
test d16 T128 K8 ow0.3: acc 0.806  margin 0.132  ±0.012
```

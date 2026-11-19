# Search seed 14

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 337342  time: 244s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1012 candidates
* linear, not error-correcting: 2036 candidates
* linear attention: 88052 candidates
* delta rule: 1499380 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 88052 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 88052 candidates

## Best rule

```
S' = ((v)⊗(k) - 0.958·((S·k)⊗(k) - S))

Effective program (7 instructions):
  V2 = MatVec(M0, V0)
  M3 = Outer(V2, V0)
  M1 = MatSub(M3, M0)
  s0 = 0.9577
  M0 = Outer(V1, V0)
  M2 = MatScale(s0, M1)
  M0 = MatSub(M0, M2)

structure: delta rule  [a=0.958 b=1.000 c=-0.958 g=-0.000, erase c/a=1.000, R²=1.0000, 384 steps]

train acc 0.825 ±0.013
test d16 T12 ow0.3: acc 0.808  margin 0.211  ±0.006
test d16 T12 ow0.0: acc 0.722  margin 0.136  ±0.006
test d16 T12 ow0.6: acc 0.888  margin 0.281  ±0.006
test d32 T24 ow0.3: acc 0.834  margin 0.263  ±0.006
test d8 T6 ow0.3: acc 0.719  margin 0.071  ±0.009
test d16 T64 K8 ow0.3: acc 0.775  margin 0.182  ±0.009
test d16 T128 K8 ow0.3: acc 0.780  margin 0.177  ±0.013
```

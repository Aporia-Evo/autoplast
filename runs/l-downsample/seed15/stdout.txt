# Search seed 15

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 554587  time: 415s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1140 candidates
* decayed linear attention: 2932 candidates
* linear, not error-correcting: 3188 candidates
* linear attention: 11636 candidates
* delta rule: 148852 candidates
* gated delta rule: 258036 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 11380 candidates
- delta rule (beta=1) (acc 0.858): 147572 candidates
- delta rule (beta=0.5) (acc 0.932): 148852 candidates
- gated delta (alpha=0.9) (acc 0.729): 11380 candidates

## Best rule

```
S' = 1.109·((S + ((tanh(v) - S·0.377·tanh(k)))⊗(tanh(k))) + ((tanh(v) - S·0.377·tanh(k)))⊗(tanh(k)))

Effective program (11 instructions):
  V0 = Tanh(V0)
  s2 = 0.3770
  V2 = VecScale(s2, V0)
  V3 = Tanh(V1)
  V4 = MatVec(M0, V2)
  V2 = VecSub(V3, V4)
  M3 = Outer(V2, V0)
  M2 = MatAdd(M0, M3)
  M0 = MatAdd(M2, M3)
  s2 = 1.1092
  M0 = MatScale(s2, M0)

structure: gated delta rule  [a=1.109 b=2.007 c=-0.757 g=0.009, erase c/a=0.682, R²=0.9980, 384 steps]

train acc 0.973 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.306  ±0.003
test d16 T12 ow0.0: acc 0.954  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.296  ±0.004
test d32 T24 ow0.3: acc 0.963  margin 0.342  ±0.003
test d8 T6 ow0.3: acc 0.833  margin 0.137  ±0.008
test d16 T64 K8 ow0.3: acc 0.053  margin -0.552  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

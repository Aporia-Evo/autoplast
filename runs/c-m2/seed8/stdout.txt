# Search seed 8

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 473505  time: 1211s  pop: 500  tournament: 10

commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1140 candidates
* decayed linear attention: 2548 candidates
* linear attention: 3060 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3060 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((v)⊗(tanh(tanh(tanh(k)))) - 0.869·(0 - S))
P1' = (v)⊗(tanh(tanh(tanh(k))))

Effective program (8 instructions):
  M2 = MatSub(M2, M0)
  V3 = Tanh(V0)
  s0 = 0.8692
  M2 = MatScale(s0, M2)
  V3 = Tanh(V3)
  V0 = Tanh(V3)
  M1 = Outer(V1, V0)
  M0 = MatSub(M1, M2)

structure: decayed linear attention  [a=0.869 b=0.864 c=-0.000 g=0.003, erase c/a=0.000, R²=0.9918, 1408 steps]

train acc 0.510 ±0.014
test regime collision3: acc 0.514  margin -0.047  ±0.006
test d16 T12 ow0.3: acc 0.727  margin 0.122  ±0.007
test d16 T12 ow0.0: acc 0.700  margin 0.101  ±0.006
test d16 T12 ow0.6: acc 0.726  margin 0.112  ±0.009
test d32 T24 ow0.3: acc 0.616  margin 0.081  ±0.007
test d8 T6 ow0.3: acc 0.636  margin 0.031  ±0.010
test d16 T64 K8 ow0.3: acc 0.580  margin -0.013  ±0.011
test d16 T128 K8 ow0.3: acc 0.547  margin -0.033  ±0.016
```

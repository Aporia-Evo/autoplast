# Search seed 11

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 326634  time: 745s  pop: 500  tournament: 10

commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1908 candidates
* unclassified: 14196 candidates
* gated delta rule: 1452148 candidates
* delta rule: 1453300 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 14452 candidates
- delta rule (beta=1) (acc 0.578): 1453300 candidates
- delta rule (beta=0.5) (acc 0.617): 1454068 candidates
- gated delta (alpha=0.9) (acc 0.519): 1452148 candidates

## Best rule

```
S' = (((tanh(v) - P1·tanh(k)))⊗(tanh(tanh(k))) + S)
P1' = σ(σ(0))·(((tanh(v) - P1·tanh(k)))⊗(tanh(tanh(k))) + S)

Effective program (10 instructions):
  V3 = Tanh(V0)
  V0 = Tanh(V3)
  V4 = MatVec(M1, V3)
  V5 = Tanh(V1)
  V1 = VecSub(V5, V4)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M1, M0)
  s2 = Sigmoid(s3)
  s1 = Sigmoid(s2)
  M1 = MatScale(s1, M0)

structure: delta rule  [a=1.000 b=0.856 c=-0.531 g=0.002, erase c/a=0.531, R²=0.9944, 1408 steps]

train acc 0.619 ±0.014
test regime collision3: acc 0.637  margin 0.046  ±0.006
test d16 T12 ow0.3: acc 0.924  margin 0.266  ±0.004
test d16 T12 ow0.0: acc 0.892  margin 0.234  ±0.004
test d16 T12 ow0.6: acc 0.943  margin 0.273  ±0.004
test d32 T24 ow0.3: acc 0.985  margin 0.358  ±0.002
test d8 T6 ow0.3: acc 0.786  margin 0.108  ±0.009
test d16 T64 K8 ow0.3: acc 0.850  margin 0.176  ±0.008
test d16 T128 K8 ow0.3: acc 0.840  margin 0.168  ±0.011
```

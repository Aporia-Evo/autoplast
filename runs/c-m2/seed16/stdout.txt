# Search seed 16

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 607646  time: 1621s  pop: 500  tournament: 10

commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4212 candidates
* unclassified: 8052 candidates
* linear attention: 9076 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 9076 candidates
- delta rule (beta=1) (acc 0.578): 425716 candidates
- delta rule (beta=0.5) (acc 0.617): 426868 candidates
- gated delta (alpha=0.9) (acc 0.519): 409716 candidates

## Best rule

```
S' = ((v)⊗((tanh(k) + tanh(k))) - (P1 - S))
P1' = -0.184·((P1 - S)·tanh((tanh(k) + tanh(k))))⊗(tanh((tanh(k) + tanh(k))))

Effective program (10 instructions):
  V4 = Tanh(V0)
  V0 = VecAdd(V4, V4)
  M3 = MatSub(M1, M0)
  V4 = Tanh(V0)
  s1 = -0.1845
  M0 = Outer(V1, V0)
  M0 = MatSub(M0, M3)
  V1 = MatVec(M3, V4)
  M2 = Outer(V1, V4)
  M1 = MatScale(s1, M2)

structure: unclassified  [a=0.938 b=1.891 c=-0.028 g=0.000, erase c/a=0.030, R²=0.8324, 1408 steps]

train acc 0.621 ±0.014
test regime collision3: acc 0.630  margin 0.037  ±0.006
test d16 T12 ow0.3: acc 0.911  margin 0.243  ±0.004
test d16 T12 ow0.0: acc 0.907  margin 0.230  ±0.004
test d16 T12 ow0.6: acc 0.880  margin 0.220  ±0.006
test d32 T24 ow0.3: acc 0.978  margin 0.348  ±0.002
test d8 T6 ow0.3: acc 0.722  margin 0.078  ±0.009
test d16 T64 K8 ow0.3: acc 0.772  margin 0.123  ±0.009
test d16 T128 K8 ow0.3: acc 0.749  margin 0.106  ±0.014
```

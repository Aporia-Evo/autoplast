# Search seed 8

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 569150  time: 1042s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3828 candidates
* decayed linear attention: 4596 candidates
* linear attention: 462964 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 462196 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((v)⊗(tanh((tanh(k) + k))) - (-1.862·S + S))
P2' = -1.862·S

Effective program (8 instructions):
  s2 = -1.8623
  M2 = MatScale(s2, M0)
  M3 = MatAdd(M2, M0)
  V3 = Tanh(V0)
  V2 = VecAdd(V3, V0)
  V3 = Tanh(V2)
  M0 = Outer(V1, V3)
  M0 = MatSub(M0, M3)

structure: unclassified  [a=0.862 b=1.628 c=-0.000 g=0.004, erase c/a=0.000, R²=0.9846, 1408 steps]

train acc 0.510 ±0.014
test regime collision3: acc 0.509  margin -0.051  ±0.006
test d16 T12 ow0.3: acc 0.717  margin 0.116  ±0.007
test d16 T12 ow0.0: acc 0.686  margin 0.089  ±0.006
test d16 T12 ow0.6: acc 0.722  margin 0.113  ±0.009
test d32 T24 ow0.3: acc 0.597  margin 0.065  ±0.007
test d8 T6 ow0.3: acc 0.630  margin 0.029  ±0.010
test d16 T64 K8 ow0.3: acc 0.574  margin -0.017  ±0.011
test d16 T128 K8 ow0.3: acc 0.543  margin -0.037  ±0.016
```

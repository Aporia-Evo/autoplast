# Search seed 3

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 723988  time: 1255s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1524 candidates
* decayed linear attention: 2548 candidates
* gated delta rule: 133748 candidates
* delta rule: 135796 candidates
* delta + Kronecker mix: 181364 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5236 candidates
- delta rule (beta=1) (acc 0.578): 135796 candidates
- delta rule (beta=0.5) (acc 0.617): 137076 candidates
- gated delta (alpha=0.9) (acc 0.519): 133748 candidates

## Best rule

```
S' = (S + 0.379·(((((v + v) - (P2 + S)·k) + v))⊗(k) + P2))
P1' = ((((v + v) - (P2 + S)·k) + v))⊗(k)
P2' = 0.379·(((((v + v) - (P2 + S)·k) + v))⊗(k) + P2)

Effective program (10 instructions):
  M3 = MatAdd(M2, M0)
  V5 = MatVec(M3, V0)
  V4 = VecAdd(V1, V1)
  V2 = VecSub(V4, V5)
  s0 = 0.3790
  V2 = VecAdd(V2, V1)
  M1 = Outer(V2, V0)
  M3 = MatAdd(M1, M2)
  M2 = MatScale(s0, M3)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=1.023 b=1.137 c=-0.402 g=0.000, erase c/a=0.393, R²=0.8583, 1408 steps]

train acc 0.654 ±0.014
test regime collision3: acc 0.659  margin 0.059  ±0.006
test d16 T12 ow0.3: acc 0.934  margin 0.268  ±0.004
test d16 T12 ow0.0: acc 0.902  margin 0.238  ±0.004
test d16 T12 ow0.6: acc 0.932  margin 0.264  ±0.005
test d32 T24 ow0.3: acc 0.982  margin 0.358  ±0.002
test d8 T6 ow0.3: acc 0.808  margin 0.119  ±0.008
test d16 T64 K8 ow0.3: acc 0.841  margin 0.176  ±0.008
test d16 T128 K8 ow0.3: acc 0.847  margin 0.171  ±0.011
```

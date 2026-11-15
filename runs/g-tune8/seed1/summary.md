# Search seed 1

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500036  real evaluations (after cache): 852910  time: 2793s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 5364 candidates
* linear, not error-correcting: 8956 candidates
* linear attention: 51252 candidates
* decayed linear attention: 73036 candidates
* delta rule: 753820 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 50484 candidates
- delta rule (beta=1) (acc 0.578): 741020 candidates
- delta rule (beta=0.5) (acc 0.617): 741956 candidates
- gated delta (alpha=0.9) (acc 0.519): 740484 candidates

## Best rule

```
S' = (1.004·((tanh(v))⊗(k) - (0 - S)) - (1.004·((tanh(v))⊗(k) - (0 - S)))(0.596·(tanh(tanh(k)))⊗(tanh(tanh(k)))))
P1' = (0 - S)
P2' = (1.004·((tanh(v))⊗(k) - (0 - S)))(0.596·(tanh(tanh(k)))⊗(tanh(tanh(k))))

Effective program (13 instructions):
  M1 = MatSub(M3, M0)
  V1 = Tanh(V1)
  V3 = Tanh(V0)
  V3 = Tanh(V3)
  M0 = Outer(V1, V0)
  s0 = 0.5962
  M2 = Outer(V3, V3)
  M2 = MatScale(s0, M2)
  s2 = 1.0036
  M0 = MatSub(M0, M1)
  M0 = MatScale(s2, M0)
  M2 = MatMul(M0, M2)
  M0 = MatSub(M0, M2)

structure: delta rule  [a=1.004 b=0.492 c=-0.481 g=0.002, erase c/a=0.479, R²=0.9930, 1408 steps]

train acc 0.624 ±0.014
test regime collision3: acc 0.641  margin 0.050  ±0.006
test d16 T12 ow0.3: acc 0.922  margin 0.261  ±0.004
test d16 T12 ow0.0: acc 0.906  margin 0.239  ±0.004
test d16 T12 ow0.6: acc 0.939  margin 0.259  ±0.005
test d32 T24 ow0.3: acc 0.987  margin 0.357  ±0.002
test d8 T6 ow0.3: acc 0.777  margin 0.105  ±0.009
test d16 T64 K8 ow0.3: acc 0.824  margin 0.147  ±0.008
test d16 T128 K8 ow0.3: acc 0.803  margin 0.131  ±0.012
```

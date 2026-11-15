# Search seed 15

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1113521  time: 3474s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 1050140 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1396 candidates
* unclassified: 3852 candidates
* linear attention: 5780 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5780 candidates
- delta rule (beta=1) (acc 0.578): 287676 candidates
- delta rule (beta=0.5) (acc 0.617): 288692 candidates
- gated delta (alpha=0.9) (acc 0.519): 59548 candidates

## Best rule

```
S' = …
P1' = 0.687·(((P2 + (tanh(tanh(v)))⊗(k)) - (((tanh(tanh(v)))⊗(k) + (tanh(tanh(v)))⊗(k)) + ((tanh(tanh(v)))⊗(k) + (tanh(tanh(v)))⊗(k))))·k)⊗(k)
P2' = (((P2 + (tanh(tanh(v)))⊗(k)) + (((tanh(tanh(v)))⊗(k) + (tanh(tanh(v)))⊗(k)) + ((tanh(tanh(v)))⊗(k) + (tanh(tanh(v)))⊗(k)))) - 0.687·(((P2 + (tanh(tanh(v)))⊗(k)) - (((tanh(tanh(v)))⊗(k) + (tanh(tanh(v)))⊗(k)) + ((tanh(tanh(v)))⊗(k) + (tanh(tanh(v)))⊗(k))))·k)⊗(k))

Effective program (17 instructions):
  V5 = Tanh(V1)
  V3 = Tanh(V5)
  M1 = Outer(V3, V0)
  M2 = MatAdd(M2, M1)
  M0 = MatAdd(M1, M1)
  s0 = 0.6866
  M0 = MatAdd(M0, M0)
  M3 = MatSub(M2, M0)
  M0 = MatAdd(M2, M0)
  V4 = MatVec(M3, V0)
  M3 = Outer(V4, V0)
  M1 = MatScale(s0, M3)
  M3 = Outer(V0, V0)
  M3 = MatMul(M0, M3)
  M3 = MatSub(M2, M3)
  M2 = MatSub(M0, M1)
  M0 = MatAdd(M3, M2)

structure: unclassified  [a=1.034 b=2.790 c=-0.867 g=0.002, erase c/a=0.839, R²=0.5177, 1408 steps]

train acc 0.675 ±0.013
test regime collision3: acc 0.684  margin 0.074  ±0.006
test d16 T12 ow0.3: acc 0.929  margin 0.284  ±0.004
test d16 T12 ow0.0: acc 0.886  margin 0.238  ±0.004
test d16 T12 ow0.6: acc 0.958  margin 0.294  ±0.004
test d32 T24 ow0.3: acc 0.982  margin 0.368  ±0.002
test d8 T6 ow0.3: acc 0.827  margin 0.134  ±0.008
test d16 T64 K8 ow0.3: acc 0.865  margin 0.207  ±0.008
test d16 T128 K8 ow0.3: acc 0.874  margin 0.206  ±0.010
```

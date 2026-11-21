# Search seed 3

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 2100084  real evaluations (after cache): 1087255  time: 8250s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* linear, not error-correcting: 1268 candidates
* decayed linear attention: 1524 candidates
* linear attention: 8564 candidates
* delta rule: 340212 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8564 candidates
- delta rule (beta=1) (acc 0.578): 335860 candidates
- delta rule (beta=0.5) (acc 0.617): 339828 candidates
- gated delta (alpha=0.9) (acc 0.519): 335348 candidates

## Best rule

```
S' = (1.009·(S + (tanh(v))⊗(k)) - 0.146·((S + (tanh(v))⊗(k)))((((k + k))⊗(tanh((k + k))) - (P2)(((k + k))⊗(tanh((k + k)))))))
P1' = (((k + k))⊗(tanh((k + k))) - (P2)(((k + k))⊗(tanh((k + k)))))
P2' = ((tanh(v))⊗(tanh(k)))((tanh(v))⊗(tanh(k)))

Effective program (17 instructions):
  V4 = VecAdd(V0, V0)
  V5 = Tanh(V4)
  M1 = Outer(V4, V5)
  M2 = MatMul(M2, M1)
  V5 = Tanh(V1)
  M1 = MatSub(M1, M2)
  M2 = Outer(V5, V0)
  M0 = MatAdd(M0, M2)
  M2 = MatMul(M0, M1)
  s0 = 0.1464
  M2 = MatScale(s0, M2)
  s2 = 1.0086
  V0 = Tanh(V0)
  M0 = MatScale(s2, M0)
  M0 = MatSub(M0, M2)
  M2 = Outer(V5, V0)
  M2 = MatMul(M2, M2)

structure: unclassified  [a=1.010 b=0.518 c=-0.479 g=-0.010, erase c/a=0.474, R²=0.9671, 1408 steps]

train acc 0.634 ±0.014
test regime collision3: acc 0.642  margin 0.051  ±0.006
test d16 T12 ow0.3: acc 0.914  margin 0.253  ±0.004
test d16 T12 ow0.0: acc 0.919  margin 0.244  ±0.003
test d16 T12 ow0.6: acc 0.922  margin 0.244  ±0.005
test d32 T24 ow0.3: acc 0.979  margin 0.352  ±0.002
test d8 T6 ow0.3: acc 0.758  margin 0.096  ±0.009
test d16 T64 K8 ow0.3: acc 0.798  margin 0.126  ±0.009
test d16 T128 K8 ow0.3: acc 0.757  margin 0.106  ±0.013
```

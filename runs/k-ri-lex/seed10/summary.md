# Search seed 10

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 944872  time: 2373s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 356123 attempts, 284531 blocks inserted, 295867 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 200052 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 628 candidates
* unclassified: 1652 candidates
* delta rule: 14324 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 2676 candidates
- delta rule (beta=1) (acc 0.578): 13684 candidates
- delta rule (beta=0.5) (acc 0.617): 14324 candidates
- gated delta (alpha=0.9) (acc 0.519): 12148 candidates

## Best rule

```
S' = ((((S + P1) + -0.848·P1) + ((((v + -0.233·S·k) + 0.146·(-0.233·S·k ⊙ k)))⊗(k) + (((v + -0.233·S·k) + 0.146·(-0.233·S·k ⊙ k)))⊗(k))) + -0.008·((S + P1) + -0.848·P1))
P1' = (((((v + -0.233·S·k) + 0.146·(-0.233·S·k ⊙ k)))⊗(k) + (((v + -0.233·S·k) + 0.146·(-0.233·S·k ⊙ k)))⊗(k)) - -0.848·P1)
P2' = -0.008·((S + P1) + -0.848·P1)

Effective program (19 instructions):
  V5 = MatVec(M0, V0)
  s1 = -0.2330
  s2 = -0.0076
  V5 = VecScale(s1, V5)
  V1 = VecAdd(V1, V5)
  M2 = MatAdd(M0, M1)
  s0 = 0.1457
  V5 = Hadamard(V5, V0)
  V2 = VecScale(s0, V5)
  V1 = VecAdd(V1, V2)
  s0 = -0.8483
  M1 = MatScale(s0, M1)
  M2 = MatAdd(M2, M1)
  M0 = Outer(V1, V0)
  M3 = MatAdd(M0, M0)
  M1 = MatSub(M3, M1)
  M0 = MatAdd(M2, M3)
  M2 = MatScale(s2, M2)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=1.029 b=2.000 c=-0.452 g=0.000, erase c/a=0.439, R²=0.9611, 1408 steps]

train acc 0.681 ±0.013
test regime collision3: acc 0.677  margin 0.071  ±0.006
test d16 T12 ow0.3: acc 0.950  margin 0.265  ±0.003
test d16 T12 ow0.0: acc 0.932  margin 0.252  ±0.003
test d16 T12 ow0.6: acc 0.939  margin 0.241  ±0.005
test d32 T24 ow0.3: acc 0.985  margin 0.361  ±0.002
test d8 T6 ow0.3: acc 0.790  margin 0.109  ±0.008
test d16 T64 K8 ow0.3: acc 0.863  margin 0.172  ±0.008
test d16 T128 K8 ow0.3: acc 0.869  margin 0.170  ±0.011
```

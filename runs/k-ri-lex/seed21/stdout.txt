# Search seed 21

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 919657  time: 2638s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 356949 attempts, 251810 blocks inserted, 275714 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 850036 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 628 candidates
* linear attention: 1140 candidates
* unclassified: 25972 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 1140 candidates
- delta rule (beta=1) (acc 0.578): 92404 candidates
- delta rule (beta=0.5) (acc 0.617): 103540 candidates
- gated delta (alpha=0.9) (acc 0.519): 22388 candidates

## Best rule

```
S' = (((S + (((P2 + P2) + -0.016·(P1)(S)) - P1)) + (((v + v))⊗(k) + 0.184·(((P2 + P2) + -0.016·(P1)(S)) - P1))) + -0.917·(((S + (((P2 + P2) + -0.016·(P1)(S)) - P1))·k - (v + v)))⊗(k))
P1' = 0.003·(((S + (((P2 + P2) + -0.016·(P1)(S)) - P1)) + (((v + v))⊗(k) + 0.184·(((P2 + P2) + -0.016·(P1)(S)) - P1))) + -0.917·(((S + (((P2 + P2) + -0.016·(P1)(S)) - P1))·k - (v + v)))⊗(k))
P2' = ((((v + v))⊗(k) + 0.184·(((P2 + P2) + -0.016·(P1)(S)) - P1)) + (((v + v))⊗(k) + 0.184·(((P2 + P2) + -0.016·(P1)(S)) - P1)))

Effective program (22 instructions):
  V1 = VecAdd(V1, V1)
  M3 = MatAdd(M2, M2)
  M2 = MatMul(M1, M0)
  s0 = -0.0156
  M2 = MatScale(s0, M2)
  M3 = MatAdd(M3, M2)
  M1 = MatSub(M3, M1)
  M2 = Outer(V1, V0)
  s0 = -0.9175
  M0 = MatAdd(M0, M1)
  s2 = 0.1842
  M1 = MatScale(s2, M1)
  M2 = MatAdd(M2, M1)
  V2 = MatVec(M0, V0)
  V1 = VecSub(V2, V1)
  s2 = 0.0030
  M1 = Outer(V1, V0)
  M1 = MatScale(s0, M1)
  M3 = MatAdd(M0, M2)
  M0 = MatAdd(M3, M1)
  M1 = MatScale(s2, M0)
  M2 = MatAdd(M2, M2)

structure: unclassified  [a=1.075 b=3.850 c=-0.964 g=-0.001, erase c/a=0.897, R²=0.7869, 1408 steps]

train acc 0.738 ±0.013
test regime collision3: acc 0.723  margin 0.110  ±0.006
test d16 T12 ow0.3: acc 0.948  margin 0.285  ±0.003
test d16 T12 ow0.0: acc 0.935  margin 0.268  ±0.003
test d16 T12 ow0.6: acc 0.940  margin 0.255  ±0.005
test d32 T24 ow0.3: acc 0.975  margin 0.367  ±0.002
test d8 T6 ow0.3: acc 0.820  margin 0.129  ±0.008
test d16 T64 K8 ow0.3: acc 0.883  margin 0.201  ±0.007
test d16 T128 K8 ow0.3: acc 0.898  margin 0.205  ±0.009
```

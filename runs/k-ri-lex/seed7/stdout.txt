# Search seed 7

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 934591  time: 5033s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357101 attempts, 226461 blocks inserted, 243489 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 850036 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* decayed linear attention: 1140 candidates
* delta rule: 209012 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 2804 candidates
- delta rule (beta=1) (acc 0.578): 209652 candidates
- delta rule (beta=0.5) (acc 0.617): 210548 candidates
- gated delta (alpha=0.9) (acc 0.519): 95348 candidates

## Best rule

```
S' = (… + ((…)((tanh(k))⊗(tanh(k))) + 0.050·((((((v + v))⊗(k) + ((v + v))⊗(k)) + (((v + v))⊗(k) + ((v + v))⊗(k))) + 0.744·P1) + -0.005·S)))
P1' = ((((((v + v))⊗(k) + ((v + v))⊗(k)) + (((v + v))⊗(k) + ((v + v))⊗(k))) + 0.744·P1) + -0.005·S)
P2' = ((…)((tanh(k))⊗(tanh(k))) + 0.050·((((((v + v))⊗(k) + ((v + v))⊗(k)) + (((v + v))⊗(k) + ((v + v))⊗(k))) + 0.744·P1) + -0.005·S))

Effective program (22 instructions):
  s2 = 0.7443
  V5 = VecAdd(V1, V1)
  M2 = MatScale(s2, M1)
  M1 = Outer(V5, V0)
  M1 = MatAdd(M1, M1)
  M3 = MatAdd(M1, M1)
  V0 = Tanh(V0)
  M1 = MatAdd(M3, M2)
  s3 = -0.0051
  M2 = MatScale(s3, M0)
  M1 = MatAdd(M1, M2)
  M2 = MatAdd(M3, M1)
  M0 = MatAdd(M0, M2)
  M0 = MatAdd(M0, M2)
  M3 = Outer(V0, V0)
  M2 = MatSub(M1, M0)
  M2 = MatMul(M2, M3)
  s0 = 0.0500
  M3 = MatScale(s0, M1)
  M2 = MatAdd(M2, M3)
  M3 = MatSub(M0, M1)
  M0 = MatAdd(M3, M2)

structure: unclassified  [a=1.075 b=2.978 c=-0.945 g=0.003, erase c/a=0.879, R²=0.7825, 1408 steps]

train acc 0.740 ±0.013
test regime collision3: acc 0.723  margin 0.114  ±0.006
test d16 T12 ow0.3: acc 0.949  margin 0.287  ±0.003
test d16 T12 ow0.0: acc 0.934  margin 0.267  ±0.003
test d16 T12 ow0.6: acc 0.947  margin 0.263  ±0.004
test d32 T24 ow0.3: acc 0.971  margin 0.366  ±0.003
test d8 T6 ow0.3: acc 0.834  margin 0.134  ±0.008
test d16 T64 K8 ow0.3: acc 0.880  margin 0.207  ±0.007
test d16 T128 K8 ow0.3: acc 0.898  margin 0.210  ±0.009
```

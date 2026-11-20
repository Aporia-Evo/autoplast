# Search seed 26

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 951774  time: 5116s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 356164 attempts, 255676 blocks inserted, 274967 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 700020 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* linear attention: 1012 candidates
* decayed linear attention: 2804 candidates
* unclassified: 7668 candidates
* gated delta rule: 135796 candidates
* delta rule: 140532 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 1012 candidates
- delta rule (beta=1) (acc 0.578): 140532 candidates
- delta rule (beta=0.5) (acc 0.617): 140532 candidates
- gated delta (alpha=0.9) (acc 0.519): 135796 candidates

## Best rule

```
S' = …
P1' = ((((S + ((P1)(P1) - P2)))((k)⊗(k)) + -0.002·((S + ((P1)(P1) - P2)))((k)⊗(k))) + ((v)⊗(k) + -0.450·((((S + ((P1)(P1) - P2)))((k)⊗(k)) + -0.002·((S + ((P1)(P1) - P2)))((k)⊗(k))) + (((S + ((P1)(P1) - P2)))((k)⊗(k)) + -0.002·((S + ((P1)(P1) - P2)))((k)⊗(k))))))
P2' = (1/(-0.450) + 1/(-0.450))·((((S + ((P1)(P1) - P2)))((k)⊗(k)) + -0.002·((S + ((P1)(P1) - P2)))((k)⊗(k))) + ((v)⊗(k) + -0.450·((((S + ((P1)(P1) - P2)))((k)⊗(k)) + -0.002·((S + ((P1)(P1) - P2)))((k)⊗(k))) + (((S + ((P1)(P1) - P2)))((k)⊗(k)) + -0.002·((S + ((P1)(P1) - P2)))((k)⊗(k))))))

Effective program (22 instructions):
  M1 = MatMul(M1, M1)
  M3 = MatSub(M1, M2)
  M0 = MatAdd(M0, M3)
  s3 = -0.4502
  M1 = Outer(V0, V0)
  M2 = MatMul(M0, M1)
  s1 = -0.0017
  M1 = MatScale(s1, M2)
  M2 = MatAdd(M2, M1)
  M3 = MatAdd(M2, M2)
  M1 = Outer(V1, V0)
  M3 = MatScale(s3, M3)
  M1 = MatAdd(M1, M3)
  M0 = MatAdd(M0, M1)
  M1 = MatAdd(M2, M1)
  M2 = Transpose(M0)
  s2 = 0.0072
  M2 = MatScale(s2, M2)
  M0 = MatAdd(M0, M2)
  s1 = Recip(s3)
  s1 = SAdd(s1, s1)
  M2 = MatScale(s1, M1)

structure: unclassified  [a=1.032 b=1.003 c=-0.925 g=0.001, erase c/a=0.896, R²=0.5129, 1408 steps]

train acc 0.682 ±0.013
test regime collision3: acc 0.690  margin 0.086  ±0.006
test d16 T12 ow0.3: acc 0.937  margin 0.274  ±0.004
test d16 T12 ow0.0: acc 0.918  margin 0.251  ±0.003
test d16 T12 ow0.6: acc 0.956  margin 0.266  ±0.004
test d32 T24 ow0.3: acc 0.988  margin 0.351  ±0.002
test d8 T6 ow0.3: acc 0.841  margin 0.138  ±0.008
test d16 T64 K8 ow0.3: acc 0.810  margin 0.136  ±0.009
test d16 T128 K8 ow0.3: acc 0.786  margin 0.125  ±0.013
```

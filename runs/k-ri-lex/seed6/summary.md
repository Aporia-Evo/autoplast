# Search seed 6

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 916666  time: 5911s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 356823 attempts, 231571 blocks inserted, 259143 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 150004 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1652 candidates
* decayed linear attention: 5876 candidates
* delta rule: 118388 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3956 candidates
- delta rule (beta=1) (acc 0.578): 118004 candidates
- delta rule (beta=0.5) (acc 0.617): 120948 candidates
- gated delta (alpha=0.9) (acc 0.519): 18932 candidates

## Best rule

```
S' = ((S + (P1 + -0.070·P2)) + ((v)⊗(k) - (σ((0 + σ(0)))·(S + (P1 + -0.070·P2)))((k)⊗(k))))
P1' = …
P2' = (((σ((0 + σ(0)))·(S + (P1 + -0.070·P2)))((k)⊗(k)) + ((σ((0 + σ(0)))·(S + (P1 + -0.070·P2)))((k)⊗(k)))((σ((0 + σ(0)))·(S + (P1 + -0.070·P2)))((k)⊗(k)))) + σ(0)·(((v)⊗(k) - (σ((0 + σ(0)))·(S + (P1 + -0.070·P2)))((k)⊗(k))))((((σ((0 + σ(0)))·(S + (P1 + -0.070·P2)))((k)⊗(k)))((σ((0 + σ(0)))·(S + (P1 + -0.070·P2)))((k)⊗(k))))ᵀ))

Effective program (20 instructions):
  M3 = Outer(V0, V0)
  s1 = Sigmoid(s0)
  s3 = SAdd(s0, s1)
  s2 = -0.0698
  M2 = MatScale(s2, M2)
  M1 = MatAdd(M1, M2)
  s0 = Sigmoid(s3)
  M0 = MatAdd(M0, M1)
  M1 = Outer(V1, V0)
  M2 = MatScale(s0, M0)
  M2 = MatMul(M2, M3)
  M1 = MatSub(M1, M2)
  M3 = MatMul(M2, M2)
  M2 = MatAdd(M2, M3)
  M3 = Transpose(M3)
  M3 = MatMul(M1, M3)
  M3 = MatScale(s1, M3)
  M2 = MatAdd(M2, M3)
  M0 = MatAdd(M0, M1)
  M1 = MatAdd(M1, M2)

structure: unclassified  [a=1.026 b=1.002 c=-0.624 g=0.001, erase c/a=0.608, R²=0.5878, 1408 steps]

train acc 0.664 ±0.014
test regime collision3: acc 0.668  margin 0.062  ±0.006
test d16 T12 ow0.3: acc 0.935  margin 0.262  ±0.004
test d16 T12 ow0.0: acc 0.914  margin 0.238  ±0.004
test d16 T12 ow0.6: acc 0.935  margin 0.257  ±0.005
test d32 T24 ow0.3: acc 0.989  margin 0.351  ±0.002
test d8 T6 ow0.3: acc 0.792  margin 0.110  ±0.008
test d16 T64 K8 ow0.3: acc 0.829  margin 0.173  ±0.008
test d16 T128 K8 ow0.3: acc 0.827  margin 0.167  ±0.012
```

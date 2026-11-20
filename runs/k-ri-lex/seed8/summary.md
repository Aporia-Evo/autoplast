# Search seed 8

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 896965  time: 4702s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357288 attempts, 263230 blocks inserted, 287510 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 350068 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* linear attention: 1652 candidates
* decayed linear attention: 3828 candidates
* unclassified: 14196 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 1652 candidates
- delta rule (beta=1) (acc 0.578): 109556 candidates
- delta rule (beta=0.5) (acc 0.617): 116596 candidates
- gated delta (alpha=0.9) (acc 0.519): 96244 candidates

## Best rule

```
S' = (((S + P1) + σ(0)·(((v)⊗(k) + (v)⊗(k)) - (((S + P1))((k)⊗(k)) + -0.010·(S + P1)))) + σ(σ(0.530))·σ(0)·(((v)⊗(k) + (v)⊗(k)) - (((S + P1))((k)⊗(k)) + -0.010·(S + P1))))
P1' = (((v)⊗(k) + (v)⊗(k)) + (σ(0.530)·(((v)⊗(k) + (v)⊗(k)) + (((S + P1))((k)⊗(k)) + -0.010·(S + P1))) + σ(0)·(((v)⊗(k) + (v)⊗(k)) - (((S + P1))((k)⊗(k)) + -0.010·(S + P1)))))
P2' = (σ(0.530)·(((v)⊗(k) + (v)⊗(k)) + (((S + P1))((k)⊗(k)) + -0.010·(S + P1))) + σ(0)·(((v)⊗(k) + (v)⊗(k)) - (((S + P1))((k)⊗(k)) + -0.010·(S + P1))))

Effective program (21 instructions):
  M0 = MatAdd(M0, M1)
  M1 = Outer(V1, V0)
  M2 = Outer(V0, V0)
  s1 = Sigmoid(s1)
  M1 = MatAdd(M1, M1)
  M2 = MatMul(M0, M2)
  s0 = -0.0104
  M3 = MatScale(s0, M0)
  M2 = MatAdd(M2, M3)
  M3 = MatSub(M1, M2)
  M3 = MatScale(s1, M3)
  M0 = MatAdd(M0, M3)
  s2 = 0.5303
  M2 = MatAdd(M1, M2)
  s1 = Sigmoid(s2)
  M2 = MatScale(s1, M2)
  M2 = MatAdd(M2, M3)
  M1 = MatAdd(M1, M2)
  s1 = Sigmoid(s1)
  M3 = MatScale(s1, M3)
  M0 = MatAdd(M0, M3)

structure: unclassified  [a=1.041 b=1.656 c=-0.847 g=0.001, erase c/a=0.813, R²=0.5783, 1408 steps]

train acc 0.676 ±0.013
test regime collision3: acc 0.685  margin 0.077  ±0.006
test d16 T12 ow0.3: acc 0.937  margin 0.289  ±0.004
test d16 T12 ow0.0: acc 0.893  margin 0.245  ±0.004
test d16 T12 ow0.6: acc 0.960  margin 0.301  ±0.004
test d32 T24 ow0.3: acc 0.986  margin 0.376  ±0.002
test d8 T6 ow0.3: acc 0.841  margin 0.140  ±0.008
test d16 T64 K8 ow0.3: acc 0.864  margin 0.204  ±0.008
test d16 T128 K8 ow0.3: acc 0.861  margin 0.199  ±0.011
```

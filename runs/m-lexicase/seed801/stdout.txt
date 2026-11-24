# Search seed 801

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 763131  time: 4707s  pop: 500  tournament: 10

commit: dce11aa  task seed: 801  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 200052 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 756 candidates
* unclassified: 3060 candidates
* linear attention: 3700 candidates
* delta rule: 108532 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.364): 3700 candidates
- delta rule (beta=1) (acc 0.585): 108532 candidates
- delta rule (beta=0.5) (acc 0.628): 108532 candidates
- gated delta (alpha=0.9) (acc 0.506): 15604 candidates

## Best rule

```
S' = (σ(σ(1.148))·((σ(1.148)·(v)⊗(k) + (v)⊗(k)) + (σ(1.148)·(v)⊗(k) + (v)⊗(k))) + (((S - P2) + S) - ((((S - P2) + S) + (σ(1.148)·(v)⊗(k) + (v)⊗(k))))(((σ(1.148)·(v)⊗(k))ᵀ)((v)⊗(k)))))
P1' = σ(σ(1.148))·((σ(1.148)·(v)⊗(k) + (v)⊗(k)) + (σ(1.148)·(v)⊗(k) + (v)⊗(k)))
P2' = (((S - P2) + S) - ((((S - P2) + S) + (σ(1.148)·(v)⊗(k) + (v)⊗(k))))(((σ(1.148)·(v)⊗(k))ᵀ)((v)⊗(k))))

Effective program (16 instructions):
  M1 = MatSub(M0, M2)
  M0 = MatAdd(M1, M0)
  M1 = Outer(V1, V0)
  s3 = 1.1475
  s0 = Sigmoid(s3)
  M2 = MatScale(s0, M1)
  M3 = MatAdd(M2, M1)
  M2 = Transpose(M2)
  M2 = MatMul(M2, M1)
  M1 = MatAdd(M0, M3)
  M2 = MatMul(M1, M2)
  M1 = MatAdd(M3, M3)
  s0 = Sigmoid(s0)
  M2 = MatSub(M0, M2)
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M1, M2)

structure: unclassified  [a=1.032 b=1.065 c=-0.772 g=-0.000, erase c/a=0.748, R²=0.5415, 1408 steps]

train acc 0.675 ±0.013
test regime collision3: acc 0.674  margin 0.061  ±0.006
test d16 T12 ow0.3: acc 0.922  margin 0.279  ±0.004
test d16 T12 ow0.0: acc 0.872  margin 0.230  ±0.004
test d16 T12 ow0.6: acc 0.951  margin 0.294  ±0.004
test d32 T24 ow0.3: acc 0.978  margin 0.365  ±0.002
test d8 T6 ow0.3: acc 0.813  margin 0.127  ±0.008
test d16 T64 K8 ow0.3: acc 0.870  margin 0.216  ±0.007
test d16 T128 K8 ow0.3: acc 0.881  margin 0.216  ±0.010
```

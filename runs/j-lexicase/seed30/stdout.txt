# Search seed 30

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 712791  time: 4154s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 550004 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2548 candidates
* linear attention: 2804 candidates
* decayed linear attention: 10484 candidates
* gated delta rule: 175220 candidates
* delta rule: 176372 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 2804 candidates
- delta rule (beta=1) (acc 0.578): 176372 candidates
- delta rule (beta=0.5) (acc 0.617): 177652 candidates
- gated delta (alpha=0.9) (acc 0.519): 175220 candidates

## Best rule

```
S' = ((σ(0)·((((k)⊗(tanh(v)))ᵀ + P2) + ((k)⊗(tanh(v)))ᵀ) - ((((P2 + S) - P1))((k)⊗(tanh(v))))(σ(0)·((((k)⊗(tanh(v)))ᵀ + P2) + ((k)⊗(tanh(v)))ᵀ))) + ((P2 + S) - P1))
P1' = 0·((σ(0)·((((k)⊗(tanh(v)))ᵀ + P2) + ((k)⊗(tanh(v)))ᵀ) - ((((P2 + S) - P1))((k)⊗(tanh(v))))(σ(0)·((((k)⊗(tanh(v)))ᵀ + P2) + ((k)⊗(tanh(v)))ᵀ))) + ((P2 + S) - P1))
P2' = 1.144·(((((P2 + S) - P1))((k)⊗(tanh(v))))(σ(0)·((((k)⊗(tanh(v)))ᵀ + P2) + ((k)⊗(tanh(v)))ᵀ)) + (σ(0)·((((k)⊗(tanh(v)))ᵀ + P2) + ((k)⊗(tanh(v)))ᵀ) - ((((P2 + S) - P1))((k)⊗(tanh(v))))(σ(0)·((((k)⊗(tanh(v)))ᵀ + P2) + ((k)⊗(tanh(v)))ᵀ))))

Effective program (17 instructions):
  s2 = Sigmoid(s1)
  M0 = MatAdd(M2, M0)
  M0 = MatSub(M0, M1)
  V2 = Tanh(V1)
  M1 = Outer(V0, V2)
  M3 = MatMul(M0, M1)
  M1 = Transpose(M1)
  M2 = MatAdd(M1, M2)
  M2 = MatAdd(M2, M1)
  M1 = MatScale(s2, M2)
  M2 = MatMul(M3, M1)
  s3 = 1.1445
  M1 = MatSub(M1, M2)
  M2 = MatAdd(M2, M1)
  M0 = MatAdd(M1, M0)
  M1 = MatScale(s1, M0)
  M2 = MatScale(s3, M2)

structure: unclassified  [a=1.047 b=0.911 c=-0.912 g=-0.014, erase c/a=0.871, R²=0.7236, 1408 steps]

train acc 0.674 ±0.013
test regime collision3: acc 0.682  margin 0.087  ±0.006
test d16 T12 ow0.3: acc 0.923  margin 0.267  ±0.004
test d16 T12 ow0.0: acc 0.883  margin 0.230  ±0.004
test d16 T12 ow0.6: acc 0.936  margin 0.269  ±0.005
test d32 T24 ow0.3: acc 0.967  margin 0.362  ±0.003
test d8 T6 ow0.3: acc 0.713  margin 0.066  ±0.009
test d16 T64 K8 ow0.3: acc 0.863  margin 0.209  ±0.008
test d16 T128 K8 ow0.3: acc 0.884  margin 0.215  ±0.010
```

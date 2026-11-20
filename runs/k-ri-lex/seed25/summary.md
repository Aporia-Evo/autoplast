# Search seed 25

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 956952  time: 8243s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 356927 attempts, 259156 blocks inserted, 274904 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 250100 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* linear attention: 1396 candidates
* decayed linear attention: 2804 candidates
* unclassified: 15988 candidates
* delta rule: 39796 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 1652 candidates
- delta rule (beta=1) (acc 0.578): 41204 candidates
- delta rule (beta=0.5) (acc 0.617): 42868 candidates
- gated delta (alpha=0.9) (acc 0.519): 39284 candidates

## Best rule

```
S' = (… + -0.490·(((S + ((v)⊗(tanh((k + 0.008·(v + k)))) + ((S)((P2 + (P2)ᵀ)) + -0.048·((v)⊗(tanh((k + 0.008·(v + k)))))((P2 + (P2)ᵀ))))) + (((S)((P2 + (P2)ᵀ)) + -0.048·((v)⊗(tanh((k + 0.008·(v + k)))))((P2 + (P2)ᵀ))) + ((S)((P2 + (P2)ᵀ)) + -0.048·((v)⊗(tanh((k + 0.008·(v + k)))))((P2 + (P2)ᵀ))))))((tanh((k + 0.008·(v + k))))⊗(((k + 0.008·(v + k)) + 0))))
P1' = -0.490·(((S + ((v)⊗(tanh((k + 0.008·(v + k)))) + ((S)((P2 + (P2)ᵀ)) + -0.048·((v)⊗(tanh((k + 0.008·(v + k)))))((P2 + (P2)ᵀ))))) + (((S)((P2 + (P2)ᵀ)) + -0.048·((v)⊗(tanh((k + 0.008·(v + k)))))((P2 + (P2)ᵀ))) + ((S)((P2 + (P2)ᵀ)) + -0.048·((v)⊗(tanh((k + 0.008·(v + k)))))((P2 + (P2)ᵀ))))))((tanh((k + 0.008·(v + k))))⊗(((k + 0.008·(v + k)) + 0)))
P2' = (tanh((k + 0.008·(v + k))))⊗(((k + 0.008·(v + k)) + 0))

Effective program (24 instructions):
  V4 = VecAdd(V1, V0)
  s3 = 0.0080
  V4 = VecScale(s3, V4)
  V0 = VecAdd(V0, V4)
  M3 = Transpose(M2)
  V5 = Tanh(V0)
  M1 = Outer(V1, V5)
  M2 = MatAdd(M2, M3)
  M3 = MatMul(M0, M2)
  M2 = MatMul(M1, M2)
  V3 = VecAdd(V0, V2)
  s0 = -0.0479
  M2 = MatScale(s0, M2)
  M3 = MatAdd(M3, M2)
  M1 = MatAdd(M1, M3)
  M0 = MatAdd(M0, M1)
  M1 = MatAdd(M3, M3)
  M0 = MatAdd(M0, M1)
  M2 = Outer(V5, V3)
  M1 = MatMul(M0, M2)
  s0 = -0.4899
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  M0 = MatAdd(M0, M1)

structure: unclassified  [a=1.023 b=0.052 c=-0.958 g=0.010, erase c/a=0.936, R²=0.4950, 1408 steps]

train acc 0.695 ±0.013
test regime collision3: acc 0.686  margin 0.093  ±0.006
test d16 T12 ow0.3: acc 0.909  margin 0.282  ±0.004
test d16 T12 ow0.0: acc 0.862  margin 0.233  ±0.004
test d16 T12 ow0.6: acc 0.944  margin 0.297  ±0.004
test d32 T24 ow0.3: acc 0.953  margin 0.361  ±0.003
test d8 T6 ow0.3: acc 0.796  margin 0.120  ±0.008
test d16 T64 K8 ow0.3: acc 0.832  margin 0.188  ±0.008
test d16 T128 K8 ow0.3: acc 0.832  margin 0.174  ±0.012
```

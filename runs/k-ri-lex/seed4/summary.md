# Search seed 4

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 888722  time: 6164s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 356252 attempts, 268065 blocks inserted, 296085 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1908 candidates
* linear attention: 3572 candidates
* decayed linear attention: 5364 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3572 candidates
- delta rule (beta=1) (acc 0.578): 102900 candidates
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 28788 candidates

## Best rule

```
S' = ((((((v)⊗(k) + 0.215·((S)((P2 - ((S + P1))ᵀ)))(S)) + 0.010·(S)(0.215·((S)((P2 - ((S + P1))ᵀ)))(S))) + 0.215·S) + -0.014·(((((v)⊗(k) + 0.215·((S)((P2 - ((S + P1))ᵀ)))(S)) + 0.010·(S)(0.215·((S)((P2 - ((S + P1))ᵀ)))(S))) + 0.215·S))(((((v)⊗(k) + 0.215·((S)((P2 - ((S + P1))ᵀ)))(S)) + 0.010·(S)(0.215·((S)((P2 - ((S + P1))ᵀ)))(S))) + 0.215·S))) + S)
P1' = (((((v)⊗(k) + 0.215·((S)((P2 - ((S + P1))ᵀ)))(S)) + 0.010·(S)(0.215·((S)((P2 - ((S + P1))ᵀ)))(S))) + 0.215·S) + -0.014·(((((v)⊗(k) + 0.215·((S)((P2 - ((S + P1))ᵀ)))(S)) + 0.010·(S)(0.215·((S)((P2 - ((S + P1))ᵀ)))(S))) + 0.215·S))(((((v)⊗(k) + 0.215·((S)((P2 - ((S + P1))ᵀ)))(S)) + 0.010·(S)(0.215·((S)((P2 - ((S + P1))ᵀ)))(S))) + 0.215·S)))
P2' = -0.218·0.215·S

Effective program (22 instructions):
  M1 = MatAdd(M0, M1)
  M3 = Transpose(M1)
  M1 = Outer(V1, V0)
  M2 = MatSub(M2, M3)
  M2 = MatMul(M0, M2)
  M3 = MatMul(M2, M0)
  s0 = 0.2149
  s1 = -0.2179
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  M2 = MatMul(M0, M3)
  s2 = 0.0100
  M2 = MatScale(s2, M2)
  M1 = MatAdd(M1, M2)
  M2 = MatScale(s0, M0)
  M1 = MatAdd(M1, M2)
  M3 = MatMul(M1, M1)
  s2 = -0.0141
  M3 = MatScale(s2, M3)
  M1 = MatAdd(M1, M3)
  M0 = MatAdd(M1, M0)
  M2 = MatScale(s1, M2)

structure: unclassified  [a=0.898 b=1.000 c=-0.064 g=-0.017, erase c/a=0.071, R²=0.7404, 1408 steps]

train acc 0.602 ±0.014
test regime collision3: acc 0.600  margin 0.023  ±0.006
test d16 T12 ow0.3: acc 0.879  margin 0.211  ±0.005
test d16 T12 ow0.0: acc 0.930  margin 0.233  ±0.003
test d16 T12 ow0.6: acc 0.832  margin 0.170  ±0.007
test d32 T24 ow0.3: acc 0.924  margin 0.291  ±0.004
test d8 T6 ow0.3: acc 0.704  margin 0.067  ±0.010
test d16 T64 K8 ow0.3: acc 0.589  margin 0.013  ±0.011
test d16 T128 K8 ow0.3: acc 0.499  margin -0.025  ±0.016
```

# Search seed 19

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 896788  time: 3352s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357497 attempts, 276733 blocks inserted, 290736 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1652 candidates
* decayed linear attention: 155892 candidates
* gated delta rule: 157044 candidates
* delta rule: 166772 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 2804 candidates
- delta rule (beta=1) (acc 0.578): 164980 candidates
- delta rule (beta=0.5) (acc 0.617): 166900 candidates
- gated delta (alpha=0.9) (acc 0.519): 157044 candidates

## Best rule

```
S' = (((((k)⊗((v + -0.180·S·k)) + (k)⊗((v + -0.180·S·k))) + ((k)⊗((v + -0.180·S·k)) + (k)⊗((v + -0.180·S·k)))) + ((((S + -0.004·(S)(P2)) + -0.004·(S)(P2)))ᵀ + 0.303·(((S + -0.004·(S)(P2)) + -0.004·(S)(P2)))ᵀ)))ᵀ
P1' = (((k)⊗((v + -0.180·S·k)) + (k)⊗((v + -0.180·S·k))) + ((k)⊗((v + -0.180·S·k)) + (k)⊗((v + -0.180·S·k))))
P2' = (…)((((((k)⊗((v + -0.180·S·k)) + (k)⊗((v + -0.180·S·k))) + ((k)⊗((v + -0.180·S·k)) + (k)⊗((v + -0.180·S·k)))) + ((((S + -0.004·(S)(P2)) + -0.004·(S)(P2)))ᵀ + 0.303·(((S + -0.004·(S)(P2)) + -0.004·(S)(P2)))ᵀ)))ᵀ)

Effective program (23 instructions):
  V4 = MatVec(M0, V0)
  s3 = -0.1801
  V4 = VecScale(s3, V4)
  V1 = VecAdd(V1, V4)
  M3 = MatMul(M0, M2)
  s1 = -0.0042
  M3 = MatScale(s1, M3)
  M0 = MatAdd(M0, M3)
  M0 = MatAdd(M0, M3)
  M1 = Outer(V0, V1)
  M1 = MatAdd(M1, M1)
  M1 = MatAdd(M1, M1)
  M2 = Transpose(M0)
  s3 = 0.3027
  M3 = MatScale(s3, M2)
  M2 = MatAdd(M2, M3)
  M2 = MatAdd(M1, M2)
  M0 = Transpose(M2)
  M2 = MatSub(M0, M1)
  s3 = 0.0229
  M2 = MatScale(s3, M2)
  M3 = MatAdd(M3, M2)
  M2 = MatMul(M3, M0)

structure: unclassified  [a=1.048 b=4.002 c=-0.690 g=-0.002, erase c/a=0.659, R²=0.9258, 1408 steps]

train acc 0.686 ±0.013
test regime collision3: acc 0.676  margin 0.079  ±0.006
test d16 T12 ow0.3: acc 0.947  margin 0.275  ±0.003
test d16 T12 ow0.0: acc 0.968  margin 0.280  ±0.002
test d16 T12 ow0.6: acc 0.928  margin 0.239  ±0.005
test d32 T24 ow0.3: acc 0.953  margin 0.323  ±0.003
test d8 T6 ow0.3: acc 0.839  margin 0.139  ±0.008
test d16 T64 K8 ow0.3: acc 0.610  margin 0.035  ±0.011
test d16 T128 K8 ow0.3: acc 0.427  margin -0.065  ±0.015
```

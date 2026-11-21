# Search seed 6

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 2100084  real evaluations (after cache): 1077797  time: 10247s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 1550068 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 628 candidates
* unclassified: 10996 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 11636 candidates
- delta rule (beta=1) (acc 0.578): 164980 candidates
- delta rule (beta=0.5) (acc 0.617): 194676 candidates
- gated delta (alpha=0.9) (acc 0.519): 162932 candidates

## Best rule

```
S' = …
P1' = (((P2 - P1) + ((((v)⊗(tanh(k)))((P1)(P1)) + (v)⊗(tanh(k))))((((v)⊗(tanh(k)))ᵀ)(σ(0.059)·(v)⊗(tanh(k))))))((((v)⊗(tanh(k)))ᵀ)(σ(0.059)·(v)⊗(tanh(k))))
P2' = 0.993·((P2 - P1) + ((((v)⊗(tanh(k)))((P1)(P1)) + (v)⊗(tanh(k))))((((v)⊗(tanh(k)))ᵀ)(σ(0.059)·(v)⊗(tanh(k)))))

Effective program (18 instructions):
  M2 = MatSub(M2, M1)
  V5 = Tanh(V0)
  M0 = Outer(V1, V5)
  s1 = 0.0586
  M3 = MatMul(M1, M1)
  s2 = Sigmoid(s1)
  M1 = MatMul(M0, M3)
  M3 = MatAdd(M1, M0)
  M1 = Transpose(M0)
  M0 = MatScale(s2, M0)
  M1 = MatMul(M1, M0)
  M0 = MatMul(M3, M1)
  M0 = MatAdd(M2, M0)
  M1 = MatMul(M0, M1)
  s2 = 0.9925
  M2 = MatScale(s2, M0)
  M0 = MatSub(M2, M1)
  M0 = MatSub(M0, M1)

structure: unclassified  [a=1.018 b=0.032 c=-0.941 g=0.002, erase c/a=0.924, R²=0.4680, 1408 steps]

train acc 0.689 ±0.013
test regime collision3: acc 0.694  margin 0.089  ±0.006
test d16 T12 ow0.3: acc 0.919  margin 0.265  ±0.004
test d16 T12 ow0.0: acc 0.916  margin 0.249  ±0.004
test d16 T12 ow0.6: acc 0.940  margin 0.262  ±0.005
test d32 T24 ow0.3: acc 0.976  margin 0.345  ±0.002
test d8 T6 ow0.3: acc 0.777  margin 0.112  ±0.009
test d16 T64 K8 ow0.3: acc 0.838  margin 0.164  ±0.008
test d16 T128 K8 ow0.3: acc 0.851  margin 0.161  ±0.011
```

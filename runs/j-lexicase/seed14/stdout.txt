# Search seed 14

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 625440  time: 3394s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1524 candidates
* unclassified: 2548 candidates
* delta rule: 435828 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 11252 candidates
- delta rule (beta=1) (acc 0.578): 430068 candidates
- delta rule (beta=0.5) (acc 0.617): 435828 candidates
- gated delta (alpha=0.9) (acc 0.519): 359284 candidates

## Best rule

```
S' = ((S + (v)⊗(k)) - (((S + (v)⊗(k)))((((S + (v)⊗(k)) + ((S)(P1))ᵀ))ᵀ))(σ(-0.289)·(v)⊗(k)))
P1' = (((S + (v)⊗(k)) + ((S)(P1))ᵀ))ᵀ
P2' = (S + (v)⊗(k))

Effective program (12 instructions):
  M3 = Outer(V1, V0)
  M2 = MatAdd(M0, M3)
  M1 = MatMul(M0, M1)
  s3 = -0.2890
  M0 = Transpose(M1)
  M1 = MatAdd(M2, M0)
  M1 = Transpose(M1)
  M0 = MatMul(M2, M1)
  s0 = Sigmoid(s3)
  M3 = MatScale(s0, M3)
  M3 = MatMul(M0, M3)
  M0 = MatSub(M2, M3)

structure: unclassified  [a=1.000 b=0.515 c=-0.431 g=-0.467, erase c/a=0.431, R²=0.9698, 1408 steps]

train acc 0.626 ±0.014
test regime collision3: acc 0.643  margin 0.048  ±0.006
test d16 T12 ow0.3: acc 0.932  margin 0.251  ±0.004
test d16 T12 ow0.0: acc 0.920  margin 0.237  ±0.003
test d16 T12 ow0.6: acc 0.933  margin 0.242  ±0.005
test d32 T24 ow0.3: acc 0.986  margin 0.337  ±0.002
test d8 T6 ow0.3: acc 0.770  margin 0.103  ±0.009
test d16 T64 K8 ow0.3: acc 0.798  margin 0.123  ±0.009
test d16 T128 K8 ow0.3: acc 0.784  margin 0.118  ±0.013
```

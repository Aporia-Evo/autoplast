# Search seed 10

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 737686  time: 3439s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 884 candidates
* unclassified: 5492 candidates
* linear attention: 6004 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6004 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 432372 candidates

## Best rule

```
S' = ((((S + P2))(((S + P2))ᵀ))(1.357·(((S + P2))(P1) - (S + P2))) - 1.357·(((S + P2))(P1) - (S + P2)))
P1' = ((S + P2))(((S + P2))ᵀ)
P2' = 0.582·(v)⊗(tanh(k))

Effective program (13 instructions):
  M2 = MatAdd(M0, M2)
  s3 = 1.3571
  M3 = MatMul(M2, M1)
  V0 = Tanh(V0)
  M1 = MatSub(M3, M2)
  M3 = MatScale(s3, M1)
  M0 = Transpose(M2)
  M1 = MatMul(M2, M0)
  M0 = MatMul(M1, M3)
  s0 = 0.5818
  M2 = Outer(V1, V0)
  M0 = MatSub(M0, M3)
  M2 = MatScale(s0, M2)

structure: unclassified  [a=0.962 b=0.001 c=-0.068 g=-0.010, erase c/a=0.071, R²=0.0032, 1408 steps]

train acc 0.572 ±0.014
test regime collision3: acc 0.564  margin -0.048  ±0.006
test d16 T12 ow0.3: acc 0.760  margin 0.105  ±0.006
test d16 T12 ow0.0: acc 0.795  margin 0.118  ±0.005
test d16 T12 ow0.6: acc 0.680  margin 0.018  ±0.009
test d32 T24 ow0.3: acc 0.851  margin 0.216  ±0.005
test d8 T6 ow0.3: acc 0.570  margin -0.126  ±0.010
test d16 T64 K8 ow0.3: acc 0.547  margin -0.057  ±0.011
test d16 T128 K8 ow0.3: acc 0.510  margin -0.080  ±0.016
```

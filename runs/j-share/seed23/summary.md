# Search seed 23

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1010465  time: 4708s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1396 candidates
* unclassified: 3444 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8820 candidates
- delta rule (beta=1) (acc 0.578): 91892 candidates
- delta rule (beta=0.5) (acc 0.617): 116340 candidates
- gated delta (alpha=0.9) (acc 0.519): 67316 candidates

## Best rule

```
S' = σ((σ(0) + 0))·(S - σ(0)·(((((S)(P2) + P1) - ((v + v))⊗(k)) + (S)(P2)) + (S)(P2)))
P1' = (((S)(P2) + P1) - ((v + v))⊗(k))
P2' = (σ(0)·(k + k))⊗(tanh(k))

Effective program (18 instructions):
  s0 = Sigmoid(s1)
  M2 = MatMul(M0, M2)
  s1 = Sigmoid(s1)
  V4 = VecAdd(V1, V1)
  M3 = Outer(V4, V0)
  M1 = MatAdd(M2, M1)
  M1 = MatSub(M1, M3)
  V2 = Tanh(V0)
  V5 = VecAdd(V0, V0)
  M3 = MatAdd(M1, M2)
  s2 = SAdd(s0, s3)
  M2 = MatAdd(M3, M2)
  M2 = MatScale(s1, M2)
  s1 = Sigmoid(s2)
  M0 = MatSub(M0, M2)
  M0 = MatScale(s1, M0)
  V1 = VecScale(s0, V5)
  M2 = Outer(V1, V2)

structure: unclassified  [a=0.977 b=0.623 c=-0.073 g=0.003, erase c/a=0.075, R²=0.3515, 1408 steps]

train acc 0.641 ±0.014
test regime collision3: acc 0.630  margin 0.050  ±0.006
test d16 T12 ow0.3: acc 0.875  margin 0.222  ±0.005
test d16 T12 ow0.0: acc 0.873  margin 0.211  ±0.004
test d16 T12 ow0.6: acc 0.828  margin 0.181  ±0.007
test d32 T24 ow0.3: acc 0.952  margin 0.334  ±0.003
test d8 T6 ow0.3: acc 0.621  margin 0.032  ±0.010
test d16 T64 K8 ow0.3: acc 0.788  margin 0.153  ±0.009
test d16 T128 K8 ow0.3: acc 0.782  margin 0.154  ±0.013
```

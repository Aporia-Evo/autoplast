# Search seed 26

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 507536  time: 231s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3572 candidates
* unclassified: 4340 candidates
* linear attention: 13940 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 13940 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 13940 candidates

## Best rule

```
S' = (((0 - S))((-1.081·(v)⊗(k))(-1.081·(v)⊗(k))) + <(k - (tanh(k) - v)), 0.950·(k - (tanh(k) - v))>·(S + (v)⊗(k)))

Effective program (15 instructions):
  M1 = MatSub(M1, M0)
  V2 = Tanh(V0)
  V5 = VecSub(V2, V1)
  M3 = Outer(V1, V0)
  V0 = VecSub(V0, V5)
  M0 = MatAdd(M0, M3)
  s2 = 0.9504
  V5 = VecScale(s2, V0)
  s3 = Dot(V0, V5)
  M0 = MatScale(s3, M0)
  s1 = -1.0814
  M3 = MatScale(s1, M3)
  M2 = MatMul(M3, M3)
  M1 = MatMul(M1, M2)
  M0 = MatAdd(M1, M0)

structure: unclassified  [a=0.954 b=0.953 c=-0.077 g=-0.021, erase c/a=0.080, R²=0.9754, 384 steps]

train acc 0.836 ±0.013
test d16 T12 ow0.3: acc 0.808  margin 0.161  ±0.006
test d16 T12 ow0.0: acc 0.863  margin 0.185  ±0.004
test d16 T12 ow0.6: acc 0.707  margin 0.099  ±0.009
test d32 T24 ow0.3: acc 0.868  margin 0.226  ±0.005
test d8 T6 ow0.3: acc 0.650  margin 0.042  ±0.010
test d16 T64 K8 ow0.3: acc 0.530  margin -0.018  ±0.011
test d16 T128 K8 ow0.3: acc 0.517  margin -0.039  ±0.016
```

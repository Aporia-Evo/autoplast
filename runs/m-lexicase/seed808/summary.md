# Search seed 808

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 815878  time: 1606s  pop: 500  tournament: 10

commit: dce11aa  task seed: 808  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 150004 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1140 candidates
* unclassified: 5364 candidates
* delta rule: 23540 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.368): 7796 candidates
- delta rule (beta=1) (acc 0.610): 23540 candidates
- delta rule (beta=0.5) (acc 0.637): 33908 candidates
- gated delta (alpha=0.9) (acc 0.527): 23540 candidates

## Best rule

```
S' = (((S - P1) + (((v + v) + ((v + v) - (S - P1)·tanh(k))))⊗(k)) + σ(0)·P2)
P1' = σ(0)·P2
P2' = ((((S - P1) + (((v + v) + ((v + v) - (S - P1)·tanh(k))))⊗(k)) + σ(0)·P2) + ((v + v))⊗((((((v + v) - (S - P1)·tanh(k)) - ((v + v) + ((v + v) - (S - P1)·tanh(k)))) - k) - k)))

Effective program (16 instructions):
  s3 = Sigmoid(s2)
  M0 = MatSub(M0, M1)
  V1 = VecAdd(V1, V1)
  V2 = Tanh(V0)
  V3 = MatVec(M0, V2)
  V4 = VecSub(V1, V3)
  M1 = MatScale(s3, M2)
  V3 = VecAdd(V1, V4)
  M2 = Outer(V3, V0)
  V4 = VecSub(V4, V3)
  V4 = VecSub(V4, V0)
  V4 = VecSub(V4, V0)
  M3 = Outer(V1, V4)
  M2 = MatAdd(M0, M2)
  M0 = MatAdd(M2, M1)
  M2 = MatAdd(M0, M3)

structure: unclassified  [a=1.018 b=4.004 c=-0.545 g=0.009, erase c/a=0.536, R²=0.7134, 1408 steps]

train acc 0.689 ±0.013
test regime collision3: acc 0.668  margin 0.056  ±0.006
test d16 T12 ow0.3: acc 0.933  margin 0.284  ±0.004
test d16 T12 ow0.0: acc 0.879  margin 0.234  ±0.004
test d16 T12 ow0.6: acc 0.943  margin 0.295  ±0.004
test d32 T24 ow0.3: acc 0.972  margin 0.367  ±0.002
test d8 T6 ow0.3: acc 0.803  margin 0.121  ±0.008
test d16 T64 K8 ow0.3: acc 0.868  margin 0.220  ±0.007
test d16 T128 K8 ow0.3: acc 0.893  margin 0.220  ±0.010
```

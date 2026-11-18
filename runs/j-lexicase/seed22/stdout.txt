# Search seed 22

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 807993  time: 2023s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 1500020 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 756 candidates
* unclassified: 1524 candidates
* linear attention: 3828 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3828 candidates
- delta rule (beta=1) (acc 0.578): 55284 candidates
- delta rule (beta=0.5) (acc 0.617): 55284 candidates
- gated delta (alpha=0.9) (acc 0.519): 45044 candidates

## Best rule

```
S' = (((P1 + P2)·(0 - k))⊗(k) + ((v)⊗((k + k)) + (P2 + S)))
P1' = σ(σ(-0.521))·(((P1 + P2)·(0 - k))⊗(k) + ((v)⊗((k + k)) + (P2 + S)))
P2' = ((((P1 + P2)·(0 - k))⊗(k) + (v)⊗((k + k))) - ((P1 + P2)·(0 - k))⊗(k))

Effective program (15 instructions):
  V3 = VecSub(V5, V0)
  M1 = MatAdd(M1, M2)
  V3 = MatVec(M1, V3)
  V5 = VecAdd(V0, V0)
  M1 = Outer(V1, V5)
  M0 = MatAdd(M2, M0)
  M2 = Outer(V3, V0)
  M0 = MatAdd(M1, M0)
  M0 = MatAdd(M2, M0)
  s3 = -0.5208
  s1 = Sigmoid(s3)
  s3 = Sigmoid(s1)
  M3 = MatAdd(M2, M1)
  M2 = MatSub(M3, M2)
  M1 = MatScale(s3, M0)

structure: unclassified  [a=1.038 b=1.999 c=-0.630 g=0.000, erase c/a=0.607, R²=0.7133, 1408 steps]

train acc 0.653 ±0.014
test regime collision3: acc 0.666  margin 0.061  ±0.006
test d16 T12 ow0.3: acc 0.930  margin 0.276  ±0.004
test d16 T12 ow0.0: acc 0.895  margin 0.239  ±0.004
test d16 T12 ow0.6: acc 0.953  margin 0.286  ±0.004
test d32 T24 ow0.3: acc 0.985  margin 0.361  ±0.002
test d8 T6 ow0.3: acc 0.821  margin 0.131  ±0.008
test d16 T64 K8 ow0.3: acc 0.860  margin 0.190  ±0.008
test d16 T128 K8 ow0.3: acc 0.860  margin 0.186  ±0.011
```

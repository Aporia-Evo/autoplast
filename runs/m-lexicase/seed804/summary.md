# Search seed 804

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 817656  time: 1778s  pop: 500  tournament: 10

commit: dce11aa  task seed: 804  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 400116 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* linear attention: 1524 candidates
* decayed linear attention: 6388 candidates
* unclassified: 71540 candidates
* delta rule: 78068 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.379): 1524 candidates
- delta rule (beta=1) (acc 0.589): 72948 candidates
- delta rule (beta=0.5) (acc 0.621): 74228 candidates
- gated delta (alpha=0.9) (acc 0.522): 6772 candidates

## Best rule

```
S' = ((0.645·P1·(0 - k))⊗(k) + ((norm(tanh(v)))⊗(0.358·(k - (0.645·0.645·P1 - (0.645·P1·(0 - k))⊗(k))·0.645·P1·(0 - k))) + P1))
P1' = ((norm(tanh(v)))⊗(0.358·(k - (0.645·0.645·P1 - (0.645·P1·(0 - k))⊗(k))·0.645·P1·(0 - k))) + ((0.645·P1·(0 - k))⊗(k) + ((norm(tanh(v)))⊗(0.358·(k - (0.645·0.645·P1 - (0.645·P1·(0 - k))⊗(k))·0.645·P1·(0 - k))) + P1)))
P2' = (norm(tanh(v)))⊗(0.358·(k - (0.645·0.645·P1 - (0.645·P1·(0 - k))⊗(k))·0.645·P1·(0 - k)))

Effective program (17 instructions):
  s0 = 0.6451
  M2 = MatScale(s0, M1)
  s3 = 0.3578
  V2 = Tanh(V1)
  V1 = VecSub(V4, V0)
  V3 = MatVec(M2, V1)
  M2 = MatScale(s0, M2)
  M0 = Outer(V3, V0)
  V2 = Normalize(V2)
  M2 = MatSub(M2, M0)
  V5 = MatVec(M2, V3)
  V0 = VecSub(V0, V5)
  V3 = VecScale(s3, V0)
  M2 = Outer(V2, V3)
  M3 = MatAdd(M2, M1)
  M0 = MatAdd(M0, M3)
  M1 = MatAdd(M2, M0)

structure: unclassified  [a=1.010 b=0.417 c=-0.635 g=-0.002, erase c/a=0.629, R²=0.3942, 1408 steps]

train acc 0.667 ±0.013
test regime collision3: acc 0.673  margin 0.069  ±0.006
test d16 T12 ow0.3: acc 0.918  margin 0.246  ±0.004
test d16 T12 ow0.0: acc 0.912  margin 0.229  ±0.004
test d16 T12 ow0.6: acc 0.917  margin 0.238  ±0.005
test d32 T24 ow0.3: acc 0.976  margin 0.337  ±0.002
test d8 T6 ow0.3: acc 0.759  margin 0.091  ±0.009
test d16 T64 K8 ow0.3: acc 0.844  margin 0.185  ±0.008
test d16 T128 K8 ow0.3: acc 0.872  margin 0.192  ±0.010
```

# Search seed 23

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 816485  time: 5285s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 300020 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2292 candidates
* decayed linear attention: 2548 candidates
* linear attention: 9076 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 9076 candidates
- delta rule (beta=1) (acc 0.578): 284148 candidates
- delta rule (beta=0.5) (acc 0.617): 287092 candidates
- gated delta (alpha=0.9) (acc 0.519): 107380 candidates

## Best rule

```
S' = ((0.637·((v)⊗(k) - P2))ᵀ - 0.637·…)
P1' = (((0.637·((v)⊗(k) - P2) + ((v)⊗(k))ᵀ) + ((P1 + (v)⊗(k)) + 0.637·((v)⊗(k) - P2))) - (((P1 + (v)⊗(k)) + 0.637·((v)⊗(k) - P2)))((((v)⊗(k))ᵀ)(0.637·((v)⊗(k) - P2))))
P2' = (0.637·((v)⊗(k) - P2))ᵀ

Effective program (17 instructions):
  M0 = Outer(V1, V0)
  M3 = MatSub(M0, M2)
  M2 = Transpose(M0)
  s0 = 0.6367
  M1 = MatAdd(M1, M0)
  M0 = MatScale(s0, M3)
  M3 = MatAdd(M0, M2)
  M1 = MatAdd(M1, M0)
  M2 = MatMul(M2, M0)
  M2 = MatMul(M1, M2)
  M1 = MatAdd(M3, M1)
  M1 = MatSub(M1, M2)
  M2 = Transpose(M0)
  M0 = MatSub(M3, M1)
  M3 = MatAdd(M0, M0)
  M3 = MatScale(s0, M3)
  M0 = MatSub(M2, M3)

structure: unclassified  [a=1.032 b=0.791 c=-0.658 g=-0.035, erase c/a=0.638, R²=0.5262, 1408 steps]

train acc 0.700 ±0.013
test regime collision3: acc 0.687  margin 0.078  ±0.006
test d16 T12 ow0.3: acc 0.935  margin 0.255  ±0.004
test d16 T12 ow0.0: acc 0.922  margin 0.243  ±0.003
test d16 T12 ow0.6: acc 0.906  margin 0.219  ±0.006
test d32 T24 ow0.3: acc 0.978  margin 0.351  ±0.002
test d8 T6 ow0.3: acc 0.744  margin 0.088  ±0.009
test d16 T64 K8 ow0.3: acc 0.800  margin 0.136  ±0.009
test d16 T128 K8 ow0.3: acc 0.801  margin 0.132  ±0.012
```

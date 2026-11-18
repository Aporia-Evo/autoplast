# Search seed 26

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 637097  time: 1663s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2420 candidates
* decayed linear attention: 3060 candidates
* linear attention: 9076 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 9076 candidates
- delta rule (beta=1) (acc 0.578): 1496692 candidates
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 434804 candidates

## Best rule

```
S' = (<k, norm((norm(k) - 0))>·(S + (v)⊗(k)) - ((S + (v)⊗(k))·tanh(tanh(tanh((norm(k) - 0)))))⊗((norm(k) - 0)))
P1' = ((S + (v)⊗(k))·tanh(tanh(tanh((norm(k) - 0)))))⊗((norm(k) - 0))
P2' = (S + (v)⊗(k))

Effective program (13 instructions):
  M3 = Outer(V1, V0)
  V4 = Normalize(V0)
  V3 = VecSub(V4, V5)
  V4 = Tanh(V3)
  V5 = Tanh(V4)
  M2 = MatAdd(M0, M3)
  V5 = Tanh(V5)
  V1 = Normalize(V3)
  V5 = MatVec(M2, V5)
  M1 = Outer(V5, V3)
  s2 = Dot(V0, V1)
  M0 = MatScale(s2, M2)
  M0 = MatSub(M0, M1)

structure: unclassified  [a=1.000 b=0.136 c=-0.856 g=0.017, erase c/a=0.856, R²=0.9765, 1408 steps]

train acc 0.600 ±0.014
test regime collision3: acc 0.609  margin 0.004  ±0.006
test d16 T12 ow0.3: acc 0.866  margin 0.254  ±0.005
test d16 T12 ow0.0: acc 0.802  margin 0.191  ±0.005
test d16 T12 ow0.6: acc 0.912  margin 0.299  ±0.005
test d32 T24 ow0.3: acc 0.946  margin 0.347  ±0.003
test d8 T6 ow0.3: acc 0.759  margin 0.099  ±0.009
test d16 T64 K8 ow0.3: acc 0.824  margin 0.218  ±0.008
test d16 T128 K8 ow0.3: acc 0.839  margin 0.217  ±0.011
```

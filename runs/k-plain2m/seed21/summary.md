# Search seed 21

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 2100084  real evaluations (after cache): 973979  time: 2236s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 756 candidates
* unclassified: 5492 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 9972 candidates
- delta rule (beta=1) (acc 0.578): 2038516 candidates
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 1151860 candidates

## Best rule

```
S' = (((0.438·P2 + 0.869·1/(0.495)·(v)⊗(k)) + (0.438·P2 + 0.869·1/(0.495)·(v)⊗(k))) - ((0.438·P2 + 0.869·1/(0.495)·(v)⊗(k))·1/(0.495)·k)⊗((k)⊗(k)·tanh(k)))
P1' = ((0.438·P2 + 0.869·1/(0.495)·(v)⊗(k))·1/(0.495)·k)⊗((k)⊗(k)·tanh(k))
P2' = ((0.438·P2 + 0.869·1/(0.495)·(v)⊗(k)) + (0.438·P2 + 0.869·1/(0.495)·(v)⊗(k)))

Effective program (17 instructions):
  s1 = 0.4953
  s3 = Recip(s1)
  M3 = Outer(V0, V0)
  V2 = Tanh(V0)
  V2 = MatVec(M3, V2)
  s1 = 0.8686
  M0 = Outer(V1, V0)
  M3 = MatScale(s3, M0)
  M1 = MatScale(s1, M3)
  s1 = 0.4382
  M0 = MatScale(s1, M2)
  M0 = MatAdd(M0, M1)
  V1 = VecScale(s3, V0)
  V5 = MatVec(M0, V1)
  M1 = Outer(V5, V2)
  M2 = MatAdd(M0, M0)
  M0 = MatSub(M2, M1)

structure: unclassified  [a=0.891 b=0.162 c=-0.847 g=0.001, erase c/a=0.950, R²=0.2573, 1408 steps]

train acc 0.578 ±0.014
test regime collision3: acc 0.589  margin 0.007  ±0.006
test d16 T12 ow0.3: acc 0.787  margin 0.163  ±0.006
test d16 T12 ow0.0: acc 0.759  margin 0.148  ±0.005
test d16 T12 ow0.6: acc 0.775  margin 0.147  ±0.008
test d32 T24 ow0.3: acc 0.674  margin 0.131  ±0.007
test d8 T6 ow0.3: acc 0.688  margin 0.065  ±0.010
test d16 T64 K8 ow0.3: acc 0.627  margin 0.025  ±0.011
test d16 T128 K8 ow0.3: acc 0.616  margin 0.011  ±0.015
```

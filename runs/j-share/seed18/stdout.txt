# Search seed 18

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 951125  time: 3199s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2676 candidates
* unclassified: 4084 candidates
* linear attention: 5748 candidates
* delta rule: 643956 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5748 candidates
- delta rule (beta=1) (acc 0.578): 298612 candidates
- delta rule (beta=0.5) (acc 0.617): 1368052 candidates
- gated delta (alpha=0.9) (acc 0.519): 111220 candidates

## Best rule

```
S' = ((S + ((v + v))⊗(k)) - ((S + ((v + v))⊗(k)))((tanh(k))⊗(σ(0)·k)))
P1' = (S + ((v + v))⊗(k))
P2' = (tanh(k))⊗(σ(0)·k)

Effective program (9 instructions):
  V2 = VecAdd(V1, V1)
  M1 = Outer(V2, V0)
  M1 = MatAdd(M0, M1)
  s2 = Sigmoid(s2)
  V2 = VecScale(s2, V0)
  V4 = Tanh(V0)
  M2 = Outer(V4, V2)
  M0 = MatMul(M1, M2)
  M0 = MatSub(M1, M0)

structure: delta rule  [a=1.000 b=1.055 c=-0.472 g=-0.000, erase c/a=0.472, R²=0.9997, 1408 steps]

train acc 0.615 ±0.014
test regime collision3: acc 0.641  margin 0.048  ±0.006
test d16 T12 ow0.3: acc 0.924  margin 0.259  ±0.004
test d16 T12 ow0.0: acc 0.904  margin 0.238  ±0.004
test d16 T12 ow0.6: acc 0.937  margin 0.256  ±0.005
test d32 T24 ow0.3: acc 0.986  margin 0.348  ±0.002
test d8 T6 ow0.3: acc 0.784  margin 0.109  ±0.009
test d16 T64 K8 ow0.3: acc 0.827  margin 0.150  ±0.008
test d16 T128 K8 ow0.3: acc 0.809  margin 0.140  ±0.012
```

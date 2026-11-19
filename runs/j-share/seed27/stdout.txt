# Search seed 27

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1025448  time: 2973s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1396 candidates
* unclassified: 3188 candidates
* linear attention: 5876 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5876 candidates
- delta rule (beta=1) (acc 0.578): 50804 candidates
- delta rule (beta=0.5) (acc 0.617): 73716 candidates
- gated delta (alpha=0.9) (acc 0.519): 47348 candidates

## Best rule

```
S' = (((tanh(σ(0)·(((S - P1))(P2) - (S - P1))·k) - v))⊗(tanh(k)) - (σ(0)·(((S - P1))(P2) - (S - P1)) + (0·(((S - P1))(P2) - (S - P1)) - ((v + 0))⊗(k))))
P1' = (σ(0)·(((S - P1))(P2) - (S - P1)) + (0·(((S - P1))(P2) - (S - P1)) - ((v + 0))⊗(k)))
P2' = 0·(((S - P1))(P2) - (S - P1))

Effective program (16 instructions):
  M1 = MatSub(M0, M1)
  V5 = VecAdd(V1, V2)
  V2 = Tanh(V0)
  M3 = MatMul(M1, M2)
  M0 = Outer(V5, V0)
  M2 = MatSub(M3, M1)
  s2 = Sigmoid(s1)
  M3 = MatScale(s2, M2)
  M2 = MatScale(s3, M2)
  M1 = MatSub(M2, M0)
  V0 = MatVec(M3, V0)
  V5 = Tanh(V0)
  V3 = VecSub(V5, V1)
  M0 = Outer(V3, V2)
  M1 = MatAdd(M3, M1)
  M0 = MatSub(M0, M1)

structure: unclassified  [a=1.020 b=0.055 c=-0.941 g=0.001, erase c/a=0.922, R²=0.4660, 1408 steps]

train acc 0.671 ±0.013
test regime collision3: acc 0.684  margin 0.079  ±0.006
test d16 T12 ow0.3: acc 0.934  margin 0.270  ±0.004
test d16 T12 ow0.0: acc 0.919  margin 0.250  ±0.003
test d16 T12 ow0.6: acc 0.944  margin 0.257  ±0.004
test d32 T24 ow0.3: acc 0.987  margin 0.353  ±0.002
test d8 T6 ow0.3: acc 0.814  margin 0.127  ±0.008
test d16 T64 K8 ow0.3: acc 0.804  margin 0.132  ±0.009
test d16 T128 K8 ow0.3: acc 0.796  margin 0.124  ±0.013
```

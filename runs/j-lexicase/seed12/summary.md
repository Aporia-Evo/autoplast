# Search seed 12

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 747347  time: 1500s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 950004 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 756 candidates
* unclassified: 3572 candidates
* linear attention: 13172 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 13172 candidates
- delta rule (beta=1) (acc 0.578): 930804 candidates
- delta rule (beta=0.5) (acc 0.617): 931572 candidates
- gated delta (alpha=0.9) (acc 0.519): 196596 candidates

## Best rule

```
S' = (P2 + (((v + v) - P2·norm(tanh(k))))⊗(tanh(tanh(k))))
P1' = ((((v + v) + (v + v)) + tanh(((v + v) + tanh(((P2 - P1) - P1)·k)))))⊗(norm(tanh(k)))
P2' = ((P2 + (((v + v) - P2·norm(tanh(k))))⊗(tanh(tanh(k)))) + (((((v + v) + (v + v)) + tanh(((v + v) + tanh(((P2 - P1) - P1)·k)))))⊗(norm(tanh(k))) + (P1 + 0)))

Effective program (20 instructions):
  V5 = VecAdd(V1, V1)
  M3 = MatAdd(M1, M3)
  M0 = MatSub(M2, M1)
  V2 = Tanh(V0)
  M0 = MatSub(M0, M1)
  V4 = Tanh(V2)
  V3 = Normalize(V2)
  V2 = MatVec(M0, V0)
  V2 = Tanh(V2)
  V2 = VecAdd(V5, V2)
  V0 = Tanh(V2)
  V2 = VecAdd(V5, V5)
  V2 = VecAdd(V2, V0)
  M1 = Outer(V2, V3)
  V2 = MatVec(M2, V3)
  M3 = MatAdd(M1, M3)
  V2 = VecSub(V5, V2)
  M0 = Outer(V2, V4)
  M0 = MatAdd(M2, M0)
  M2 = MatAdd(M0, M3)

structure: unclassified  [a=1.055 b=1.809 c=-0.945 g=-0.001, erase c/a=0.896, R²=0.6453, 1408 steps]

train acc 0.697 ±0.013
test regime collision3: acc 0.704  margin 0.098  ±0.006
test d16 T12 ow0.3: acc 0.947  margin 0.279  ±0.003
test d16 T12 ow0.0: acc 0.927  margin 0.246  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.284  ±0.004
test d32 T24 ow0.3: acc 0.991  margin 0.343  ±0.001
test d8 T6 ow0.3: acc 0.806  margin 0.116  ±0.008
test d16 T64 K8 ow0.3: acc 0.851  margin 0.184  ±0.008
test d16 T128 K8 ow0.3: acc 0.868  margin 0.179  ±0.011
```

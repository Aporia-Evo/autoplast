# Search seed 15

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 998158  time: 2193s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1396 candidates
* unclassified: 4084 candidates
* linear attention: 6260 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6260 candidates
- delta rule (beta=1) (acc 0.578): 13556 candidates
- delta rule (beta=0.5) (acc 0.617): 53876 candidates
- gated delta (alpha=0.9) (acc 0.519): 13556 candidates

## Best rule

```
S' = (((P1·v + (0 + v)))⊗((0 + k)) + (S - σ(0)·P2))
P1' = (σ(0)·(P2 + P1) - σ(0)·P2)
P2' = ((S - σ(0)·P2)·k)⊗((0 + k))

Effective program (15 instructions):
  V2 = VecAdd(V2, V1)
  M3 = MatAdd(M2, M1)
  V3 = VecAdd(V3, V0)
  V1 = MatVec(M1, V1)
  V5 = VecAdd(V1, V2)
  s0 = Sigmoid(s0)
  M2 = MatScale(s0, M2)
  M1 = MatScale(s0, M3)
  M1 = MatSub(M1, M2)
  V4 = VecAdd(V4, V0)
  M2 = MatSub(M0, M2)
  V0 = MatVec(M2, V0)
  M0 = Outer(V5, V4)
  M0 = MatAdd(M0, M2)
  M2 = Outer(V0, V3)

structure: unclassified  [a=0.949 b=1.069 c=-0.040 g=-0.000, erase c/a=0.042, R²=0.7176, 1408 steps]

train acc 0.624 ±0.014
test regime collision3: acc 0.631  margin 0.041  ±0.006
test d16 T12 ow0.3: acc 0.910  margin 0.230  ±0.004
test d16 T12 ow0.0: acc 0.927  margin 0.232  ±0.003
test d16 T12 ow0.6: acc 0.864  margin 0.199  ±0.007
test d32 T24 ow0.3: acc 0.970  margin 0.323  ±0.003
test d8 T6 ow0.3: acc 0.702  margin 0.070  ±0.010
test d16 T64 K8 ow0.3: acc 0.778  margin 0.127  ±0.009
test d16 T128 K8 ow0.3: acc 0.764  margin 0.118  ±0.013
```

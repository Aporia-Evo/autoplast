# Search seed 32

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500028  real evaluations (after cache): 1076658  time: 1989s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4596 candidates
* unclassified: 10244 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 22236 candidates
- delta rule (beta=1) (acc 0.578): 38764 candidates
- delta rule (beta=0.5) (acc 0.617): 41636 candidates
- gated delta (alpha=0.9) (acc 0.519): 33340 candidates

## Best rule

```
S' = (((3.511·3.511·v + (k - ((P1 - -0.552·P2)·k - k))))⊗(k) + (-0.552·P2 + (P2 + S)))
P1' = (P1 - -0.552·P2)
P2' = ((3.511·3.511·v + (k - ((P1 - -0.552·P2)·k - k))))⊗(k)

Effective program (14 instructions):
  s2 = -0.5519
  M0 = MatAdd(M2, M0)
  M2 = MatScale(s2, M2)
  s2 = 3.5112
  M0 = MatAdd(M2, M0)
  V1 = VecScale(s2, V1)
  M1 = MatSub(M1, M2)
  V3 = MatVec(M1, V0)
  V5 = VecSub(V3, V0)
  V4 = VecSub(V0, V5)
  V3 = VecScale(s2, V1)
  V1 = VecAdd(V3, V4)
  M2 = Outer(V1, V0)
  M0 = MatAdd(M2, M0)

structure: unclassified  [a=1.018 b=12.329 c=-0.382 g=0.000, erase c/a=0.375, R²=0.8542, 1408 steps]

train acc 0.649 ±0.014
test regime collision3: acc 0.655  margin 0.053  ±0.006
test d16 T12 ow0.3: acc 0.927  margin 0.262  ±0.004
test d16 T12 ow0.0: acc 0.905  margin 0.239  ±0.004
test d16 T12 ow0.6: acc 0.920  margin 0.253  ±0.005
test d32 T24 ow0.3: acc 0.984  margin 0.352  ±0.002
test d8 T6 ow0.3: acc 0.784  margin 0.111  ±0.009
test d16 T64 K8 ow0.3: acc 0.828  margin 0.159  ±0.008
test d16 T128 K8 ow0.3: acc 0.822  margin 0.152  ±0.012
```

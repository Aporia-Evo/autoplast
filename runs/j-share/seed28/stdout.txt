# Search seed 28

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 965099  time: 2476s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1524 candidates
* linear attention: 3060 candidates
* delta rule: 6260 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3060 candidates
- delta rule (beta=1) (acc 0.578): 6260 candidates
- delta rule (beta=0.5) (acc 0.617): 13940 candidates
- gated delta (alpha=0.9) (acc 0.519): 5364 candidates

## Best rule

```
S' = (((S)((0·P2 - 0·P2)) + S) + ((((0 + v) + tanh(0)) + ((S)((0·P2 - 0·P2)) + S)·(σ(0)·k - k)))⊗(k))
P1' = ((S)((0·P2 - 0·P2)) + S)
P2' = 0·P2

Effective program (14 instructions):
  V3 = VecAdd(V5, V1)
  M2 = MatScale(s2, M2)
  V2 = Tanh(V4)
  M1 = MatSub(M2, M2)
  M3 = MatMul(M0, M1)
  s0 = Sigmoid(s2)
  M1 = MatAdd(M3, M0)
  V1 = VecScale(s0, V0)
  V5 = VecSub(V1, V0)
  V1 = MatVec(M1, V5)
  V2 = VecAdd(V3, V2)
  V5 = VecAdd(V2, V1)
  M0 = Outer(V5, V0)
  M0 = MatAdd(M1, M0)

structure: delta rule  [a=1.000 b=1.000 c=-0.500 g=-0.000, erase c/a=0.500, R²=1.0000, 1408 steps]

train acc 0.617 ±0.014
test regime collision3: acc 0.640  margin 0.048  ±0.006
test d16 T12 ow0.3: acc 0.924  margin 0.262  ±0.004
test d16 T12 ow0.0: acc 0.900  margin 0.237  ±0.004
test d16 T12 ow0.6: acc 0.941  margin 0.264  ±0.005
test d32 T24 ow0.3: acc 0.987  margin 0.350  ±0.002
test d8 T6 ow0.3: acc 0.793  margin 0.113  ±0.008
test d16 T64 K8 ow0.3: acc 0.840  margin 0.161  ±0.008
test d16 T128 K8 ow0.3: acc 0.828  margin 0.154  ±0.012
```

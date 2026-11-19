# Search seed 6

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 953469  time: 3012s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 900084 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 628 candidates
* unclassified: 2932 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5364 candidates
- delta rule (beta=1) (acc 0.578): 162804 candidates
- delta rule (beta=0.5) (acc 0.617): 737140 candidates
- gated delta (alpha=0.9) (acc 0.519): 126068 candidates

## Best rule

```
S' = ((P2·k)⊗(norm((v + k))) - ((P1 - ((v + (P1·k + v)))⊗(k)) + P2))
P1' = (P1 - ((v + (P1·k + v)))⊗(k))
P2' = σ(σ(|(P1·k + v)|))·((P1 - ((v + (P1·k + v)))⊗(k)) + P2)

Effective program (15 instructions):
  V3 = MatVec(M1, V0)
  V3 = VecAdd(V3, V1)
  V4 = VecAdd(V1, V3)
  V2 = VecAdd(V1, V0)
  V2 = Normalize(V2)
  M0 = Outer(V4, V0)
  M1 = MatSub(M1, M0)
  s2 = Norm(V3)
  V4 = MatVec(M2, V0)
  s2 = Sigmoid(s2)
  s0 = Sigmoid(s2)
  M0 = Outer(V4, V2)
  M3 = MatAdd(M1, M2)
  M2 = MatScale(s0, M3)
  M0 = MatSub(M0, M3)

structure: unclassified  [a=1.017 b=2.014 c=-0.799 g=0.001, erase c/a=0.786, R²=0.4921, 1408 steps]

train acc 0.673 ±0.013
test regime collision3: acc 0.682  margin 0.081  ±0.006
test d16 T12 ow0.3: acc 0.942  margin 0.282  ±0.004
test d16 T12 ow0.0: acc 0.888  margin 0.235  ±0.004
test d16 T12 ow0.6: acc 0.954  margin 0.292  ±0.004
test d32 T24 ow0.3: acc 0.976  margin 0.366  ±0.002
test d8 T6 ow0.3: acc 0.815  margin 0.126  ±0.008
test d16 T64 K8 ow0.3: acc 0.864  margin 0.212  ±0.008
test d16 T128 K8 ow0.3: acc 0.884  margin 0.211  ±0.010
```

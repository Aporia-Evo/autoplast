# Search seed 14

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 953752  time: 2695s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 350068 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1396 candidates
* decayed linear attention: 1780 candidates
* delta rule: 115060 candidates
* delta + Kronecker mix: 549108 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 17908 candidates
- delta rule (beta=1) (acc 0.578): 115060 candidates
- delta rule (beta=0.5) (acc 0.617): 117620 candidates
- gated delta (alpha=0.9) (acc 0.519): 52340 candidates

## Best rule

```
S' = ((((v - S·k))⊗(k) + S) - ((0.609·k)⊗(norm(((v - S·k))⊗(k)·0.609·k)))ᵀ)
P1' = (0.609·k)⊗(norm(((v - S·k))⊗(k)·0.609·k))
P2' = (((v - S·k))⊗(k) + S)

Effective program (11 instructions):
  V4 = MatVec(M0, V0)
  V5 = VecSub(V1, V4)
  M1 = Outer(V5, V0)
  s1 = 0.6093
  M2 = MatAdd(M1, M0)
  V1 = VecScale(s1, V0)
  V5 = MatVec(M1, V1)
  V3 = Normalize(V5)
  M1 = Outer(V1, V3)
  M0 = Transpose(M1)
  M0 = MatSub(M2, M0)

structure: delta + Kronecker mix  [a=1.000 b=0.442 c=-0.445 g=-0.451, erase c/a=0.445, R²=0.9936, 1408 steps]

train acc 0.627 ±0.014
test regime collision3: acc 0.640  margin 0.038  ±0.006
test d16 T12 ow0.3: acc 0.922  margin 0.250  ±0.004
test d16 T12 ow0.0: acc 0.896  margin 0.228  ±0.004
test d16 T12 ow0.6: acc 0.933  margin 0.247  ±0.005
test d32 T24 ow0.3: acc 0.983  margin 0.340  ±0.002
test d8 T6 ow0.3: acc 0.772  margin 0.099  ±0.009
test d16 T64 K8 ow0.3: acc 0.823  margin 0.143  ±0.008
test d16 T128 K8 ow0.3: acc 0.807  margin 0.135  ±0.012
```

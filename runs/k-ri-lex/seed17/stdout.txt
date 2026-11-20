# Search seed 17

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 951272  time: 2370s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357211 attempts, 279110 blocks inserted, 290838 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 50036 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1524 candidates
* decayed linear attention: 1908 candidates
* linear attention: 6772 candidates
* gated delta rule: 23156 candidates
* delta rule: 45428 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6772 candidates
- delta rule (beta=1) (acc 0.578): 45428 candidates
- delta rule (beta=0.5) (acc 0.617): 45940 candidates
- gated delta (alpha=0.9) (acc 0.519): 23156 candidates

## Best rule

```
S' = ((((v + -0.134·S·k))⊗((((k + -0.134·-0.134·S·k) + 0.038·v) + ((k + -0.134·-0.134·S·k) + 0.038·v))) - (0 - S)) + (0.793·((v + -0.134·S·k))⊗((((k + -0.134·-0.134·S·k) + 0.038·v) + ((k + -0.134·-0.134·S·k) + 0.038·v))) - (P1)ᵀ))
P1' = 0.793·…
P2' = (0 - S)

Effective program (23 instructions):
  M2 = MatSub(M3, M0)
  M1 = Transpose(M1)
  V2 = MatVec(M0, V0)
  s2 = -0.1335
  V2 = VecScale(s2, V2)
  V5 = VecAdd(V1, V2)
  V3 = VecScale(s2, V2)
  V0 = VecAdd(V0, V3)
  s0 = 0.0383
  V1 = VecScale(s0, V1)
  V0 = VecAdd(V0, V1)
  V2 = VecAdd(V0, V0)
  M0 = Outer(V5, V2)
  s0 = 0.7933
  M3 = MatScale(s0, M0)
  M1 = MatSub(M3, M1)
  M0 = MatSub(M0, M2)
  M0 = MatAdd(M0, M1)
  M3 = MatMul(M3, M0)
  s1 = -0.0469
  M3 = MatScale(s1, M3)
  M1 = MatAdd(M1, M3)
  M1 = MatScale(s0, M1)

structure: unclassified  [a=1.010 b=3.571 c=-0.464 g=-0.000, erase c/a=0.459, R²=0.7182, 1408 steps]

train acc 0.675 ±0.013
test regime collision3: acc 0.666  margin 0.055  ±0.006
test d16 T12 ow0.3: acc 0.931  margin 0.243  ±0.004
test d16 T12 ow0.0: acc 0.910  margin 0.228  ±0.004
test d16 T12 ow0.6: acc 0.916  margin 0.221  ±0.005
test d32 T24 ow0.3: acc 0.977  margin 0.334  ±0.002
test d8 T6 ow0.3: acc 0.757  margin 0.096  ±0.009
test d16 T64 K8 ow0.3: acc 0.803  margin 0.133  ±0.009
test d16 T128 K8 ow0.3: acc 0.797  margin 0.126  ±0.013
```

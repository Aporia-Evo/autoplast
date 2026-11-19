# Search seed 11

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 999129  time: 2617s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 150004 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4724 candidates
* unclassified: 7028 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 7796 candidates
- delta rule (beta=1) (acc 0.578): 54772 candidates
- delta rule (beta=0.5) (acc 0.617): 63348 candidates
- gated delta (alpha=0.9) (acc 0.519): 54004 candidates

## Best rule

```
S' = (σ((σ(0) + σ(0)))·(S + (P2 - P1)) - (σ((σ(0) + σ(0)))·σ(σ(0))·((0 - v) + ((P2 - P1) + S)·k))⊗(σ(σ(0))·k))
P1' = σ((σ(0) + σ(0)))·(σ((σ(0) + σ(0)))·σ(σ(0))·((0 - v) + ((P2 - P1) + S)·k))⊗(σ(σ(0))·k)
P2' = (P2 - P1)

Effective program (18 instructions):
  M2 = MatSub(M2, M1)
  V2 = VecSub(V2, V1)
  M1 = MatAdd(M2, M0)
  s0 = Sigmoid(s0)
  V4 = MatVec(M1, V0)
  V1 = VecAdd(V2, V4)
  s2 = Sigmoid(s0)
  s1 = SAdd(s0, s0)
  s3 = Sigmoid(s1)
  M3 = MatAdd(M0, M2)
  s1 = Sigmoid(s1)
  V5 = VecScale(s2, V1)
  V0 = VecScale(s2, V0)
  V3 = VecScale(s1, V5)
  M0 = Outer(V3, V0)
  M1 = MatScale(s3, M0)
  M3 = MatScale(s1, M3)
  M0 = MatSub(M3, M0)

structure: unclassified  [a=1.032 b=0.283 c=-0.392 g=0.000, erase c/a=0.380, R²=0.9206, 1408 steps]

train acc 0.668 ±0.013
test regime collision3: acc 0.672  margin 0.071  ±0.006
test d16 T12 ow0.3: acc 0.944  margin 0.269  ±0.003
test d16 T12 ow0.0: acc 0.933  margin 0.256  ±0.003
test d16 T12 ow0.6: acc 0.912  margin 0.235  ±0.005
test d32 T24 ow0.3: acc 0.979  margin 0.362  ±0.002
test d8 T6 ow0.3: acc 0.786  margin 0.111  ±0.009
test d16 T64 K8 ow0.3: acc 0.829  margin 0.159  ±0.008
test d16 T128 K8 ow0.3: acc 0.835  margin 0.156  ±0.012
```

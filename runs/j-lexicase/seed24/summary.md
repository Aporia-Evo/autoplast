# Search seed 24

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 742536  time: 3981s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 400116 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2420 candidates
* decayed linear attention: 4212 candidates
* linear attention: 16244 candidates
* gated delta rule: 334580 candidates
* delta rule: 334836 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 10356 candidates
- delta rule (beta=1) (acc 0.578): 334836 candidates
- delta rule (beta=0.5) (acc 0.617): 335604 candidates
- gated delta (alpha=0.9) (acc 0.519): 334580 candidates

## Best rule

```
S' = (1/(σ(4.809))·((v)⊗(k) + (P2 + S)) + (((4.809·4.809·(v)⊗(k))((σ(1/(σ(4.809)))·k)⊗(k)) - 1/(σ(4.809))·((v)⊗(k) + (P2 + S))))((σ(1/(σ(4.809)))·k)⊗(k)))
P1' = (σ(1/(σ(4.809)))·k)⊗(k)
P2' = 1/(σ(4.809))·4.809·4.809·(v)⊗(k)

Effective program (17 instructions):
  M0 = MatAdd(M2, M0)
  M2 = Outer(V1, V0)
  s1 = 4.8094
  s2 = Sigmoid(s1)
  M0 = MatAdd(M2, M0)
  s2 = Recip(s2)
  s0 = Sigmoid(s2)
  s3 = SMul(s1, s1)
  V1 = VecScale(s0, V0)
  M1 = Outer(V1, V0)
  M0 = MatScale(s2, M0)
  M2 = MatScale(s3, M2)
  M3 = MatMul(M2, M1)
  M3 = MatSub(M3, M0)
  M2 = MatScale(s2, M2)
  M3 = MatMul(M3, M1)
  M0 = MatAdd(M0, M3)

structure: unclassified  [a=1.046 b=12.710 c=-0.758 g=0.001, erase c/a=0.725, R²=0.6213, 1408 steps]

train acc 0.667 ±0.013
test regime collision3: acc 0.677  margin 0.067  ±0.006
test d16 T12 ow0.3: acc 0.933  margin 0.287  ±0.004
test d16 T12 ow0.0: acc 0.894  margin 0.243  ±0.004
test d16 T12 ow0.6: acc 0.954  margin 0.297  ±0.004
test d32 T24 ow0.3: acc 0.987  margin 0.377  ±0.002
test d8 T6 ow0.3: acc 0.826  margin 0.135  ±0.008
test d16 T64 K8 ow0.3: acc 0.861  margin 0.204  ±0.008
test d16 T128 K8 ow0.3: acc 0.853  margin 0.198  ±0.011
```

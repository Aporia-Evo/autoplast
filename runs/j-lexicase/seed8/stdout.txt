# Search seed 8

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 769600  time: 3401s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 600052 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3956 candidates
* unclassified: 4468 candidates
* linear attention: 5108 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5108 candidates
- delta rule (beta=1) (acc 0.578): 58356 candidates
- delta rule (beta=0.5) (acc 0.617): 108276 candidates
- gated delta (alpha=0.9) (acc 0.519): 55028 candidates

## Best rule

```
S' = (((tanh(v))⊗(k) - (P1 - P2)) - (((tanh(v))⊗(k) - (P1 - P2)))((k)⊗(tanh(k))))
P1' = 0.943·|((P1 - P2) - (k)⊗(v))·tanh(k)|·(((tanh(v))⊗(k) - (P1 - P2)))((k)⊗(tanh(k)))
P2' = ((tanh(v))⊗(k) - (P1 - P2))

Effective program (15 instructions):
  M0 = MatSub(M1, M2)
  M3 = Outer(V0, V1)
  V4 = Tanh(V1)
  M2 = Outer(V4, V0)
  M1 = MatSub(M0, M3)
  V2 = Tanh(V0)
  V4 = MatVec(M1, V2)
  M2 = MatSub(M2, M0)
  M0 = Outer(V0, V2)
  s0 = Norm(V4)
  M3 = MatMul(M2, M0)
  s3 = 0.9426
  s0 = SMul(s3, s0)
  M1 = MatScale(s0, M3)
  M0 = MatSub(M2, M3)

structure: unclassified  [a=1.017 b=0.052 c=-0.959 g=0.002, erase c/a=0.943, R²=0.4616, 1408 steps]

train acc 0.696 ±0.013
test regime collision3: acc 0.686  margin 0.083  ±0.006
test d16 T12 ow0.3: acc 0.898  margin 0.256  ±0.005
test d16 T12 ow0.0: acc 0.929  margin 0.253  ±0.003
test d16 T12 ow0.6: acc 0.910  margin 0.249  ±0.005
test d32 T24 ow0.3: acc 0.936  margin 0.333  ±0.004
test d8 T6 ow0.3: acc 0.798  margin 0.117  ±0.008
test d16 T64 K8 ow0.3: acc 0.805  margin 0.152  ±0.009
test d16 T128 K8 ow0.3: acc 0.815  margin 0.154  ±0.012
```

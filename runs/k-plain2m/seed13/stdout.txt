# Search seed 13

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 2100084  real evaluations (after cache): 1078988  time: 3407s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 2100084 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* unclassified: 2676 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6388 candidates
- delta rule (beta=1) (acc 0.578): 1498612 candidates
- delta rule (beta=0.5) (acc 0.617): 2076276 candidates
- gated delta (alpha=0.9) (acc 0.519): 1474292 candidates

## Best rule

```
S' = ((((norm(v))⊗(k) + ((norm(v))⊗(k) + (P1 - P2))) + ((norm(v))⊗(k) + ((norm(v))⊗(k) + (P1 - P2)))) - 0.971·(((norm(v))⊗(k) + ((norm(v))⊗(k) + (P1 - P2))))((k)⊗((k + tanh(k)))))
P1' = ((norm(v))⊗(k) + ((norm(v))⊗(k) + (P1 - P2)))
P2' = ((tanh(k))⊗(tanh(tanh(((norm(v))⊗(k) + (P1 - P2))·tanh(tanh(k))))))ᵀ

Effective program (19 instructions):
  M1 = MatSub(M1, M2)
  V5 = Tanh(V0)
  V3 = VecAdd(V0, V5)
  V4 = Normalize(V1)
  M0 = Outer(V4, V0)
  M1 = MatAdd(M0, M1)
  V1 = Tanh(V5)
  V1 = MatVec(M1, V1)
  V1 = Tanh(V1)
  V1 = Tanh(V1)
  M3 = Outer(V5, V1)
  M1 = MatAdd(M0, M1)
  s1 = 0.9715
  M2 = Outer(V0, V3)
  M0 = MatAdd(M1, M1)
  M2 = MatMul(M1, M2)
  M2 = MatScale(s1, M2)
  M0 = MatSub(M0, M2)
  M2 = Transpose(M3)

structure: unclassified  [a=1.017 b=0.222 c=-0.959 g=0.001, erase c/a=0.943, R²=0.4646, 1408 steps]

train acc 0.668 ±0.013
test regime collision3: acc 0.684  margin 0.071  ±0.006
test d16 T12 ow0.3: acc 0.920  margin 0.281  ±0.004
test d16 T12 ow0.0: acc 0.868  margin 0.231  ±0.004
test d16 T12 ow0.6: acc 0.953  margin 0.299  ±0.004
test d32 T24 ow0.3: acc 0.969  margin 0.366  ±0.003
test d8 T6 ow0.3: acc 0.822  margin 0.131  ±0.008
test d16 T64 K8 ow0.3: acc 0.858  margin 0.204  ±0.008
test d16 T128 K8 ow0.3: acc 0.871  margin 0.199  ±0.010
```

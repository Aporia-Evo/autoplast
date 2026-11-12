# Search seed 15

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 695623  time: 2052s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1396 candidates
* unclassified: 8948 candidates
* linear attention: 18548 candidates
* delta rule: 19828 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 18548 candidates
- delta rule (beta=1) (acc 0.578): 19572 candidates
- delta rule (beta=0.5) (acc 0.617): 20724 candidates
- gated delta (alpha=0.9) (acc 0.519): 18932 candidates

## Best rule

```
S' = (P1 + (((tanh(v) - P2·tanh(k)))⊗(norm(tanh(tanh(k)))) + S))
P1' = (tanh(v))⊗(norm(tanh(tanh(k))))
P2' = ((-0.370·(P1 + (((tanh(v) - P2·tanh(k)))⊗(norm(tanh(tanh(k)))) + S)) + (tanh(v))⊗(norm(tanh(tanh(k))))) + (P1 + (((tanh(v) - P2·tanh(k)))⊗(norm(tanh(tanh(k)))) + S)))

Effective program (14 instructions):
  V3 = Tanh(V0)
  V5 = MatVec(M2, V3)
  V1 = Tanh(V1)
  V5 = VecSub(V1, V5)
  V3 = Tanh(V3)
  V0 = Normalize(V3)
  M2 = Outer(V5, V0)
  M0 = MatAdd(M2, M0)
  s0 = -0.3700
  M0 = MatAdd(M1, M0)
  M3 = MatScale(s0, M0)
  M1 = Outer(V1, V0)
  M2 = MatAdd(M3, M1)
  M2 = MatAdd(M2, M0)

structure: unclassified  [a=1.026 b=0.949 c=-0.617 g=0.002, erase c/a=0.602, R²=0.6219, 1408 steps]

train acc 0.656 ±0.014
test regime collision3: acc 0.663  margin 0.058  ±0.006
test d16 T12 ow0.3: acc 0.928  margin 0.265  ±0.004
test d16 T12 ow0.0: acc 0.885  margin 0.226  ±0.004
test d16 T12 ow0.6: acc 0.947  margin 0.275  ±0.004
test d32 T24 ow0.3: acc 0.980  margin 0.354  ±0.002
test d8 T6 ow0.3: acc 0.795  margin 0.112  ±0.008
test d16 T64 K8 ow0.3: acc 0.858  margin 0.190  ±0.008
test d16 T128 K8 ow0.3: acc 0.860  margin 0.186  ±0.011
```

# Search seed 15

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 2100084  real evaluations (after cache): 1015759  time: 2806s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 1050100 candidates

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
S' = (P1 + (((v - P2·tanh(k)))⊗(norm(tanh(k))) + S))
P1' = (v)⊗((norm(tanh(k)) + tanh(tanh(k))))
P2' = ((-0.249·(P1 + (((v - P2·tanh(k)))⊗(norm(tanh(k))) + S)) + (v)⊗((norm(tanh(k)) + tanh(tanh(k))))) + (P1 + (((v - P2·tanh(k)))⊗(norm(tanh(k))) + S)))

Effective program (14 instructions):
  V3 = Tanh(V0)
  V5 = MatVec(M2, V3)
  V5 = VecSub(V1, V5)
  V0 = Normalize(V3)
  V3 = Tanh(V3)
  M2 = Outer(V5, V0)
  M0 = MatAdd(M2, M0)
  V0 = VecAdd(V0, V3)
  s0 = -0.2491
  M0 = MatAdd(M1, M0)
  M3 = MatScale(s0, M0)
  M1 = Outer(V1, V0)
  M2 = MatAdd(M3, M1)
  M2 = MatAdd(M2, M0)

structure: unclassified  [a=1.033 b=1.000 c=-0.738 g=0.001, erase c/a=0.715, R²=0.5561, 1408 steps]

train acc 0.663 ±0.014
test regime collision3: acc 0.672  margin 0.060  ±0.006
test d16 T12 ow0.3: acc 0.924  margin 0.278  ±0.004
test d16 T12 ow0.0: acc 0.874  margin 0.230  ±0.004
test d16 T12 ow0.6: acc 0.948  margin 0.296  ±0.004
test d32 T24 ow0.3: acc 0.977  margin 0.365  ±0.002
test d8 T6 ow0.3: acc 0.818  margin 0.125  ±0.008
test d16 T64 K8 ow0.3: acc 0.865  margin 0.213  ±0.008
test d16 T128 K8 ow0.3: acc 0.873  margin 0.211  ±0.010
```

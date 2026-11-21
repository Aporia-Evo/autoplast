# Search seed 23

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 2100084  real evaluations (after cache): 803306  time: 2396s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1396 candidates
* unclassified: 6132 candidates
* linear attention: 7924 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 7924 candidates
- delta rule (beta=1) (acc 0.578): 1510388 candidates
- delta rule (beta=0.5) (acc 0.617): 1524084 candidates
- gated delta (alpha=0.9) (acc 0.519): 1508980 candidates

## Best rule

```
S' = ((tanh(v))⊗(tanh(k)) - (P2 - (S + P1)))
P1' = ((P2 - (S + P1)))((tanh(tanh(k)))⊗(tanh(tanh(tanh(tanh(tanh(tanh(k))))))))
P2' = -0.050·(tanh(tanh(k)))⊗(tanh(tanh(tanh(tanh(tanh(tanh(k)))))))

Effective program (15 instructions):
  M0 = MatAdd(M0, M1)
  V3 = Tanh(V0)
  V1 = Tanh(V1)
  V2 = Tanh(V3)
  M3 = MatSub(M2, M0)
  M0 = Outer(V1, V3)
  s2 = -0.0501
  V0 = Tanh(V2)
  V5 = Tanh(V0)
  V3 = Tanh(V5)
  V0 = Tanh(V3)
  M2 = Outer(V2, V0)
  M1 = MatMul(M3, M2)
  M0 = MatSub(M0, M3)
  M2 = MatScale(s2, M2)

structure: unclassified  [a=0.915 b=0.898 c=-0.043 g=0.002, erase c/a=0.048, R²=0.7307, 1408 steps]

train acc 0.622 ±0.014
test regime collision3: acc 0.630  margin 0.023  ±0.006
test d16 T12 ow0.3: acc 0.900  margin 0.252  ±0.005
test d16 T12 ow0.0: acc 0.864  margin 0.217  ±0.004
test d16 T12 ow0.6: acc 0.896  margin 0.254  ±0.006
test d32 T24 ow0.3: acc 0.965  margin 0.351  ±0.003
test d8 T6 ow0.3: acc 0.743  margin 0.090  ±0.009
test d16 T64 K8 ow0.3: acc 0.809  margin 0.178  ±0.009
test d16 T128 K8 ow0.3: acc 0.812  margin 0.172  ±0.012
```

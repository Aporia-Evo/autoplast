# Search seed 4

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 889341  time: 6079s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 500084 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* decayed linear attention: 1396 candidates
* linear attention: 4596 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 4596 candidates
- delta rule (beta=1) (acc 0.578): 192244 candidates
- delta rule (beta=0.5) (acc 0.617): 206836 candidates
- gated delta (alpha=0.9) (acc 0.519): 182132 candidates

## Best rule

```
S' = …
P1' = (tanh(norm(tanh(k))))⊗(norm(tanh(k)))
P2' = (((norm(tanh(v)))⊗(tanh(tanh(norm(tanh(k))))) + (S + (((S)(P1) + (((S)(P1))(P1) + (S)(P1))) + ((S)(P1) + (((S)(P1))(P1) + (S)(P1)))))) + (S)(P1))

Effective program (20 instructions):
  M2 = MatMul(M0, M1)
  M3 = MatMul(M2, M1)
  M1 = MatAdd(M3, M2)
  M1 = MatAdd(M2, M1)
  M1 = MatAdd(M1, M1)
  M3 = MatAdd(M0, M1)
  V5 = Tanh(V0)
  V1 = Tanh(V1)
  V3 = Normalize(V5)
  V0 = Tanh(V3)
  V4 = Tanh(V0)
  V1 = Normalize(V1)
  M0 = Outer(V1, V4)
  M1 = Outer(V0, V3)
  M3 = MatAdd(M0, M3)
  M0 = MatSub(M0, M0)
  M2 = MatAdd(M3, M2)
  M3 = MatSub(M0, M2)
  M0 = MatMul(M3, M1)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=1.019 b=0.043 c=-0.972 g=0.005, erase c/a=0.954, R²=0.4833, 1408 steps]

train acc 0.689 ±0.013
test regime collision3: acc 0.680  margin 0.084  ±0.006
test d16 T12 ow0.3: acc 0.917  margin 0.280  ±0.004
test d16 T12 ow0.0: acc 0.870  margin 0.228  ±0.004
test d16 T12 ow0.6: acc 0.950  margin 0.298  ±0.004
test d32 T24 ow0.3: acc 0.961  margin 0.363  ±0.003
test d8 T6 ow0.3: acc 0.769  margin 0.107  ±0.009
test d16 T64 K8 ow0.3: acc 0.842  margin 0.198  ±0.008
test d16 T128 K8 ow0.3: acc 0.851  margin 0.185  ±0.011
```

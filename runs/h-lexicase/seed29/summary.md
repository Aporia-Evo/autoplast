# Search seed 29

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 678954  time: 298s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* decayed linear attention: 1396 candidates
* linear attention: 7796 candidates
* linear, not error-correcting: 97780 candidates
* delta + Kronecker mix: 111860 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 7796 candidates
- delta rule (beta=1) (acc 0.858): 96244 candidates
- delta rule (beta=0.5) (acc 0.932): 119284 candidates
- gated delta (alpha=0.9) (acc 0.729): 7796 candidates

## Best rule

```
S' = (1.136·S + ((1.136·((1.136·tanh(v) + 1.136·tanh(v)) - S·tanh(k)) - norm(1.136·((1.136·tanh(v) + 1.136·tanh(v)) - S·tanh(k)))))⊗(k))

Effective program (13 instructions):
  V3 = Tanh(V0)
  V5 = MatVec(M0, V3)
  s2 = 1.1359
  V3 = Tanh(V1)
  V1 = VecScale(s2, V3)
  V2 = VecAdd(V1, V1)
  V3 = VecSub(V2, V5)
  V3 = VecScale(s2, V3)
  V5 = Normalize(V3)
  V2 = VecSub(V3, V5)
  M3 = Outer(V2, V0)
  M2 = MatScale(s2, M0)
  M0 = MatAdd(M2, M3)

structure: delta + Kronecker mix  [a=1.136 b=1.582 c=-0.754 g=-0.241, erase c/a=0.663, R²=0.9928, 384 steps]

train acc 0.977 ±0.005
test d16 T12 ow0.3: acc 0.969  margin 0.300  ±0.003
test d16 T12 ow0.0: acc 0.957  margin 0.276  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.289  ±0.004
test d32 T24 ow0.3: acc 0.974  margin 0.345  ±0.002
test d8 T6 ow0.3: acc 0.828  margin 0.131  ±0.008
test d16 T64 K8 ow0.3: acc 0.059  margin -0.542  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

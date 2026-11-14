# Search seed 2

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500084  real evaluations (after cache): 733474  time: 839s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 8

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3316 candidates
* linear, not error-correcting: 4092 candidates
* unclassified: 5756 candidates
* linear attention: 14228 candidates
* gated delta rule: 782052 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 14228 candidates
- delta rule (beta=1) (acc 0.858): 782052 candidates
- delta rule (beta=0.5) (acc 0.932): 782052 candidates
- gated delta (alpha=0.9) (acc 0.729): 14228 candidates

## Best rule

```
S' = ((((0 - S))(((tanh(tanh(tanh(v))))⊗(tanh(k)))ᵀ))((((tanh(tanh(tanh(v))))⊗(tanh(k)))ᵀ)ᵀ) + ((tanh(tanh(tanh(v))))⊗(tanh(k)) - 1.093·(0 - S)))

Effective program (14 instructions):
  M2 = MatSub(M1, M0)
  s2 = 1.0929
  V5 = Tanh(V1)
  V3 = Tanh(V5)
  V4 = Tanh(V3)
  V0 = Tanh(V0)
  M3 = Outer(V4, V0)
  M1 = MatScale(s2, M2)
  M0 = MatSub(M3, M1)
  M3 = Transpose(M3)
  M2 = MatMul(M2, M3)
  M3 = Transpose(M3)
  M2 = MatMul(M2, M3)
  M0 = MatAdd(M2, M0)

structure: gated delta rule  [a=1.093 b=0.834 c=-0.703 g=0.016, erase c/a=0.644, R²=0.9934, 384 steps]

train acc 0.970 ±0.006
test d16 T12 ow0.3: acc 0.964  margin 0.296  ±0.003
test d16 T12 ow0.0: acc 0.954  margin 0.274  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.285  ±0.004
test d32 T24 ow0.3: acc 0.984  margin 0.375  ±0.002
test d8 T6 ow0.3: acc 0.793  margin 0.118  ±0.008
test d16 T64 K8 ow0.3: acc 0.074  margin -0.479  ±0.006
test d16 T128 K8 ow0.3: acc 0.018  margin -0.632  ±0.004
```

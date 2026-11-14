# Search seed 9

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500113  real evaluations (after cache): 688962  time: 1166s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 3

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2164 candidates
* linear, not error-correcting: 2804 candidates
* unclassified: 4349 candidates
* linear attention: 15072 candidates
* gated Kronecker delta rule: 767461 candidates
* delta rule: 1194409 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 15072 candidates
- delta rule (beta=1) (acc 0.858): 1177803 candidates
- delta rule (beta=0.5) (acc 0.932): 1196749 candidates
- gated delta (alpha=0.9) (acc 0.729): 14816 candidates

## Best rule

```
S' = (((tanh(v))⊗(k) + ((tanh(v))⊗(k) + (S - 0))) + (((σ(0)·((tanh(v))⊗(k))ᵀ)(((tanh(v))⊗(k) + (S - 0))) - 2.421·(((tanh(v))⊗(k) + (S - 0)))(σ(0)·((tanh(v))⊗(k))ᵀ)))((σ(0)·((tanh(v))⊗(k))ᵀ)ᵀ))

Effective program (16 instructions):
  V4 = Tanh(V1)
  M3 = Outer(V4, V0)
  M1 = MatSub(M0, M2)
  M0 = Transpose(M3)
  M1 = MatAdd(M3, M1)
  s2 = Sigmoid(s2)
  M2 = MatScale(s2, M0)
  M0 = MatAdd(M3, M1)
  M3 = MatMul(M1, M2)
  s0 = 2.4214
  M1 = MatMul(M2, M1)
  M3 = MatScale(s0, M3)
  M2 = Transpose(M2)
  M3 = MatSub(M1, M3)
  M1 = MatMul(M3, M2)
  M0 = MatAdd(M0, M1)

structure: delta rule  [a=1.000 b=1.394 c=-0.549 g=0.029, erase c/a=0.549, R²=0.9970, 384 steps]

train acc 0.938 ±0.008
test d16 T12 ow0.3: acc 0.922  margin 0.265  ±0.004
test d16 T12 ow0.0: acc 0.892  margin 0.234  ±0.004
test d16 T12 ow0.6: acc 0.943  margin 0.274  ±0.004
test d32 T24 ow0.3: acc 0.985  margin 0.358  ±0.002
test d8 T6 ow0.3: acc 0.790  margin 0.111  ±0.008
test d16 T64 K8 ow0.3: acc 0.847  margin 0.176  ±0.008
test d16 T128 K8 ow0.3: acc 0.846  margin 0.172  ±0.011
```

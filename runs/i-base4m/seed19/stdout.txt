# Search seed 19

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1349419  time: 2027s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1268 candidates
* decayed linear attention: 1524 candidates
* linear, not error-correcting: 2036 candidates
* linear attention: 9588 candidates
* delta rule: 2110836 candidates
* gated delta rule: 2127604 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 9588 candidates
- delta rule (beta=1) (acc 0.858): 2112244 candidates
- delta rule (beta=0.5) (acc 0.932): 2114548 candidates
- gated delta (alpha=0.9) (acc 0.729): 9588 candidates

## Best rule

```
S' = (((tanh(v))⊗(k) + (S - -0.065·S)) + (-0.065·S)((((((tanh(v))⊗(k) + (S - -0.065·S)) + (((tanh(v))⊗(k) + ((tanh(v))⊗(k) + (tanh(v))⊗(k))))ᵀ) + (((tanh(v))⊗(k) + (S - -0.065·S)) + (((tanh(v))⊗(k) + ((tanh(v))⊗(k) + (tanh(v))⊗(k))))ᵀ)))(((tanh(v))⊗(k) + (tanh(v))⊗(k)))))

Effective program (14 instructions):
  V1 = Tanh(V1)
  M2 = Outer(V1, V0)
  s2 = -0.0648
  M1 = MatScale(s2, M0)
  M3 = MatAdd(M2, M2)
  M0 = MatSub(M0, M1)
  M0 = MatAdd(M2, M0)
  M2 = MatAdd(M2, M3)
  M2 = Transpose(M2)
  M2 = MatAdd(M0, M2)
  M2 = MatAdd(M2, M2)
  M2 = MatMul(M2, M3)
  M1 = MatMul(M1, M2)
  M0 = MatAdd(M0, M1)

structure: gated delta rule  [a=1.065 b=0.945 c=-0.717 g=-0.001, erase c/a=0.674, R²=0.9910, 384 steps]

train acc 0.969 ±0.006
test d16 T12 ow0.3: acc 0.959  margin 0.296  ±0.003
test d16 T12 ow0.0: acc 0.936  margin 0.263  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.300  ±0.004
test d32 T24 ow0.3: acc 0.992  margin 0.370  ±0.001
test d8 T6 ow0.3: acc 0.818  margin 0.129  ±0.008
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

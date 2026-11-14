# Search seed 18

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 811700  time: 889s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1908 candidates
* linear, not error-correcting: 2804 candidates
* unclassified: 3700 candidates
* linear attention: 4980 candidates
* delta + Kronecker mix: 307956 candidates
* delta rule: 311028 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 4980 candidates
- delta rule (beta=1) (acc 0.858): 101620 candidates
- delta rule (beta=0.5) (acc 0.932): 311028 candidates
- gated delta (alpha=0.9) (acc 0.729): 4980 candidates

## Best rule

```
S' = 1.074·(((tanh((tanh(S·k) - v)))⊗((tanh(S·k) - v)))(|(tanh(S·k) + v)|·σ(0)·(v)⊗(k)) - (0 - S))

Effective program (16 instructions):
  M1 = Outer(V1, V0)
  V0 = MatVec(M0, V0)
  V3 = Tanh(V0)
  V0 = VecSub(V3, V1)
  s2 = Sigmoid(s2)
  M1 = MatScale(s2, M1)
  M0 = MatSub(M3, M0)
  V1 = VecAdd(V3, V1)
  s3 = Norm(V1)
  V1 = Tanh(V0)
  M3 = Outer(V1, V0)
  M2 = MatScale(s3, M1)
  s1 = 1.0745
  M2 = MatMul(M3, M2)
  M0 = MatSub(M2, M0)
  M0 = MatScale(s1, M0)

structure: delta + Kronecker mix  [a=1.074 b=0.543 c=-0.569 g=-0.058, erase c/a=0.530, R²=0.9927, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.958  margin 0.279  ±0.003
test d16 T12 ow0.0: acc 0.956  margin 0.265  ±0.003
test d16 T12 ow0.6: acc 0.957  margin 0.264  ±0.004
test d32 T24 ow0.3: acc 0.993  margin 0.367  ±0.001
test d8 T6 ow0.3: acc 0.799  margin 0.116  ±0.008
test d16 T64 K8 ow0.3: acc 0.260  margin -0.208  ±0.010
test d16 T128 K8 ow0.3: acc 0.014  margin -0.557  ±0.004
```

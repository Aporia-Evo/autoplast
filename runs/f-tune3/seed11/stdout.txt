# Search seed 11

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500030  real evaluations (after cache): 852492  time: 1340s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 3

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1908 candidates
* linear, not error-correcting: 3060 candidates
* unclassified: 3060 candidates
* linear attention: 15362 candidates
* gated delta rule: 369246 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 15362 candidates
- delta rule (beta=1) (acc 0.858): 369246 candidates
- delta rule (beta=0.5) (acc 0.932): 369422 candidates
- gated delta (alpha=0.9) (acc 0.729): 14287 candidates

## Best rule

```
S' = (σ(0.182)·(((tanh(v))⊗(tanh(tanh(tanh(k)))) + S) + ((tanh(v))⊗(tanh(tanh(tanh(k)))) + S)) + (((tanh(v))⊗(tanh(tanh(tanh(k)))) + ((tanh(v))⊗(tanh(tanh(tanh(k)))) - S)))((((tanh(v))⊗(tanh(tanh(tanh(k)))))ᵀ)((tanh(v))⊗(tanh(tanh(tanh(k)))))))

Effective program (16 instructions):
  V2 = Tanh(V0)
  V3 = Tanh(V2)
  V0 = Tanh(V3)
  V4 = Tanh(V1)
  M1 = Outer(V4, V0)
  s2 = 0.1819
  M3 = Transpose(M1)
  M3 = MatMul(M3, M1)
  M2 = MatSub(M1, M0)
  M2 = MatAdd(M1, M2)
  M3 = MatMul(M2, M3)
  M0 = MatAdd(M1, M0)
  M1 = MatAdd(M0, M0)
  s0 = Sigmoid(s2)
  M0 = MatScale(s0, M1)
  M0 = MatAdd(M0, M3)

structure: gated delta rule  [a=1.090 b=2.079 c=-0.699 g=0.026, erase c/a=0.641, R²=0.9904, 384 steps]

train acc 0.972 ±0.006
test d16 T12 ow0.3: acc 0.961  margin 0.296  ±0.003
test d16 T12 ow0.0: acc 0.948  margin 0.272  ±0.003
test d16 T12 ow0.6: acc 0.960  margin 0.286  ±0.004
test d32 T24 ow0.3: acc 0.986  margin 0.378  ±0.002
test d8 T6 ow0.3: acc 0.790  margin 0.113  ±0.008
test d16 T64 K8 ow0.3: acc 0.075  margin -0.466  ±0.006
test d16 T128 K8 ow0.3: acc 0.021  margin -0.630  ±0.005
```

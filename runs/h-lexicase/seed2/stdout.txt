# Search seed 2

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 658917  time: 1009s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1652 candidates
* unclassified: 2548 candidates
* linear attention: 4212 candidates
* delta rule: 358516 candidates
* gated delta rule: 487668 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 4852 candidates
- delta rule (beta=1) (acc 0.858): 359284 candidates
- delta rule (beta=0.5) (acc 0.932): 364916 candidates
- gated delta (alpha=0.9) (acc 0.729): 4212 candidates

## Best rule

```
S' = ((1.099·S + (0 - (σ(1.895)·v)⊗(tanh(k)))) + ((((1.099·S + (0 - (σ(1.895)·v)⊗(tanh(k)))))((((σ(1.895)·v)⊗(tanh(k)))ᵀ)((0 - (σ(1.895)·v)⊗(tanh(k))))) + (σ(1.895)·v)⊗(tanh(k))) + (σ(1.895)·v)⊗(tanh(k))))

Effective program (15 instructions):
  s0 = 1.0993
  V0 = Tanh(V0)
  s3 = 1.8946
  s1 = Sigmoid(s3)
  V4 = VecScale(s1, V1)
  M2 = Outer(V4, V0)
  M3 = MatSub(M3, M2)
  M1 = Transpose(M2)
  M1 = MatMul(M1, M3)
  M0 = MatScale(s0, M0)
  M0 = MatAdd(M0, M3)
  M1 = MatMul(M0, M1)
  M3 = MatAdd(M1, M2)
  M3 = MatAdd(M3, M2)
  M0 = MatAdd(M0, M3)

structure: gated delta rule  [a=1.099 b=1.393 c=-0.752 g=0.006, erase c/a=0.684, R²=0.9985, 384 steps]

train acc 0.973 ±0.006
test d16 T12 ow0.3: acc 0.967  margin 0.306  ±0.003
test d16 T12 ow0.0: acc 0.952  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.300  ±0.004
test d32 T24 ow0.3: acc 0.975  margin 0.360  ±0.002
test d8 T6 ow0.3: acc 0.837  margin 0.135  ±0.008
test d16 T64 K8 ow0.3: acc 0.071  margin -0.497  ±0.006
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

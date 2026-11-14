# Search seed 14

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 614240  time: 758s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1012 candidates
* linear, not error-correcting: 1652 candidates
* linear attention: 5620 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 5620 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 5620 candidates

## Best rule

```
S' = ((|tanh(v)|·(tanh(norm(tanh(v))))⊗(k) + ((tanh(norm(tanh(v))))⊗(k) + |tanh(v)|·S)) + ((-0.492·|tanh(v)|·(tanh(norm(tanh(v))))⊗(k))(|tanh(v)|·S))((-0.492·|tanh(v)|·(tanh(norm(tanh(v))))⊗(k))(|tanh(v)|·S)))

Effective program (14 instructions):
  V5 = Tanh(V1)
  V2 = Normalize(V5)
  s0 = Norm(V5)
  V5 = Tanh(V2)
  M3 = Outer(V5, V0)
  M0 = MatScale(s0, M0)
  M2 = MatScale(s0, M3)
  s2 = -0.4918
  M1 = MatScale(s2, M2)
  M1 = MatMul(M1, M0)
  M1 = MatMul(M1, M1)
  M0 = MatAdd(M3, M0)
  M0 = MatAdd(M2, M0)
  M0 = MatAdd(M0, M1)

structure: linear attention  [a=0.952 b=1.859 c=-0.001 g=-0.016, erase c/a=0.001, R²=0.9947, 384 steps]

train acc 0.821 ±0.013
test d16 T12 ow0.3: acc 0.787  margin 0.149  ±0.006
test d16 T12 ow0.0: acc 0.867  margin 0.185  ±0.004
test d16 T12 ow0.6: acc 0.648  margin 0.068  ±0.009
test d32 T24 ow0.3: acc 0.878  margin 0.225  ±0.005
test d8 T6 ow0.3: acc 0.635  margin 0.032  ±0.010
test d16 T64 K8 ow0.3: acc 0.450  margin -0.059  ±0.011
test d16 T128 K8 ow0.3: acc 0.439  margin -0.081  ±0.016
```

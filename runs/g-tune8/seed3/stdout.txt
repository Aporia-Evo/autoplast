# Search seed 3

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500132  real evaluations (after cache): 1183806  time: 4888s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 200020 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* linear, not error-correcting: 1268 candidates
* decayed linear attention: 1524 candidates
* linear attention: 6164 candidates
* delta rule: 36236 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5388 candidates
- delta rule (beta=1) (acc 0.578): 34124 candidates
- delta rule (beta=0.5) (acc 0.617): 34748 candidates
- gated delta (alpha=0.9) (acc 0.519): 33948 candidates

## Best rule

```
S' = ((((P1 + P2) + S) + (-0.906·((P1 + P2) + S))((k)⊗(tanh(k)))) + ((((tanh(v) + tanh(v)) + (tanh(v) + tanh(v))) + ((tanh(v) + tanh(v)) + (tanh(v) + tanh(v)))))⊗(k))
P1' = (((((tanh(v) + tanh(v)) + (tanh(v) + tanh(v))) + ((tanh(v) + tanh(v)) + (tanh(v) + tanh(v)))))⊗(k) + σ(σ(|tanh(v)|))·P1)
P2' = σ(σ(|tanh(v)|))·P1

Effective program (19 instructions):
  V5 = Tanh(V0)
  M3 = Outer(V0, V5)
  M2 = MatAdd(M1, M2)
  M0 = MatAdd(M2, M0)
  s3 = -0.9060
  M2 = MatScale(s3, M0)
  M3 = MatMul(M2, M3)
  V5 = Tanh(V1)
  V1 = VecAdd(V5, V5)
  s0 = Norm(V5)
  s0 = Sigmoid(s0)
  s0 = Sigmoid(s0)
  M2 = MatScale(s0, M1)
  V4 = VecAdd(V1, V1)
  V3 = VecAdd(V4, V4)
  M1 = Outer(V3, V0)
  M3 = MatAdd(M0, M3)
  M0 = MatAdd(M3, M1)
  M1 = MatAdd(M1, M2)

structure: unclassified  [a=1.071 b=7.613 c=-0.909 g=-0.001, erase c/a=0.849, R²=0.8220, 1408 steps]

train acc 0.728 ±0.013
test regime collision3: acc 0.724  margin 0.112  ±0.006
test d16 T12 ow0.3: acc 0.950  margin 0.288  ±0.003
test d16 T12 ow0.0: acc 0.936  margin 0.269  ±0.003
test d16 T12 ow0.6: acc 0.938  margin 0.260  ±0.005
test d32 T24 ow0.3: acc 0.983  margin 0.377  ±0.002
test d8 T6 ow0.3: acc 0.816  margin 0.125  ±0.008
test d16 T64 K8 ow0.3: acc 0.873  margin 0.191  ±0.007
test d16 T128 K8 ow0.3: acc 0.880  margin 0.194  ±0.010
```

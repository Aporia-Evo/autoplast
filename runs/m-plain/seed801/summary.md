# Search seed 801

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 834511  time: 1350s  pop: 500  tournament: 10

commit: dce11aa  task seed: 801  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3572 candidates
* unclassified: 4212 candidates
* delta + Kronecker mix: 4340 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.364): 14196 candidates
- delta rule (beta=1) (acc 0.585): not reached
- delta rule (beta=0.5) (acc 0.628): not reached
- gated delta (alpha=0.9) (acc 0.506): 98164 candidates

## Best rule

```
S' = (P1 - (1.600·v)⊗(((tanh((v - k)) - tanh(((k + 0.248·k) + k))) - tanh(v))))
P1' = σ(1.981)·(P1 - (1.600·v)⊗(((tanh((v - k)) - tanh(((k + 0.248·k) + k))) - tanh(v))))

Effective program (17 instructions):
  s0 = 0.2481
  V2 = VecScale(s0, V0)
  V2 = VecAdd(V0, V2)
  V3 = VecSub(V1, V0)
  V5 = Tanh(V3)
  V3 = VecAdd(V2, V0)
  V2 = Tanh(V3)
  V4 = Tanh(V1)
  V5 = VecSub(V5, V2)
  s3 = 1.5999
  V3 = VecSub(V5, V4)
  s1 = 1.9810
  V4 = VecScale(s3, V1)
  M0 = Outer(V4, V3)
  M0 = MatSub(M1, M0)
  s1 = Sigmoid(s1)
  M1 = MatScale(s1, M0)

structure: unclassified  [a=0.879 b=4.337 c=-0.000 g=-0.000, erase c/a=0.001, R²=0.9611, 1408 steps]

train acc 0.510 ±0.014
test regime collision3: acc 0.514  margin -0.042  ±0.006
test d16 T12 ow0.3: acc 0.732  margin 0.126  ±0.007
test d16 T12 ow0.0: acc 0.721  margin 0.110  ±0.006
test d16 T12 ow0.6: acc 0.718  margin 0.109  ±0.009
test d32 T24 ow0.3: acc 0.643  margin 0.101  ±0.007
test d8 T6 ow0.3: acc 0.615  margin 0.022  ±0.010
test d16 T64 K8 ow0.3: acc 0.581  margin -0.010  ±0.011
test d16 T128 K8 ow0.3: acc 0.557  margin -0.029  ±0.016
```

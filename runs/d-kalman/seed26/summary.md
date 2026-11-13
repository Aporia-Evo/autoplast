# Search seed 26

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 507578  time: 912s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* unclassified: 2804 candidates
* linear attention: 5364 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5364 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = <tanh(tanh(tanh(v))), norm(tanh(tanh(v)))>·((v)⊗(tanh(k)) + S)
P2' = (v)⊗(tanh(k))

Effective program (9 instructions):
  V0 = Tanh(V0)
  V3 = Tanh(V1)
  M2 = Outer(V1, V0)
  V0 = Tanh(V3)
  M0 = MatAdd(M2, M0)
  V2 = Tanh(V0)
  V1 = Normalize(V0)
  s3 = Dot(V2, V1)
  M0 = MatScale(s3, M0)

structure: decayed linear attention  [a=0.878 b=0.829 c=-0.001 g=0.008, erase c/a=0.001, R²=0.9956, 1408 steps]

train acc 0.511 ±0.014
test regime collision3: acc 0.516  margin -0.043  ±0.006
test d16 T12 ow0.3: acc 0.728  margin 0.124  ±0.007
test d16 T12 ow0.0: acc 0.703  margin 0.104  ±0.006
test d16 T12 ow0.6: acc 0.720  margin 0.111  ±0.009
test d32 T24 ow0.3: acc 0.795  margin 0.193  ±0.006
test d8 T6 ow0.3: acc 0.632  margin 0.021  ±0.010
test d16 T64 K8 ow0.3: acc 0.583  margin -0.012  ±0.011
test d16 T128 K8 ow0.3: acc 0.553  margin -0.029  ±0.016
```

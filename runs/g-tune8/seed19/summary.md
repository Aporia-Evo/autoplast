# Search seed 19

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500068  real evaluations (after cache): 935767  time: 1845s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 1140 candidates
* linear attention: 10796 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 10796 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = 0.439·((S + (v)⊗(norm(tanh(tanh((tanh(tanh(k)) + tanh(tanh(tanh(k))))))))) + S)
P1' = ((S + (v)⊗(norm(tanh(tanh((tanh(tanh(k)) + tanh(tanh(tanh(k))))))))) + S)

Effective program (12 instructions):
  V3 = Tanh(V0)
  V3 = Tanh(V3)
  V0 = Tanh(V3)
  V0 = VecAdd(V3, V0)
  V4 = Tanh(V0)
  V4 = Tanh(V4)
  V4 = Normalize(V4)
  M3 = Outer(V1, V4)
  M3 = MatAdd(M0, M3)
  M1 = MatAdd(M3, M0)
  s1 = 0.4388
  M0 = MatScale(s1, M1)

structure: unclassified  [a=0.878 b=0.431 c=-0.000 g=0.000, erase c/a=0.000, R²=0.9637, 1408 steps]

train acc 0.514 ±0.014
test regime collision3: acc 0.514  margin -0.043  ±0.006
test d16 T12 ow0.3: acc 0.736  margin 0.127  ±0.007
test d16 T12 ow0.0: acc 0.713  margin 0.108  ±0.006
test d16 T12 ow0.6: acc 0.713  margin 0.108  ±0.009
test d32 T24 ow0.3: acc 0.635  margin 0.097  ±0.007
test d8 T6 ow0.3: acc 0.630  margin 0.027  ±0.010
test d16 T64 K8 ow0.3: acc 0.572  margin -0.013  ±0.011
test d16 T128 K8 ow0.3: acc 0.547  margin -0.031  ±0.016
```

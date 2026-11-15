# Search seed 21

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500164  real evaluations (after cache): 1005579  time: 2023s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 756 candidates
* unclassified: 3196 candidates
* linear attention: 3708 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3708 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 22404 candidates

## Best rule

```
S' = (|tanh(tanh(tanh((k + σ(1.970)·v))))|·(σ(1.970)·v)⊗(tanh(k)) + σ(1.970)·S)
P2' = |tanh(tanh(tanh((k + σ(1.970)·v))))|·(σ(1.970)·v)⊗(tanh(k))

Effective program (13 instructions):
  s3 = 1.9695
  s2 = Sigmoid(s3)
  V4 = Tanh(V0)
  V1 = VecScale(s2, V1)
  M2 = Outer(V1, V4)
  V3 = VecAdd(V0, V1)
  V3 = Tanh(V3)
  V2 = Tanh(V3)
  V5 = Tanh(V2)
  s0 = Norm(V5)
  M0 = MatScale(s2, M0)
  M2 = MatScale(s0, M2)
  M0 = MatAdd(M2, M0)

structure: unclassified  [a=0.878 b=0.883 c=0.000 g=0.010, erase c/a=-0.000, R²=0.9881, 1408 steps]

train acc 0.521 ±0.014
test regime collision3: acc 0.511  margin -0.045  ±0.006
test d16 T12 ow0.3: acc 0.730  margin 0.124  ±0.007
test d16 T12 ow0.0: acc 0.715  margin 0.109  ±0.006
test d16 T12 ow0.6: acc 0.710  margin 0.107  ±0.009
test d32 T24 ow0.3: acc 0.639  margin 0.098  ±0.007
test d8 T6 ow0.3: acc 0.629  margin 0.028  ±0.010
test d16 T64 K8 ow0.3: acc 0.578  margin -0.014  ±0.011
test d16 T128 K8 ow0.3: acc 0.548  margin -0.033  ±0.016
```

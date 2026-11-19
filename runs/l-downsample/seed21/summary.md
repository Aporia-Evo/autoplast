# Search seed 21

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 483814  time: 290s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2420 candidates
* linear, not error-correcting: 3828 candidates
* unclassified: 4468 candidates
* linear attention: 57716 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 57716 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 57460 candidates

## Best rule

```
S' = ((tanh(tanh(v)))⊗(((k + k) + tanh(k))) + |tanh(v)|·S)

Effective program (9 instructions):
  V4 = Tanh(V0)
  V1 = Tanh(V1)
  V3 = VecAdd(V0, V0)
  s0 = Norm(V1)
  V1 = Tanh(V1)
  V0 = VecAdd(V3, V4)
  M3 = Outer(V1, V0)
  M0 = MatScale(s0, M0)
  M0 = MatAdd(M3, M0)

structure: linear attention  [a=0.952 b=2.689 c=-0.001 g=0.006, erase c/a=0.001, R²=0.9959, 384 steps]

train acc 0.818 ±0.013
test d16 T12 ow0.3: acc 0.788  margin 0.150  ±0.006
test d16 T12 ow0.0: acc 0.867  margin 0.185  ±0.004
test d16 T12 ow0.6: acc 0.648  margin 0.069  ±0.009
test d32 T24 ow0.3: acc 0.878  margin 0.226  ±0.005
test d8 T6 ow0.3: acc 0.633  margin 0.033  ±0.010
test d16 T64 K8 ow0.3: acc 0.448  margin -0.056  ±0.011
test d16 T128 K8 ow0.3: acc 0.443  margin -0.079  ±0.016
```

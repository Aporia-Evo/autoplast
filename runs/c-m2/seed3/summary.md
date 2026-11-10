# Search seed 3

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 479643  time: 1101s  pop: 500  tournament: 10

commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1268 candidates
* linear attention: 9972 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 9972 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((v)⊗(norm(tanh(tanh((k + k))))) + 0.880·S)
P1' = 0.880·S

Effective program (8 instructions):
  s0 = 0.8799
  M1 = MatScale(s0, M0)
  V3 = VecAdd(V0, V0)
  V0 = Tanh(V3)
  V5 = Tanh(V0)
  V0 = Normalize(V5)
  M0 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)

structure: unclassified  [a=0.880 b=0.986 c=-0.000 g=0.000, erase c/a=0.000, R²=0.9714, 1408 steps]

train acc 0.512 ±0.014
test regime collision3: acc 0.515  margin -0.041  ±0.006
test d16 T12 ow0.3: acc 0.739  margin 0.129  ±0.007
test d16 T12 ow0.0: acc 0.719  margin 0.112  ±0.006
test d16 T12 ow0.6: acc 0.711  margin 0.108  ±0.009
test d32 T24 ow0.3: acc 0.643  margin 0.103  ±0.007
test d8 T6 ow0.3: acc 0.632  margin 0.029  ±0.010
test d16 T64 K8 ow0.3: acc 0.574  margin -0.011  ±0.011
test d16 T128 K8 ow0.3: acc 0.545  margin -0.030  ±0.016
```

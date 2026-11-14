# Search seed 20

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 418489  time: 189s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1268 candidates
* linear, not error-correcting: 2036 candidates
* unclassified: 3572 candidates
* linear attention: 20596 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 20596 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 20596 candidates

## Best rule

```
S' = <norm(tanh((k + k))), tanh(k)>·((v)⊗(k) + S)

Effective program (8 instructions):
  V5 = VecAdd(V0, V0)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M3, M0)
  V0 = Tanh(V0)
  V5 = Tanh(V5)
  V2 = Normalize(V5)
  s2 = Dot(V2, V0)
  M0 = MatScale(s2, M0)

structure: decayed linear attention  [a=0.949 b=0.950 c=0.000 g=0.000, erase c/a=-0.000, R²=0.9991, 384 steps]

train acc 0.812 ±0.014
test d16 T12 ow0.3: acc 0.788  margin 0.150  ±0.006
test d16 T12 ow0.0: acc 0.869  margin 0.186  ±0.004
test d16 T12 ow0.6: acc 0.652  margin 0.074  ±0.009
test d32 T24 ow0.3: acc 0.878  margin 0.226  ±0.005
test d8 T6 ow0.3: acc 0.645  margin 0.035  ±0.010
test d16 T64 K8 ow0.3: acc 0.444  margin -0.058  ±0.011
test d16 T128 K8 ow0.3: acc 0.459  margin -0.067  ±0.016
```

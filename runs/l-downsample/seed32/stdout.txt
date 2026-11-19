# Search seed 32

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 497311  time: 380s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* decayed linear attention: 1268 candidates
* linear, not error-correcting: 2164 candidates
* linear attention: 222196 candidates
* delta rule: 1391092 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 222580 candidates
- delta rule (beta=1) (acc 0.858): 1391092 candidates
- delta rule (beta=0.5) (acc 0.932): 1410164 candidates
- gated delta (alpha=0.9) (acc 0.729): 222196 candidates

## Best rule

```
S' = ((norm((S·norm(k) - S·k)))⊗(norm(k)) + ((<tanh(v), norm(v)>·tanh(v))⊗(k) + S))

Effective program (13 instructions):
  V4 = Tanh(V1)
  V3 = Normalize(V1)
  s1 = Dot(V4, V3)
  V4 = VecScale(s1, V4)
  M3 = Outer(V4, V0)
  V3 = Normalize(V0)
  V1 = MatVec(M0, V3)
  M1 = MatAdd(M3, M0)
  V2 = MatVec(M0, V0)
  V0 = VecSub(V1, V2)
  V1 = Normalize(V0)
  M0 = Outer(V1, V3)
  M0 = MatAdd(M0, M1)

structure: delta rule  [a=1.000 b=0.905 c=-0.539 g=0.010, erase c/a=0.539, R²=0.9949, 384 steps]

train acc 0.928 ±0.009
test d16 T12 ow0.3: acc 0.914  margin 0.259  ±0.004
test d16 T12 ow0.0: acc 0.883  margin 0.231  ±0.004
test d16 T12 ow0.6: acc 0.928  margin 0.258  ±0.005
test d32 T24 ow0.3: acc 0.982  margin 0.347  ±0.002
test d8 T6 ow0.3: acc 0.784  margin 0.109  ±0.009
test d16 T64 K8 ow0.3: acc 0.819  margin 0.144  ±0.009
test d16 T128 K8 ow0.3: acc 0.800  margin 0.132  ±0.013
```

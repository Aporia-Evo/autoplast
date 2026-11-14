# Search seed 11

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 872773  time: 177s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: random programs, no selection  tune-consts: 0

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* decayed linear attention: 1652 candidates
* linear attention: 7412 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 7412 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 7412 candidates

## Best rule

```
S' = ((v)⊗(k) + S)

Effective program (2 instructions):
  M2 = Outer(V1, V0)
  M0 = MatAdd(M2, M0)

structure: linear attention  [a=1.000 b=1.000 c=-0.000 g=0.000, erase c/a=0.000, R²=1.0000, 384 steps]

train acc 0.772 ±0.015
test d16 T12 ow0.3: acc 0.750  margin 0.132  ±0.006
test d16 T12 ow0.0: acc 0.917  margin 0.205  ±0.004
test d16 T12 ow0.6: acc 0.549  margin 0.018  ±0.009
test d32 T24 ow0.3: acc 0.828  margin 0.202  ±0.006
test d8 T6 ow0.3: acc 0.615  margin 0.019  ±0.010
test d16 T64 K8 ow0.3: acc 0.104  margin -0.325  ±0.007
test d16 T128 K8 ow0.3: acc 0.062  margin -0.419  ±0.008
```

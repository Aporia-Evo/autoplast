# Search seed 914

task: opt (testbed 2)  alphabet: 21 ops, with VecRecip, VecSqrt  readout: fixed o = S q  add-node mutation: on  candidates: 300020  real evaluations (after cache): 108516  time: 88s  pop: 500  tournament: 10

commit: dce11aa  task seed: 914  train episodes: 128  persistent registers: 1 matrix, 2 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 5748 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)


## Best rule

```
w' = 1/(((u2 + (1/(σ(0)·1/(w)) + 1/(σ(0)·1/(w)))) + (1/(σ(0)·1/(w)) + 1/(σ(0)·1/(w)))))
u2' = 0.643·1/(((u2 + (1/(σ(0)·1/(w)) + 1/(σ(0)·1/(w)))) + (1/(σ(0)·1/(w)) + 1/(σ(0)·1/(w)))))
u3' = σ(0)·1/(w)

Effective program (10 instructions):
  V1 = VecRecip(V0)
  s0 = Sigmoid(s2)
  V3 = VecScale(s0, V1)
  V4 = VecRecip(V3)
  V1 = VecAdd(V4, V4)
  s2 = 0.6433
  V5 = VecAdd(V2, V1)
  V1 = VecAdd(V5, V1)
  V0 = VecRecip(V1)
  V2 = VecScale(s2, V0)

train objective -0.0410  diverged 0.000  max_state 248.575
test opt train-distribution: objective -0.0303  diverged 0.000  max_state 249.311
test opt kappa1000: objective -0.0193  diverged 0.000  max_state 249.311
test opt d32: objective 0.0161  diverged 0.000  max_state 249.996
test opt d8: objective -0.0493  diverged 0.000  max_state 243.966
test opt sigma0.3: objective -0.0258  diverged 0.000  max_state 249.311
test opt T200: objective -0.0307  diverged 0.000  max_state 249.981
test opt scale10/0.1: objective -0.0303  diverged 0.000  max_state 249.311
```

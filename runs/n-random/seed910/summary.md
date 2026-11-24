# Search seed 910

task: opt (testbed 2)  alphabet: 21 ops, with VecRecip, VecSqrt  readout: fixed o = S q  add-node mutation: on  candidates: 300020  real evaluations (after cache): 164948  time: 128s  pop: 500  tournament: 10

commit: dce11aa  task seed: 910  train episodes: 128  persistent registers: 1 matrix, 2 vector, start zero  batch: 128

search: random programs, no selection  tune-consts: 0  select: fitness  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1908 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)


## Best rule

```
w' = (w - tanh(g))

Effective program (2 instructions):
  V5 = Tanh(V1)
  V0 = VecSub(V0, V5)

train objective -2.0675  diverged 0.000  max_state 0.000
test opt train-distribution: objective -2.1148  diverged 0.000  max_state 0.000
test opt kappa1000: objective -1.4388  diverged 0.000  max_state 0.000
test opt d32: objective -1.5313  diverged 0.000  max_state 0.000
test opt d8: objective -2.2068  diverged 0.000  max_state 0.000
test opt sigma0.3: objective -0.9748  diverged 0.000  max_state 0.000
test opt T200: objective -2.7978  diverged 0.000  max_state 0.000
test opt scale10/0.1: objective -0.0893  diverged 0.000  max_state 0.000
```

# Search seed 912

task: opt (testbed 2)  alphabet: 21 ops, with VecRecip, VecSqrt  readout: fixed o = S q  add-node mutation: on  candidates: 300020  real evaluations (after cache): 164828  time: 128s  pop: 500  tournament: 10

commit: dce11aa  task seed: 912  train episodes: 128  persistent registers: 1 matrix, 2 vector, start zero  batch: 128

search: random programs, no selection  tune-consts: 0  select: fitness  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 4724 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)


## Best rule

```
w' = (w - tanh(tanh(g)))
u2' = tanh(g)

Effective program (3 instructions):
  V2 = Tanh(V1)
  V1 = Tanh(V2)
  V0 = VecSub(V0, V1)

train objective -2.1143  diverged 0.000  max_state 0.983
test opt train-distribution: objective -2.1207  diverged 0.000  max_state 0.994
test opt kappa1000: objective -1.4397  diverged 0.000  max_state 0.814
test opt d32: objective -1.6095  diverged 0.000  max_state 0.999
test opt d8: objective -2.2075  diverged 0.000  max_state 0.933
test opt sigma0.3: objective -0.9809  diverged 0.000  max_state 0.994
test opt T200: objective -2.8056  diverged 0.000  max_state 0.948
test opt scale10/0.1: objective -0.2027  diverged 0.000  max_state 1.000
```

# Search seed 905

task: opt (testbed 2)  alphabet: 21 ops, with VecRecip, VecSqrt  readout: fixed o = S q  add-node mutation: on  candidates: 300020  real evaluations (after cache): 164385  time: 126s  pop: 500  tournament: 10

commit: dce11aa  task seed: 905  train episodes: 128  persistent registers: 1 matrix, 2 vector, start zero  batch: 128

search: random programs, no selection  tune-consts: 0  select: fitness  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)


## Best rule

```
w' = (w - tanh(g))
u2' = tanh(g)

Effective program (2 instructions):
  V2 = Tanh(V1)
  V0 = VecSub(V0, V2)

train objective -2.1305  diverged 0.000  max_state 0.942
test opt train-distribution: objective -2.1148  diverged 0.000  max_state 0.999
test opt kappa1000: objective -1.4388  diverged 0.000  max_state 0.853
test opt d32: objective -1.5313  diverged 0.000  max_state 1.000
test opt d8: objective -2.2068  diverged 0.000  max_state 0.933
test opt sigma0.3: objective -0.9748  diverged 0.000  max_state 0.999
test opt T200: objective -2.7978  diverged 0.000  max_state 0.982
test opt scale10/0.1: objective -0.0893  diverged 0.000  max_state 1.000
```

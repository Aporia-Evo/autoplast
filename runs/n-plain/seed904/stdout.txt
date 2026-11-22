# Search seed 904

task: opt (testbed 2)  alphabet: 21 ops, with VecRecip, VecSqrt  readout: fixed o = S q  add-node mutation: on  candidates: 300020  real evaluations (after cache): 185873  time: 577s  pop: 500  tournament: 10

commit: dce11aa  task seed: 904  train episodes: 128  persistent registers: 1 matrix, 2 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2548 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)


## Best rule

```
w' = ((u3 + w) - tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(g)))))))))))))))))))))))
u2' = (u3 + w)

Effective program (24 instructions):
  V1 = Tanh(V1)
  V1 = Tanh(V1)
  V2 = VecAdd(V3, V0)
  V4 = Tanh(V1)
  V5 = Tanh(V4)
  V4 = Tanh(V5)
  V0 = Tanh(V4)
  V1 = Tanh(V0)
  V5 = Tanh(V1)
  V5 = Tanh(V5)
  V1 = Tanh(V5)
  V1 = Tanh(V1)
  V5 = Tanh(V1)
  V1 = Tanh(V5)
  V0 = Tanh(V1)
  V0 = Tanh(V0)
  V1 = Tanh(V0)
  V1 = Tanh(V1)
  V4 = Tanh(V1)
  V1 = Tanh(V4)
  V5 = Tanh(V1)
  V1 = Tanh(V5)
  V5 = Tanh(V1)
  V0 = VecSub(V2, V5)

train objective -2.1677  diverged 0.000  max_state 4.382
test opt train-distribution: objective -2.1521  diverged 0.000  max_state 3.956
test opt kappa1000: objective -1.4475  diverged 0.000  max_state 3.878
test opt d32: objective -1.8789  diverged 0.000  max_state 3.980
test opt d8: objective -2.2143  diverged 0.000  max_state 3.877
test opt sigma0.3: objective -1.0376  diverged 0.000  max_state 4.093
test opt T200: objective -2.8404  diverged 0.000  max_state 4.172
test opt scale10/0.1: objective -0.6768  diverged 0.000  max_state 3.912
```

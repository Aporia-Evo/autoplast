# Search seed 907

task: opt (testbed 2)  alphabet: 21 ops, with VecRecip, VecSqrt  readout: fixed o = S q  add-node mutation: on  candidates: 300020  real evaluations (after cache): 222124  time: 792s  pop: 500  tournament: 10

commit: dce11aa  task seed: 907  train episodes: 128  persistent registers: 1 matrix, 2 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 4724 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)


## Best rule

```
w' = (w - tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(g))))))))))))))))))))))))
u2' = tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(g))))))))))))))))))))))
u3' = tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(g)))))))))))))

Effective program (24 instructions):
  V3 = Tanh(V1)
  V3 = Tanh(V3)
  V5 = Tanh(V3)
  V5 = Tanh(V5)
  V3 = Tanh(V5)
  V5 = Tanh(V3)
  V1 = Tanh(V5)
  V3 = Tanh(V1)
  V5 = Tanh(V3)
  V3 = Tanh(V5)
  V3 = Tanh(V3)
  V3 = Tanh(V3)
  V3 = Tanh(V3)
  V2 = Tanh(V3)
  V5 = Tanh(V2)
  V1 = Tanh(V5)
  V1 = Tanh(V1)
  V1 = Tanh(V1)
  V2 = Tanh(V1)
  V5 = Tanh(V2)
  V4 = Tanh(V5)
  V2 = Tanh(V4)
  V5 = Tanh(V2)
  V0 = VecSub(V0, V5)

train objective -2.2065  diverged 0.000  max_state 0.320
test opt train-distribution: objective -2.1529  diverged 0.000  max_state 0.316
test opt kappa1000: objective -1.4477  diverged 0.000  max_state 0.318
test opt d32: objective -1.8831  diverged 0.000  max_state 0.325
test opt d8: objective -2.2144  diverged 0.000  max_state 0.327
test opt sigma0.3: objective -1.0394  diverged 0.000  max_state 0.325
test opt T200: objective -2.8413  diverged 0.000  max_state 0.324
test opt scale10/0.1: objective -0.6792  diverged 0.000  max_state 0.329
```

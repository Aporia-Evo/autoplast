# Search seed 902

task: opt (testbed 2)  alphabet: 21 ops, with VecRecip, VecSqrt  readout: fixed o = S q  add-node mutation: on  candidates: 300020  real evaluations (after cache): 218083  time: 725s  pop: 500  tournament: 10

commit: dce11aa  task seed: 902  train episodes: 128  persistent registers: 1 matrix, 2 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 6644 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)


## Best rule

```
w' = (w - tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(1.598·tanh(tanh(g))))))))))))))))))))))
u2' = tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(1.598·tanh(tanh(g)))))))))))))))))))))
u3' = tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(1.598·tanh(tanh(g)))))))))))))))

Effective program (24 instructions):
  V2 = Tanh(V1)
  V4 = Tanh(V2)
  s1 = 1.5982
  V1 = VecScale(s1, V4)
  V2 = Tanh(V1)
  V5 = Tanh(V2)
  V3 = Tanh(V5)
  V3 = Tanh(V3)
  V1 = Tanh(V3)
  V2 = Tanh(V1)
  V3 = Tanh(V2)
  V1 = Tanh(V3)
  V4 = Tanh(V1)
  V4 = Tanh(V4)
  V5 = Tanh(V4)
  V2 = Tanh(V5)
  V3 = Tanh(V2)
  V5 = Tanh(V3)
  V1 = Tanh(V5)
  V5 = Tanh(V1)
  V2 = Tanh(V5)
  V5 = Tanh(V2)
  V2 = Tanh(V5)
  V0 = VecSub(V0, V2)

train objective -2.3508  diverged 0.000  max_state 0.315
test opt train-distribution: objective -2.2879  diverged 0.000  max_state 0.321
test opt kappa1000: objective -1.3161  diverged 0.000  max_state 0.319
test opt d32: objective -1.9172  diverged 0.000  max_state 0.322
test opt d8: objective -2.4623  diverged 0.000  max_state 0.322
test opt sigma0.3: objective -0.7081  diverged 0.000  max_state 0.321
test opt T200: objective -2.6810  diverged 0.000  max_state 0.321
test opt scale10/0.1: objective -0.7505  diverged 0.000  max_state 0.322
```

# Search seed 916

task: opt (testbed 2)  alphabet: 21 ops, with VecRecip, VecSqrt  readout: fixed o = S q  add-node mutation: on  candidates: 300020  real evaluations (after cache): 142367  time: 393s  pop: 500  tournament: 10

commit: dce11aa  task seed: 916  train episodes: 128  persistent registers: 1 matrix, 2 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)


## Best rule

```
w' = (w - tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(1.653·tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(g))))))))))))))))))))))
u2' = tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(1.653·tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(g)))))))))))))))))))))
u3' = tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(1.653·tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(g)))))))))))))))))))

Effective program (24 instructions):
  V4 = Tanh(V1)
  V5 = Tanh(V4)
  s0 = 1.6527
  V3 = Tanh(V5)
  V1 = Tanh(V3)
  V4 = Tanh(V1)
  V5 = Tanh(V4)
  V3 = Tanh(V5)
  V1 = Tanh(V3)
  V5 = VecScale(s0, V1)
  V2 = Tanh(V5)
  V2 = Tanh(V2)
  V2 = Tanh(V2)
  V2 = Tanh(V2)
  V1 = Tanh(V2)
  V4 = Tanh(V1)
  V1 = Tanh(V4)
  V5 = Tanh(V1)
  V2 = Tanh(V5)
  V5 = Tanh(V2)
  V3 = Tanh(V5)
  V1 = Tanh(V3)
  V2 = Tanh(V1)
  V0 = VecSub(V0, V2)

train objective -2.2697  diverged 0.000  max_state 0.320
test opt train-distribution: objective -2.2660  diverged 0.000  max_state 0.321
test opt kappa1000: objective -1.2836  diverged 0.000  max_state 0.320
test opt d32: objective -1.8869  diverged 0.000  max_state 0.322
test opt d8: objective -2.4635  diverged 0.000  max_state 0.321
test opt sigma0.3: objective -0.6453  diverged 0.000  max_state 0.321
test opt T200: objective -2.6451  diverged 0.000  max_state 0.321
test opt scale10/0.1: objective -0.7036  diverged 0.000  max_state 0.322
```

# Search seed 905

task: opt (testbed 2)  alphabet: 21 ops, with VecRecip, VecSqrt  readout: fixed o = S q  add-node mutation: on  candidates: 300020  real evaluations (after cache): 222355  time: 656s  pop: 500  tournament: 10

commit: dce11aa  task seed: 905  train episodes: 128  persistent registers: 1 matrix, 2 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1268 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)


## Best rule

```
w' = (w - tanh(tanh(σ(-0.201·-1.460)·tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh((tanh(tanh(tanh(g))) + tanh(u3))))))))))))))))
u2' = tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh((tanh(tanh(tanh(g))) + tanh(u3))))))))))))
u3' = σ(-0.201·-1.460)·tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh((tanh(tanh(tanh(g))) + tanh(u3)))))))))))))

Effective program (24 instructions):
  V5 = Tanh(V1)
  V2 = Tanh(V5)
  V4 = Tanh(V2)
  s0 = -1.4597
  s2 = -0.2011
  V5 = Tanh(V3)
  V5 = VecAdd(V4, V5)
  V2 = Tanh(V5)
  V1 = Tanh(V2)
  V2 = Tanh(V1)
  V4 = Tanh(V2)
  V4 = Tanh(V4)
  V5 = Tanh(V4)
  V4 = Tanh(V5)
  V4 = Tanh(V4)
  s0 = SMul(s2, s0)
  s2 = Sigmoid(s0)
  V1 = Tanh(V4)
  V2 = Tanh(V1)
  V5 = Tanh(V2)
  V3 = VecScale(s2, V5)
  V5 = Tanh(V3)
  V1 = Tanh(V5)
  V0 = VecSub(V0, V1)

train objective -2.6318  diverged 0.000  max_state 0.330
test opt train-distribution: objective -2.6468  diverged 0.000  max_state 0.322
test opt kappa1000: objective -1.4834  diverged 0.000  max_state 0.333
test opt d32: objective -2.3887  diverged 0.000  max_state 0.331
test opt d8: objective -2.6997  diverged 0.000  max_state 0.337
test opt sigma0.3: objective -1.0333  diverged 0.000  max_state 0.332
test opt T200: objective -2.9239  diverged 0.000  max_state 0.327
test opt scale10/0.1: objective -0.9701  diverged 0.000  max_state 0.347
```

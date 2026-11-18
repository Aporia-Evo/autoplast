# Search seed 32

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 718260  time: 2686s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 750068 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1012 candidates
* decayed linear attention: 1396 candidates
* linear attention: 7924 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 7924 candidates
- delta rule (beta=1) (acc 0.578): 505332 candidates
- delta rule (beta=0.5) (acc 0.617): 506740 candidates
- gated delta (alpha=0.9) (acc 0.519): 433652 candidates

## Best rule

```
S' = (1.402·(0.245·(S + S) - 0.245·(0.245·(S + S))((tanh((k + k)))⊗(tanh((k + k))))) + (((v)⊗((k + k)) + P1) - 0.245·(0.245·(S + S))((tanh((k + k)))⊗(tanh((k + k))))))
P1' = (((v)⊗((k + k)) + P1) - 0.245·(0.245·(S + S))((tanh((k + k)))⊗(tanh((k + k)))))
P2' = (tanh((k + k)))⊗(tanh((k + k)))

Effective program (15 instructions):
  s1 = 0.2452
  V0 = VecAdd(V0, V0)
  M2 = MatAdd(M0, M0)
  M3 = MatScale(s1, M2)
  V3 = Tanh(V0)
  M2 = Outer(V3, V3)
  M0 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)
  M1 = MatMul(M3, M2)
  s0 = 1.4024
  M1 = MatScale(s1, M1)
  M3 = MatSub(M3, M1)
  M1 = MatSub(M0, M1)
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M3, M1)

structure: unclassified  [a=1.046 b=2.015 c=-0.724 g=-0.001, erase c/a=0.693, R²=0.7898, 1408 steps]

train acc 0.668 ±0.013
test regime collision3: acc 0.686  margin 0.078  ±0.006
test d16 T12 ow0.3: acc 0.931  margin 0.267  ±0.004
test d16 T12 ow0.0: acc 0.891  margin 0.231  ±0.004
test d16 T12 ow0.6: acc 0.927  margin 0.253  ±0.005
test d32 T24 ow0.3: acc 0.950  margin 0.342  ±0.003
test d8 T6 ow0.3: acc 0.688  margin 0.060  ±0.010
test d16 T64 K8 ow0.3: acc 0.859  margin 0.204  ±0.008
test d16 T128 K8 ow0.3: acc 0.875  margin 0.202  ±0.010
```

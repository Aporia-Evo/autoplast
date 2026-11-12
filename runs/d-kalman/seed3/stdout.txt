# Search seed 3

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 734403  time: 5081s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* linear, not error-correcting: 1268 candidates
* decayed linear attention: 1524 candidates
* linear attention: 8564 candidates
* delta rule: 340212 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8564 candidates
- delta rule (beta=1) (acc 0.578): 335860 candidates
- delta rule (beta=0.5) (acc 0.617): 339828 candidates
- gated delta (alpha=0.9) (acc 0.519): 335348 candidates

## Best rule

```
S' = ((S + (norm(tanh(v)))⊗(k)) - 0.153·((S + (norm(tanh(v)))⊗(k)))((((k + k))⊗(tanh((k + k))) - (P2)(((k + k))⊗(tanh((k + k)))))))
P1' = (((k + k))⊗(tanh((k + k))) - (P2)(((k + k))⊗(tanh((k + k)))))
P2' = ((tanh(v))⊗(k))((tanh(v))⊗(k))

Effective program (15 instructions):
  V4 = VecAdd(V0, V0)
  V5 = Tanh(V4)
  M1 = Outer(V4, V5)
  M2 = MatMul(M2, M1)
  V5 = Tanh(V1)
  M1 = MatSub(M1, M2)
  V3 = Normalize(V5)
  M2 = Outer(V3, V0)
  M0 = MatAdd(M0, M2)
  M2 = MatMul(M0, M1)
  s0 = 0.1526
  M2 = MatScale(s0, M2)
  M0 = MatSub(M0, M2)
  M2 = Outer(V5, V0)
  M2 = MatMul(M2, M2)

structure: unclassified  [a=1.002 b=0.518 c=-0.497 g=-0.013, erase c/a=0.496, R²=0.9609, 1408 steps]

train acc 0.631 ±0.014
test regime collision3: acc 0.639  margin 0.049  ±0.006
test d16 T12 ow0.3: acc 0.911  margin 0.254  ±0.004
test d16 T12 ow0.0: acc 0.906  margin 0.240  ±0.004
test d16 T12 ow0.6: acc 0.923  margin 0.252  ±0.005
test d32 T24 ow0.3: acc 0.978  margin 0.351  ±0.002
test d8 T6 ow0.3: acc 0.763  margin 0.097  ±0.009
test d16 T64 K8 ow0.3: acc 0.827  margin 0.156  ±0.008
test d16 T128 K8 ow0.3: acc 0.818  margin 0.149  ±0.012
```

# Search seed 11

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 291008  time: 4283s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 28916 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = tanh(tanh(tanh(tanh((tanh(tanh(tanh(tanh(S)))) + (v)⊗(k))))))
o = S·q

Effective program (10 instructions):
  M0 = MatTanh(M0)
  M2 = MatTanh(M0)
  M2 = MatTanh(M2)
  M3 = MatTanh(M2)
  M0 = Outer(V1, V0)
  M0 = MatAdd(M3, M0)
  M3 = MatTanh(M0)
  M1 = MatTanh(M3)
  M2 = MatTanh(M1)
  M0 = MatTanh(M2)

train acc 0.510
test regime collision3: acc 0.521  margin -0.024
test d16 T12 ow0.3: acc 0.783  margin 0.148
test d16 T12 ow0.0: acc 0.810  margin 0.160
test d16 T12 ow0.6: acc 0.717  margin 0.107
test d32 T24 ow0.3: acc 0.873  margin 0.224
test d8 T6 ow0.3: acc 0.640  margin 0.033
test d16 T64 K8 ow0.3: acc 0.584  margin -0.000
test d16 T128 K8 ow0.3: acc 0.567  margin -0.011
```

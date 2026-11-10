# Search seed 15

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 334074  time: 567s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 26484 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((v)⊗(((tanh(k) + k) + tanh((tanh(k) + k)))) + |tanh(tanh(tanh(v)))|·S)
o = S·q

Effective program (11 instructions):
  V3 = Tanh(V1)
  V3 = Tanh(V3)
  V2 = Tanh(V3)
  V3 = Tanh(V0)
  V0 = VecAdd(V3, V0)
  V5 = Tanh(V0)
  V0 = VecAdd(V0, V5)
  s1 = Norm(V2)
  M3 = Outer(V1, V0)
  M0 = MatScale(s1, M0)
  M0 = MatAdd(M3, M0)

train acc 0.512
test regime collision3: acc 0.516  margin -0.044
test d16 T12 ow0.3: acc 0.729  margin 0.124
test d16 T12 ow0.0: acc 0.703  margin 0.103
test d16 T12 ow0.6: acc 0.719  margin 0.110
test d32 T24 ow0.3: acc 0.796  margin 0.193
test d8 T6 ow0.3: acc 0.633  margin 0.020
test d16 T64 K8 ow0.3: acc 0.581  margin -0.012
test d16 T128 K8 ow0.3: acc 0.551  margin -0.030
```

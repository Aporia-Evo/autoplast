# Search seed 3

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 381693  time: 1755s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 384628 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 472180 candidates

## Best rule

```
S' = tanh(((v)⊗((k + k)) + tanh(tanh(S))))
o = (max(S·q, tanh(S·q)) - (tanh(relu(tanh(S·q))) ⊙ tanh(relu(tanh(S·q)))))

Effective program (6 instructions):
  M0 = MatTanh(M0)
  V3 = VecAdd(V0, V0)
  M1 = Outer(V1, V3)
  M0 = MatTanh(M0)
  M0 = MatAdd(M1, M0)
  M0 = MatTanh(M0)

train acc 0.520
test regime collision3: acc 0.515  margin -0.039
test d16 T12 ow0.3: acc 0.753  margin 0.128
test d16 T12 ow0.0: acc 0.749  margin 0.122
test d16 T12 ow0.6: acc 0.727  margin 0.106
test d32 T24 ow0.3: acc 0.848  margin 0.208
test d8 T6 ow0.3: acc 0.616  margin 0.015
test d16 T64 K8 ow0.3: acc 0.581  margin -0.011
test d16 T128 K8 ow0.3: acc 0.556  margin -0.020
```

# Search seed 14

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 352500  time: 1721s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 240628 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 522740 candidates

## Best rule

```
S' = (((v + v))⊗(k) - (0 - tanh(tanh(S))))
o = (S·q - (tanh(S·S·q) ⊙ max(0, norm(S·q))))

Effective program (6 instructions):
  V1 = VecAdd(V1, V1)
  M0 = MatTanh(M0)
  M3 = MatTanh(M0)
  M3 = MatSub(M2, M3)
  M0 = Outer(V1, V0)
  M0 = MatSub(M0, M3)

train acc 0.520
test regime collision3: acc 0.514  margin -0.031
test d16 T12 ow0.3: acc 0.767  margin 0.139
test d16 T12 ow0.0: acc 0.795  margin 0.148
test d16 T12 ow0.6: acc 0.711  margin 0.102
test d32 T24 ow0.3: acc 0.870  margin 0.220
test d8 T6 ow0.3: acc 0.610  margin 0.016
test d16 T64 K8 ow0.3: acc 0.573  margin -0.006
test d16 T128 K8 ow0.3: acc 0.562  margin -0.017
```

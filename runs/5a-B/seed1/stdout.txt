# Search seed 1

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 211965  time: 1144s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 86900 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = tanh(tanh(0.947·((v)⊗(k) - (0 - S))))
o = S·q

Effective program (7 instructions):
  M3 = MatSub(M1, M0)
  M0 = Outer(V1, V0)
  M0 = MatSub(M0, M3)
  s3 = 0.9465
  M0 = MatScale(s3, M0)
  M2 = MatTanh(M0)
  M0 = MatTanh(M2)

train acc 0.514
test regime collision3: acc 0.524  margin -0.022
test d16 T12 ow0.3: acc 0.790  margin 0.152
test d16 T12 ow0.0: acc 0.823  margin 0.169
test d16 T12 ow0.6: acc 0.710  margin 0.101
test d32 T24 ow0.3: acc 0.827  margin 0.210
test d8 T6 ow0.3: acc 0.649  margin 0.043
test d16 T64 K8 ow0.3: acc 0.568  margin -0.004
test d16 T128 K8 ow0.3: acc 0.557  margin -0.018
```

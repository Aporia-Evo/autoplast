# Search seed 4

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 366362  time: 664s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 92916 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = |tanh(tanh(tanh(v)))|·(((tanh(0.735·k))⊗(v) + (S)ᵀ))ᵀ
o = S·q

Effective program (12 instructions):
  V3 = Tanh(V1)
  V5 = Tanh(V3)
  s3 = 0.7348
  V3 = VecScale(s3, V0)
  V0 = Tanh(V3)
  V4 = Tanh(V5)
  M1 = Outer(V0, V1)
  s3 = Norm(V4)
  M3 = Transpose(M0)
  M2 = MatAdd(M1, M3)
  M1 = Transpose(M2)
  M0 = MatScale(s3, M1)

train acc 0.512
test regime collision3: acc 0.517  margin -0.043
test d16 T12 ow0.3: acc 0.728  margin 0.124
test d16 T12 ow0.0: acc 0.704  margin 0.105
test d16 T12 ow0.6: acc 0.722  margin 0.111
test d32 T24 ow0.3: acc 0.796  margin 0.194
test d8 T6 ow0.3: acc 0.634  margin 0.021
test d16 T64 K8 ow0.3: acc 0.583  margin -0.011
test d16 T128 K8 ow0.3: acc 0.555  margin -0.028
```

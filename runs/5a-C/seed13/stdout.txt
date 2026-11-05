# Search seed 13

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 270706  time: 416s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 41332 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((v)⊗(tanh(0.838·tanh(tanh(k)))) + 0.873·S)
o = S·q

Effective program (9 instructions):
  s3 = 0.8726
  M0 = MatScale(s3, M0)
  V5 = Tanh(V0)
  s3 = 0.8381
  V4 = Tanh(V5)
  V5 = VecScale(s3, V4)
  V0 = Tanh(V5)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M1, M0)

train acc 0.511
test regime collision3: acc 0.515  margin -0.044
test d16 T12 ow0.3: acc 0.732  margin 0.125
test d16 T12 ow0.0: acc 0.706  margin 0.106
test d16 T12 ow0.6: acc 0.724  margin 0.112
test d32 T24 ow0.3: acc 0.623  margin 0.089
test d8 T6 ow0.3: acc 0.639  margin 0.032
test d16 T64 K8 ow0.3: acc 0.581  margin -0.011
test d16 T128 K8 ow0.3: acc 0.547  margin -0.031
```

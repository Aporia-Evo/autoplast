# Search seed 6

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 521740  time: 764s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 77172 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((v)⊗(tanh(1.192·k)) + |tanh(tanh(tanh(v)))|·S)

Effective program (10 instructions):
  s3 = 1.1916
  V0 = VecScale(s3, V0)
  V4 = Tanh(V0)
  V3 = Tanh(V1)
  V0 = Tanh(V3)
  M2 = Outer(V1, V4)
  V1 = Tanh(V0)
  s2 = Norm(V1)
  M1 = MatScale(s2, M0)
  M0 = MatAdd(M2, M1)

train acc 0.511
test regime collision3: acc 0.517  margin -0.044
test d16 T12 ow0.3: acc 0.729  margin 0.124
test d16 T12 ow0.0: acc 0.703  margin 0.104
test d16 T12 ow0.6: acc 0.720  margin 0.110
test d32 T24 ow0.3: acc 0.795  margin 0.193
test d8 T6 ow0.3: acc 0.633  margin 0.020
test d16 T64 K8 ow0.3: acc 0.578  margin -0.012
test d16 T128 K8 ow0.3: acc 0.551  margin -0.030
```

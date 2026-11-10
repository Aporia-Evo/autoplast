# Search seed 2

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 300020  real evaluations (after cache): 109940  time: 260s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 21876 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((v)⊗(k) - |tanh(tanh((tanh(k) + (tanh(k) ⊙ v))))|·(0 - S))

Effective program (10 instructions):
  M3 = MatSub(M1, M0)
  V4 = Tanh(V0)
  V5 = Hadamard(V4, V1)
  M0 = Outer(V1, V0)
  V3 = VecAdd(V4, V5)
  V5 = Tanh(V3)
  V4 = Tanh(V5)
  s2 = Norm(V4)
  M3 = MatScale(s2, M3)
  M0 = MatSub(M0, M3)

train acc 0.510
test regime collision3: acc 0.517  margin -0.038
test d16 T12 ow0.3: acc 0.746  margin 0.131
test d16 T12 ow0.0: acc 0.732  margin 0.119
test d16 T12 ow0.6: acc 0.714  margin 0.104
test d32 T24 ow0.3: acc 0.806  margin 0.197
test d8 T6 ow0.3: acc 0.642  margin 0.025
test d16 T64 K8 ow0.3: acc 0.578  margin -0.013
test d16 T128 K8 ow0.3: acc 0.541  margin -0.031
```

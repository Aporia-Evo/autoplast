# Search seed 11

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 371830  time: 613s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 16884 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((v)⊗(norm((tanh(k) + tanh((k + tanh(k)))))) + σ(<tanh(tanh(tanh((k + tanh(k))))), tanh(tanh((k + tanh(k))))>)·S)
o = S·q

Effective program (12 instructions):
  V5 = Tanh(V0)
  V0 = VecAdd(V0, V5)
  V2 = Tanh(V0)
  V4 = Tanh(V2)
  V5 = VecAdd(V5, V2)
  V0 = Normalize(V5)
  M1 = Outer(V1, V0)
  V2 = Tanh(V4)
  s2 = Dot(V2, V4)
  s2 = Sigmoid(s2)
  M0 = MatScale(s2, M0)
  M0 = MatAdd(M1, M0)

train acc 0.509
test regime collision3: acc 0.517  margin -0.035
test d16 T12 ow0.3: acc 0.747  margin 0.135
test d16 T12 ow0.0: acc 0.735  margin 0.121
test d16 T12 ow0.6: acc 0.722  margin 0.108
test d32 T24 ow0.3: acc 0.813  margin 0.203
test d8 T6 ow0.3: acc 0.634  margin 0.022
test d16 T64 K8 ow0.3: acc 0.576  margin -0.008
test d16 T128 K8 ow0.3: acc 0.556  margin -0.026
```

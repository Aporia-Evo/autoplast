# Search seed 8

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 433958  time: 744s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 163188 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = (|tanh(tanh(tanh(k)))|·S + (norm(tanh(v)))⊗(tanh((norm(tanh(tanh(k))) + tanh(tanh(k))))))
o = tanh(tanh(norm(S·q)))

Effective program (12 instructions):
  V3 = Tanh(V1)
  V4 = Normalize(V3)
  V3 = Tanh(V0)
  V3 = Tanh(V3)
  V0 = Normalize(V3)
  V1 = VecAdd(V0, V3)
  V0 = Tanh(V1)
  M3 = Outer(V4, V0)
  V2 = Tanh(V3)
  s0 = Norm(V2)
  M0 = MatScale(s0, M0)
  M0 = MatAdd(M0, M3)

train acc 0.509
test regime collision3: acc 0.517  margin -0.040
test d16 T12 ow0.3: acc 0.736  margin 0.128
test d16 T12 ow0.0: acc 0.706  margin 0.102
test d16 T12 ow0.6: acc 0.721  margin 0.109
test d32 T24 ow0.3: acc 0.798  margin 0.194
test d8 T6 ow0.3: acc 0.625  margin 0.016
test d16 T64 K8 ow0.3: acc 0.577  margin -0.014
test d16 T128 K8 ow0.3: acc 0.540  margin -0.034
```

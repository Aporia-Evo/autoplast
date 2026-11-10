# Search seed 12

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 348304  time: 535s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 164980 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((v)⊗(tanh(tanh(tanh(k)))) + σ((σ(σ(1.210)) + 1.210))·(S + 0))
o = S·q

Effective program (12 instructions):
  V5 = Tanh(V0)
  s1 = 1.2098
  V5 = Tanh(V5)
  s3 = Sigmoid(s1)
  s0 = Sigmoid(s3)
  M2 = MatAdd(M0, M1)
  V4 = Tanh(V5)
  M0 = Outer(V1, V4)
  s2 = SAdd(s0, s1)
  s2 = Sigmoid(s2)
  M3 = MatScale(s2, M2)
  M0 = MatAdd(M0, M3)

train acc 0.510
test regime collision3: acc 0.514  margin -0.047
test d16 T12 ow0.3: acc 0.727  margin 0.122
test d16 T12 ow0.0: acc 0.700  margin 0.100
test d16 T12 ow0.6: acc 0.726  margin 0.112
test d32 T24 ow0.3: acc 0.615  margin 0.081
test d8 T6 ow0.3: acc 0.636  margin 0.031
test d16 T64 K8 ow0.3: acc 0.580  margin -0.013
test d16 T128 K8 ow0.3: acc 0.547  margin -0.033
```

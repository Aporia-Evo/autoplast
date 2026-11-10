# Search seed 3

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 291286  time: 414s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 26868 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 1270004 candidates

## Best rule

```
S' = <((tanh(k) - norm(tanh(tanh(k)))) - v), ((tanh(k) - norm(tanh(tanh(k)))) - v)>·(σ(1.373·1.373)·S + (v)⊗(tanh(tanh(k))))
o = S·q

Effective program (13 instructions):
  V4 = Tanh(V0)
  V0 = Tanh(V4)
  s0 = 1.3725
  s0 = SMul(s0, s0)
  s0 = Sigmoid(s0)
  M0 = MatScale(s0, M0)
  M3 = Outer(V1, V0)
  V0 = Normalize(V0)
  V3 = VecSub(V4, V0)
  M0 = MatAdd(M0, M3)
  V0 = VecSub(V3, V1)
  s3 = Dot(V0, V0)
  M0 = MatScale(s3, M0)

train acc 0.515
test regime collision3: acc 0.512  margin -0.045
test d16 T12 ow0.3: acc 0.730  margin 0.123
test d16 T12 ow0.0: acc 0.705  margin 0.103
test d16 T12 ow0.6: acc 0.726  margin 0.113
test d32 T24 ow0.3: acc 0.615  margin 0.081
test d8 T6 ow0.3: acc 0.642  margin 0.032
test d16 T64 K8 ow0.3: acc 0.580  margin -0.012
test d16 T128 K8 ow0.3: acc 0.545  margin -0.032
```

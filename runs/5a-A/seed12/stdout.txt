# Search seed 12

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 553379  time: 713s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 18036 candidates
- delta rule (beta=1) (acc 0.578): 35828 candidates
- delta rule (beta=0.5) (acc 0.617): 43764 candidates
- gated delta (alpha=0.9) (acc 0.519): 35828 candidates

## Best rule

```
S' = (S + ((tanh(v) - tanh(tanh(<S·k, S·k>·0.403·S·k))))⊗(k))

Effective program (11 instructions):
  s2 = 0.4030
  V4 = MatVec(M0, V0)
  s1 = Dot(V4, V4)
  s3 = SMul(s1, s2)
  V5 = VecScale(s3, V4)
  V3 = Tanh(V1)
  V5 = Tanh(V5)
  V2 = Tanh(V5)
  V1 = VecSub(V3, V2)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)

train acc 0.630
test regime collision3: acc 0.648  margin 0.051
test d16 T12 ow0.3: acc 0.938  margin 0.243
test d16 T12 ow0.0: acc 0.933  margin 0.226
test d16 T12 ow0.6: acc 0.943  margin 0.245
test d32 T24 ow0.3: acc 0.991  margin 0.331
test d8 T6 ow0.3: acc 0.771  margin 0.096
test d16 T64 K8 ow0.3: acc 0.827  margin 0.155
test d16 T128 K8 ow0.3: acc 0.805  margin 0.149
```

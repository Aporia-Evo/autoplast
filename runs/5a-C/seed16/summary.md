# Search seed 16

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 392698  time: 785s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 22132 candidates
- delta rule (beta=1) (acc 0.578): 256244 candidates
- delta rule (beta=0.5) (acc 0.617): 260980 candidates
- gated delta (alpha=0.9) (acc 0.519): 255348 candidates

## Best rule

```
S' = ((S - 0) + <tanh(tanh(tanh(tanh(k)))), tanh(tanh(tanh(tanh(k))))>·((v - (S - 0)·tanh(tanh(tanh(tanh(k))))))⊗(tanh(tanh(tanh(tanh(tanh(tanh(k))))))))
o = S·q

Effective program (13 instructions):
  V0 = Tanh(V0)
  M2 = MatSub(M0, M3)
  V0 = Tanh(V0)
  V5 = Tanh(V0)
  V4 = Tanh(V5)
  V0 = Tanh(V4)
  V5 = MatVec(M2, V4)
  V1 = VecSub(V1, V5)
  V3 = Tanh(V0)
  M0 = Outer(V1, V3)
  s0 = Dot(V4, V4)
  M1 = MatScale(s0, M0)
  M0 = MatAdd(M2, M1)

train acc 0.625
test regime collision3: acc 0.638  margin 0.045
test d16 T12 ow0.3: acc 0.917  margin 0.255
test d16 T12 ow0.0: acc 0.882  margin 0.226
test d16 T12 ow0.6: acc 0.924  margin 0.254
test d32 T24 ow0.3: acc 0.978  margin 0.361
test d8 T6 ow0.3: acc 0.715  margin 0.074
test d16 T64 K8 ow0.3: acc 0.821  margin 0.155
test d16 T128 K8 ow0.3: acc 0.794  margin 0.135
```

# Search seed 7

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 780278  time: 1889s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 15348 candidates
- delta rule (beta=1) (acc 0.853): 19956 candidates
- delta rule (beta=0.5) (acc 0.901): 20852 candidates
- gated delta (alpha=0.9) (acc 0.713): 19956 candidates

## Best rule

```
S' = ((S - 0) + 1.175·(((0.565·tanh(σ(0)·k) ⊙ v) + (v - (S - 0)·tanh(σ(0)·k))))⊗(tanh(k)))

Effective program (15 instructions):
  M3 = MatSub(M0, M3)
  s2 = Sigmoid(s1)
  V4 = VecScale(s2, V0)
  V2 = Tanh(V4)
  s0 = 0.5646
  V3 = MatVec(M3, V2)
  V4 = VecScale(s0, V2)
  V5 = Hadamard(V4, V1)
  V3 = VecSub(V1, V3)
  s2 = 1.1751
  V4 = Tanh(V0)
  V1 = VecAdd(V5, V3)
  M0 = Outer(V1, V4)
  M0 = MatScale(s2, M0)
  M0 = MatAdd(M3, M0)

train acc 0.911
test d16 T12 ow0.3: acc 0.924  margin 0.266
test d16 T12 ow0.0: acc 0.889  margin 0.234
test d16 T12 ow0.6: acc 0.940  margin 0.275
test d32 T24 ow0.3: acc 0.984  margin 0.357
test d8 T6 ow0.3: acc 0.789  margin 0.111
test d16 T64 K8 ow0.3: acc 0.851  margin 0.179
test d16 T128 K8 ow0.3: acc 0.850  margin 0.173
```

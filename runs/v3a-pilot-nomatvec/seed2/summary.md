# Search seed 2

task: v3  alphabet: 18 ops, without MatVec  add-node mutation: on  candidates: 300020  real evaluations (after cache): 126239  time: 538s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 13684 candidates
- delta rule (beta=1) (acc 0.853): 78836 candidates
- delta rule (beta=0.5) (acc 0.901): 80628 candidates
- gated delta (alpha=0.9) (acc 0.713): 78836 candidates

## Best rule

```
S' = ((tanh(0.365·tanh(v)))⊗((k - 0)) - (σ(0.365)·(S)(((k - 0))⊗((k - 0))) - S))

Effective program (12 instructions):
  V3 = VecSub(V0, V5)
  s1 = 0.3647
  s0 = Sigmoid(s1)
  V0 = Tanh(V1)
  V5 = VecScale(s1, V0)
  V0 = Tanh(V5)
  M2 = Outer(V3, V3)
  M3 = MatMul(M0, M2)
  M3 = MatScale(s0, M3)
  M1 = MatSub(M3, M0)
  M0 = Outer(V0, V3)
  M0 = MatSub(M0, M1)

train acc 0.908
test d16 T12 ow0.3: acc 0.920  margin 0.270
test d16 T12 ow0.0: acc 0.885  margin 0.233
test d16 T12 ow0.6: acc 0.945  margin 0.285
test d32 T24 ow0.3: acc 0.985  margin 0.360
test d8 T6 ow0.3: acc 0.792  margin 0.115
test d16 T64 K8 ow0.3: acc 0.852  margin 0.193
test d16 T128 K8 ow0.3: acc 0.854  margin 0.189
```

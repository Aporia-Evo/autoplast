# Search seed 16

task: v3  alphabet: 18 ops, without MatVec  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 556581  time: 1664s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 97652 candidates
- delta rule (beta=1) (acc 0.853): 382964 candidates
- delta rule (beta=0.5) (acc 0.901): 384372 candidates
- gated delta (alpha=0.9) (acc 0.713): 138868 candidates

## Best rule

```
S' = ((tanh(v))⊗(norm(tanh(k))) + (S - (0.674·S)((tanh(k))⊗(tanh(k)))))

Effective program (10 instructions):
  V1 = Tanh(V1)
  V0 = Tanh(V0)
  M1 = Outer(V0, V0)
  s0 = 0.6743
  V0 = Normalize(V0)
  M3 = MatScale(s0, M0)
  M1 = MatMul(M3, M1)
  M3 = MatSub(M0, M1)
  M0 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)

train acc 0.908
test d16 T12 ow0.3: acc 0.917  margin 0.271
test d16 T12 ow0.0: acc 0.882  margin 0.232
test d16 T12 ow0.6: acc 0.943  margin 0.288
test d32 T24 ow0.3: acc 0.983  margin 0.363
test d8 T6 ow0.3: acc 0.788  margin 0.114
test d16 T64 K8 ow0.3: acc 0.856  margin 0.199
test d16 T128 K8 ow0.3: acc 0.857  margin 0.194
```

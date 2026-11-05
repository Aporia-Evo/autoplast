# Search seed 15

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 322192  time: 1835s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 10740 candidates
- delta rule (beta=1) (acc 0.853): 947956 candidates
- delta rule (beta=0.5) (acc 0.901): 948596 candidates
- gated delta (alpha=0.9) (acc 0.713): 127476 candidates

## Best rule

```
S' = ((S + (v)⊗(k)) - (((S + (v)⊗(k)))((σ(1.166)·(v)⊗(k))ᵀ))(σ(1.166)·(v)⊗(k)))

Effective program (9 instructions):
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  s1 = 1.1657
  s3 = Sigmoid(s1)
  M3 = MatScale(s3, M3)
  M1 = Transpose(M3)
  M2 = MatMul(M0, M1)
  M3 = MatMul(M2, M3)
  M0 = MatSub(M0, M3)

train acc 0.905
test d16 T12 ow0.3: acc 0.920  margin 0.269
test d16 T12 ow0.0: acc 0.886  margin 0.234
test d16 T12 ow0.6: acc 0.944  margin 0.284
test d32 T24 ow0.3: acc 0.984  margin 0.359
test d8 T6 ow0.3: acc 0.796  margin 0.116
test d16 T64 K8 ow0.3: acc 0.854  margin 0.191
test d16 T128 K8 ow0.3: acc 0.851  margin 0.187
```

# Search seed 16

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 249048  time: 924s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 6644 candidates
- delta rule (beta=1) (acc 0.853): 1361396 candidates
- delta rule (beta=0.5) (acc 0.901): 1362804 candidates
- gated delta (alpha=0.9) (acc 0.713): 74100 candidates

## Best rule

```
S' = (1.015·((S + (v)⊗(k)) + (v)⊗(k)) - ((S - (0.679·(v)⊗(k))ᵀ))(((0.679·(v)⊗(k))ᵀ)((v)⊗(k))))

Effective program (12 instructions):
  M2 = Outer(V1, V0)
  s2 = 0.6788
  M3 = MatScale(s2, M2)
  M3 = Transpose(M3)
  M1 = MatMul(M3, M2)
  M3 = MatSub(M0, M3)
  M1 = MatMul(M3, M1)
  s0 = 1.0154
  M3 = MatAdd(M0, M2)
  M2 = MatAdd(M3, M2)
  M0 = MatScale(s0, M2)
  M0 = MatSub(M0, M1)

train acc 0.908
test d16 T12 ow0.3: acc 0.927  margin 0.281
test d16 T12 ow0.0: acc 0.889  margin 0.241
test d16 T12 ow0.6: acc 0.951  margin 0.300
test d32 T24 ow0.3: acc 0.990  margin 0.380
test d8 T6 ow0.3: acc 0.800  margin 0.118
test d16 T64 K8 ow0.3: acc 0.841  margin 0.191
test d16 T128 K8 ow0.3: acc 0.812  margin 0.171
```

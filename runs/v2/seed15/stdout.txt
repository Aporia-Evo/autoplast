# Search seed 15

add-node mutation: on  candidates: 1500020  real evaluations (after cache): 456625  time: 1624s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 13428 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 13428 candidates

## Best rule

```
S' = 0.954·((S + (norm(tanh(v)))⊗(k)) - (((S + S) + (((norm(tanh(v)))⊗(k))((norm(tanh(v)))⊗(k)))ᵀ))((((norm(tanh(v)))⊗(k))((norm(tanh(v)))⊗(k)))ᵀ))

Effective program (12 instructions):
  V2 = Tanh(V1)
  V2 = Normalize(V2)
  M3 = Outer(V2, V0)
  M2 = MatMul(M3, M3)
  M1 = MatAdd(M0, M0)
  M0 = MatAdd(M0, M3)
  M2 = Transpose(M2)
  M3 = MatAdd(M1, M2)
  M3 = MatMul(M3, M2)
  M0 = MatSub(M0, M3)
  s3 = 0.9536
  M0 = MatScale(s3, M0)

train acc 0.840
test d16 T12 ow0.3: acc 0.808  margin 0.164
test d16 T12 ow0.0: acc 0.852  margin 0.184
test d16 T12 ow0.6: acc 0.723  margin 0.110
test d32 T24 ow0.3: acc 0.871  margin 0.229
test d8 T6 ow0.3: acc 0.668  margin 0.048
```

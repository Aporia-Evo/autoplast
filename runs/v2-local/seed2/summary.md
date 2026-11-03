# Search seed 2

candidates: 1500020  real evaluations (after cache): 401997  time: 1897s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 16756 candidates
- delta rule (beta=1) (acc 0.858): 863924 candidates
- delta rule (beta=0.5) (acc 0.932): 865204 candidates
- gated delta (alpha=0.9) (acc 0.729): 16756 candidates

## Best rule

```
S' = 1.098·(((v)⊗(k) + S) - 1.098·(((v)⊗(k) + S))((((v)⊗(k))ᵀ)(0.661·(v)⊗(k))))

Effective program (11 instructions):
  s1 = 0.6606
  M3 = Outer(V1, V0)
  s3 = 1.0975
  M0 = MatAdd(M3, M0)
  M2 = MatScale(s1, M3)
  M1 = Transpose(M3)
  M3 = MatMul(M1, M2)
  M2 = MatMul(M0, M3)
  M3 = MatScale(s3, M2)
  M3 = MatSub(M0, M3)
  M0 = MatScale(s3, M3)

train acc 0.971
test d16 T12 ow0.3: acc 0.967  margin 0.311
test d16 T12 ow0.0: acc 0.947  margin 0.281
test d16 T12 ow0.6: acc 0.964  margin 0.312
test d32 T24 ow0.3: acc 0.978  margin 0.366
test d8 T6 ow0.3: acc 0.836  margin 0.139
```

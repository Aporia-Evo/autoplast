# Search seed 1

candidates: 3000052  real evaluations (after cache): 878201  time: 986s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.778): 16884 candidates
- delta rule (beta=1) (acc 0.872): not reached
- delta rule (beta=0.5) (acc 0.935): not reached
- gated delta (alpha=0.9) (acc 0.751): 16884 candidates

## Best rule

```
S' = (((v)⊗(k))ᵀ + (2.523·((v)⊗(k) + (v)⊗(k)) + 0.932·S))

Effective program (9 instructions):
  M1 = Outer(V1, V0)
  M3 = MatAdd(M1, M1)
  s3 = 0.9315
  M0 = MatScale(s3, M0)
  s3 = 2.5231
  M3 = MatScale(s3, M3)
  M2 = MatAdd(M3, M0)
  M1 = Transpose(M1)
  M0 = MatAdd(M1, M2)

train acc 0.848
test d16 T12 ow0.3: acc 0.782  margin 0.145
test d16 T12 ow0.0: acc 0.832  margin 0.169
test d16 T12 ow0.6: acc 0.670  margin 0.081
test d32 T24 ow0.3: acc 0.806  margin 0.198
test d8 T6 ow0.3: acc 0.622  margin 0.028
```

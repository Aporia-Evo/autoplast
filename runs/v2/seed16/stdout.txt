# Search seed 16

add-node mutation: on  candidates: 1500020  real evaluations (after cache): 643482  time: 386s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 6644 candidates
- delta rule (beta=1) (acc 0.858): 14068 candidates
- delta rule (beta=0.5) (acc 0.932): 14836 candidates
- gated delta (alpha=0.9) (acc 0.729): 6644 candidates

## Best rule

```
S' = (0.492 + 0.616)·(S + ((v - S·((k ⊙ (v ⊙ v)) + k)))⊗(0.616·((k ⊙ (v ⊙ v)) + k)))

Effective program (12 instructions):
  V4 = Hadamard(V1, V1)
  s2 = 0.4924
  s3 = 0.6159
  V2 = Hadamard(V0, V4)
  V4 = VecAdd(V2, V0)
  V3 = MatVec(M0, V4)
  V5 = VecSub(V1, V3)
  V0 = VecScale(s3, V4)
  s0 = SAdd(s2, s3)
  M2 = Outer(V5, V0)
  M0 = MatAdd(M0, M2)
  M0 = MatScale(s0, M0)

train acc 0.972
test d16 T12 ow0.3: acc 0.967  margin 0.306
test d16 T12 ow0.0: acc 0.951  margin 0.279
test d16 T12 ow0.6: acc 0.960  margin 0.300
test d32 T24 ow0.3: acc 0.942  margin 0.319
test d8 T6 ow0.3: acc 0.826  margin 0.133
```

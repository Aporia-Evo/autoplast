# Search seed 13

add-node mutation: off  candidates: 1500020  real evaluations (after cache): 577754  time: 484s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 8564 candidates
- delta rule (beta=1) (acc 0.858): 491380 candidates
- delta rule (beta=0.5) (acc 0.932): 494068 candidates
- gated delta (alpha=0.9) (acc 0.729): 8564 candidates

## Best rule

```
S' = 1.100·(((tanh(v))⊗(k) + 0.680·((S - (tanh(v))⊗(k))·tanh((0 - k)))⊗(k)) + (S - (tanh(v))⊗(k)))

Effective program (13 instructions):
  V5 = VecSub(V2, V0)
  V1 = Tanh(V1)
  V5 = Tanh(V5)
  M3 = Outer(V1, V0)
  M0 = MatSub(M0, M3)
  s1 = 0.6803
  V1 = MatVec(M0, V5)
  M1 = Outer(V1, V0)
  M1 = MatScale(s1, M1)
  M3 = MatAdd(M3, M1)
  M0 = MatAdd(M3, M0)
  s3 = 1.1003
  M0 = MatScale(s3, M0)

train acc 0.973
test d16 T12 ow0.3: acc 0.968  margin 0.301
test d16 T12 ow0.0: acc 0.956  margin 0.279
test d16 T12 ow0.6: acc 0.960  margin 0.288
test d32 T24 ow0.3: acc 0.962  margin 0.338
test d8 T6 ow0.3: acc 0.836  margin 0.136
```

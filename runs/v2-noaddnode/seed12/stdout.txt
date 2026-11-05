# Search seed 12

add-node mutation: off  candidates: 1500020  real evaluations (after cache): 343624  time: 232s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 17908 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 17908 candidates

## Best rule

```
S' = ((v)⊗(k) + σ(-0.085)·(S + S))

Effective program (6 instructions):
  s1 = -0.0846
  M2 = Outer(V1, V0)
  s3 = Sigmoid(s1)
  M3 = MatAdd(M0, M0)
  M0 = MatScale(s3, M3)
  M0 = MatAdd(M2, M0)

train acc 0.814
test d16 T12 ow0.3: acc 0.787  margin 0.149
test d16 T12 ow0.0: acc 0.884  margin 0.194
test d16 T12 ow0.6: acc 0.636  margin 0.064
test d32 T24 ow0.3: acc 0.874  margin 0.225
test d8 T6 ow0.3: acc 0.633  margin 0.029
```

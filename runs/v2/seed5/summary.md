# Search seed 5

add-node mutation: on  candidates: 1500020  real evaluations (after cache): 243198  time: 445s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 79988 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 78708 candidates

## Best rule

```
S' = ((v)⊗(k) + 0.958·S)

Effective program (4 instructions):
  s3 = 0.9577
  M3 = Outer(V1, V0)
  M0 = MatScale(s3, M0)
  M0 = MatAdd(M3, M0)

train acc 0.814
test d16 T12 ow0.3: acc 0.787  margin 0.149
test d16 T12 ow0.0: acc 0.884  margin 0.194
test d16 T12 ow0.6: acc 0.636  margin 0.064
test d32 T24 ow0.3: acc 0.874  margin 0.225
test d8 T6 ow0.3: acc 0.633  margin 0.029
```

# Search seed 1

add-node mutation: on  candidates: 1500020  real evaluations (after cache): 351470  time: 509s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 71156 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 71156 candidates

## Best rule

```
S' = ((0.479·S + 0.479·S) - (v)⊗((0 - k)))

Effective program (6 instructions):
  s1 = 0.4789
  V0 = VecSub(V4, V0)
  M2 = MatScale(s1, M0)
  M1 = MatAdd(M2, M2)
  M0 = Outer(V1, V0)
  M0 = MatSub(M1, M0)

train acc 0.814
test d16 T12 ow0.3: acc 0.787  margin 0.149
test d16 T12 ow0.0: acc 0.884  margin 0.194
test d16 T12 ow0.6: acc 0.636  margin 0.064
test d32 T24 ow0.3: acc 0.874  margin 0.225
test d8 T6 ow0.3: acc 0.633  margin 0.029
```

# Search seed 1

add-node mutation: on  candidates: 300020  real evaluations (after cache): 92195  time: 58s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 71156 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 71156 candidates

## Best rule

```
S' = ((0.481·S + 0.481·S) - (v)⊗(((0 - k) - 0)))

Effective program (7 instructions):
  s1 = 0.4807
  V0 = VecSub(V4, V0)
  M2 = MatScale(s1, M0)
  M1 = MatAdd(M2, M2)
  V4 = VecSub(V0, V3)
  M0 = Outer(V1, V4)
  M0 = MatSub(M1, M0)

train acc 0.814
test d16 T12 ow0.3: acc 0.786  margin 0.148
test d16 T12 ow0.0: acc 0.891  margin 0.195
test d16 T12 ow0.6: acc 0.631  margin 0.060
test d32 T24 ow0.3: acc 0.875  margin 0.226
test d8 T6 ow0.3: acc 0.634  margin 0.028
```

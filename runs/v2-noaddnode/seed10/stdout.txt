# Search seed 10

add-node mutation: off  candidates: 1500020  real evaluations (after cache): 222124  time: 162s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 29044 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 29044 candidates

## Best rule

```
S' = 0.958·((v)⊗(k) + S)

Effective program (4 instructions):
  M1 = Outer(V1, V0)
  M0 = MatAdd(M1, M0)
  s1 = 0.9577
  M0 = MatScale(s1, M0)

train acc 0.814
test d16 T12 ow0.3: acc 0.787  margin 0.149
test d16 T12 ow0.0: acc 0.884  margin 0.194
test d16 T12 ow0.6: acc 0.636  margin 0.064
test d32 T24 ow0.3: acc 0.874  margin 0.225
test d8 T6 ow0.3: acc 0.633  margin 0.029
```

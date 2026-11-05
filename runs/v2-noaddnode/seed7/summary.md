# Search seed 7

add-node mutation: off  candidates: 1500020  real evaluations (after cache): 387614  time: 276s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 49524 candidates
- delta rule (beta=1) (acc 0.858): 500340 candidates
- delta rule (beta=0.5) (acc 0.932): 500340 candidates
- gated delta (alpha=0.9) (acc 0.729): 49524 candidates

## Best rule

```
S' = (1.141·S + ((tanh(v) - S·k))⊗(tanh(k)))

Effective program (8 instructions):
  V5 = MatVec(M0, V0)
  V1 = Tanh(V1)
  s1 = 1.1405
  M0 = MatScale(s1, M0)
  V2 = VecSub(V1, V5)
  V0 = Tanh(V0)
  M2 = Outer(V2, V0)
  M0 = MatAdd(M0, M2)

train acc 0.966
test d16 T12 ow0.3: acc 0.962  margin 0.319
test d16 T12 ow0.0: acc 0.939  margin 0.281
test d16 T12 ow0.6: acc 0.957  margin 0.323
test d32 T24 ow0.3: acc 0.932  margin 0.322
test d8 T6 ow0.3: acc 0.842  margin 0.143
```

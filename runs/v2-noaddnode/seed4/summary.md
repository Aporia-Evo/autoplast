# Search seed 4

add-node mutation: off  candidates: 1500020  real evaluations (after cache): 465309  time: 346s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 21620 candidates
- delta rule (beta=1) (acc 0.858): 74484 candidates
- delta rule (beta=0.5) (acc 0.932): 78324 candidates
- gated delta (alpha=0.9) (acc 0.729): 21620 candidates

## Best rule

```
S' = (1.111·S + σ(<S·k, S·k>)·((v - S·k))⊗(k))

Effective program (9 instructions):
  V5 = MatVec(M0, V0)
  s2 = Dot(V5, V5)
  s2 = Sigmoid(s2)
  s3 = 1.1108
  V1 = VecSub(V1, V5)
  M3 = Outer(V1, V0)
  M3 = MatScale(s2, M3)
  M0 = MatScale(s3, M0)
  M0 = MatAdd(M0, M3)

train acc 0.977
test d16 T12 ow0.3: acc 0.971  margin 0.286
test d16 T12 ow0.0: acc 0.962  margin 0.269
test d16 T12 ow0.6: acc 0.964  margin 0.277
test d32 T24 ow0.3: acc 0.991  margin 0.364
test d8 T6 ow0.3: acc 0.826  margin 0.129
```

# Search seed 5

add-node mutation: off  candidates: 1500020  real evaluations (after cache): 535788  time: 447s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 32756 candidates
- delta rule (beta=1) (acc 0.858): 337396 candidates
- delta rule (beta=0.5) (acc 0.932): 337524 candidates
- gated delta (alpha=0.9) (acc 0.729): 32756 candidates

## Best rule

```
S' = (-1.122·(0 - S) + ((v - S·tanh(k)))⊗(tanh(tanh(tanh(tanh(k))))))

Effective program (11 instructions):
  V0 = Tanh(V0)
  V2 = MatVec(M0, V0)
  M2 = MatSub(M1, M0)
  V1 = VecSub(V1, V2)
  V0 = Tanh(V0)
  V0 = Tanh(V0)
  V0 = Tanh(V0)
  M3 = Outer(V1, V0)
  s3 = -1.1223
  M0 = MatScale(s3, M2)
  M0 = MatAdd(M0, M3)

train acc 0.970
test d16 T12 ow0.3: acc 0.967  margin 0.309
test d16 T12 ow0.0: acc 0.951  margin 0.279
test d16 T12 ow0.6: acc 0.963  margin 0.302
test d32 T24 ow0.3: acc 0.959  margin 0.341
test d8 T6 ow0.3: acc 0.830  margin 0.134
```

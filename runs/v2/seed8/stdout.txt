# Search seed 8

add-node mutation: on  candidates: 1500020  real evaluations (after cache): 647410  time: 785s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 6388 candidates
- delta rule (beta=1) (acc 0.858): 44404 candidates
- delta rule (beta=0.5) (acc 0.932): 111476 candidates
- gated delta (alpha=0.9) (acc 0.729): 5748 candidates

## Best rule

```
S' = 1.055·(S - (((S·tanh(k) - norm((v + tanh(S·tanh(k))))) - ((v + tanh(S·tanh(k))) - S·tanh(k))))⊗(k))

Effective program (12 instructions):
  V2 = Tanh(V0)
  V4 = MatVec(M0, V2)
  V2 = Tanh(V4)
  V3 = VecAdd(V1, V2)
  s2 = 1.0555
  V1 = VecSub(V3, V4)
  V3 = Normalize(V3)
  V3 = VecSub(V4, V3)
  V2 = VecSub(V3, V1)
  M3 = Outer(V2, V0)
  M0 = MatSub(M0, M3)
  M0 = MatScale(s2, M0)

train acc 0.969
test d16 T12 ow0.3: acc 0.961  margin 0.290
test d16 T12 ow0.0: acc 0.954  margin 0.263
test d16 T12 ow0.6: acc 0.959  margin 0.290
test d32 T24 ow0.3: acc 0.994  margin 0.371
test d8 T6 ow0.3: acc 0.813  margin 0.125
```

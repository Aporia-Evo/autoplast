# Search seed 16

add-node mutation: off  candidates: 1500020  real evaluations (after cache): 376662  time: 222s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 21876 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 21876 candidates

## Best rule

```
S' = |tanh(v)|·((tanh(norm(tanh(v))))⊗(k) + S)

Effective program (7 instructions):
  V1 = Tanh(V1)
  s0 = Norm(V1)
  V5 = Normalize(V1)
  V1 = Tanh(V5)
  M2 = Outer(V1, V0)
  M0 = MatAdd(M2, M0)
  M0 = MatScale(s0, M0)

train acc 0.817
test d16 T12 ow0.3: acc 0.788  margin 0.149
test d16 T12 ow0.0: acc 0.866  margin 0.185
test d16 T12 ow0.6: acc 0.647  margin 0.069
test d32 T24 ow0.3: acc 0.878  margin 0.226
test d8 T6 ow0.3: acc 0.634  margin 0.033
```

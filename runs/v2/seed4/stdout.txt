# Search seed 4

add-node mutation: on  candidates: 1500020  real evaluations (after cache): 334724  time: 527s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 4724 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 4724 candidates

## Best rule

```
S' = ((tanh(tanh(v)))⊗(k) + |tanh(v)|·S)

Effective program (6 instructions):
  V1 = Tanh(V1)
  V3 = Tanh(V1)
  M3 = Outer(V3, V0)
  s3 = Norm(V1)
  M1 = MatScale(s3, M0)
  M0 = MatAdd(M3, M1)

train acc 0.817
test d16 T12 ow0.3: acc 0.788  margin 0.149
test d16 T12 ow0.0: acc 0.867  margin 0.185
test d16 T12 ow0.6: acc 0.647  margin 0.069
test d32 T24 ow0.3: acc 0.879  margin 0.226
test d8 T6 ow0.3: acc 0.636  margin 0.034
```

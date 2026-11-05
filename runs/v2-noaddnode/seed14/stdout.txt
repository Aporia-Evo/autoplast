# Search seed 14

add-node mutation: off  candidates: 1500020  real evaluations (after cache): 385843  time: 301s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 10100 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 10100 candidates

## Best rule

```
S' = (((v)⊗(k) + (v)⊗(tanh(k))) + <k, tanh(k)>·S)

Effective program (7 instructions):
  M1 = Outer(V1, V0)
  V4 = Tanh(V0)
  s3 = Dot(V0, V4)
  M3 = Outer(V1, V4)
  M0 = MatScale(s3, M0)
  M1 = MatAdd(M1, M3)
  M0 = MatAdd(M1, M0)

train acc 0.812
test d16 T12 ow0.3: acc 0.789  margin 0.150
test d16 T12 ow0.0: acc 0.871  margin 0.188
test d16 T12 ow0.6: acc 0.646  margin 0.072
test d32 T24 ow0.3: acc 0.878  margin 0.225
test d8 T6 ow0.3: acc 0.642  margin 0.035
```

# Search seed 1

add-node mutation: off  candidates: 1500020  real evaluations (after cache): 475699  time: 386s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 18420 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 18420 candidates

## Best rule

```
S' = ((tanh(tanh(v)))⊗(k) - <v, tanh(v)>·(0 - S))

Effective program (7 instructions):
  M2 = MatSub(M2, M0)
  V2 = Tanh(V1)
  s1 = Dot(V1, V2)
  V2 = Tanh(V2)
  M2 = MatScale(s1, M2)
  M1 = Outer(V2, V0)
  M0 = MatSub(M1, M2)

train acc 0.817
test d16 T12 ow0.3: acc 0.789  margin 0.149
test d16 T12 ow0.0: acc 0.865  margin 0.185
test d16 T12 ow0.6: acc 0.648  margin 0.069
test d32 T24 ow0.3: acc 0.878  margin 0.226
test d8 T6 ow0.3: acc 0.637  margin 0.034
```

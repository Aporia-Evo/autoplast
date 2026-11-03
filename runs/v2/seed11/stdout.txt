# Search seed 11

add-node mutation: on  candidates: 1500020  real evaluations (after cache): 593605  time: 2278s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 10484 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 10484 candidates

## Best rule

```
S' = 0.952·(((0 - S))((((tanh(v))⊗(k))(((tanh(v))⊗(k) + (tanh(v))⊗(k))))ᵀ) + ((tanh(v))⊗(k) - (0 - S)))

Effective program (11 instructions):
  M1 = MatSub(M2, M0)
  V4 = Tanh(V1)
  M0 = Outer(V4, V0)
  M3 = MatAdd(M0, M0)
  M3 = MatMul(M0, M3)
  M0 = MatSub(M0, M1)
  M3 = Transpose(M3)
  M1 = MatMul(M1, M3)
  M0 = MatAdd(M1, M0)
  s0 = 0.9523
  M0 = MatScale(s0, M0)

train acc 0.836
test d16 T12 ow0.3: acc 0.809  margin 0.164
test d16 T12 ow0.0: acc 0.856  margin 0.185
test d16 T12 ow0.6: acc 0.723  margin 0.110
test d32 T24 ow0.3: acc 0.868  margin 0.228
test d8 T6 ow0.3: acc 0.680  margin 0.053
```

# Search seed 2

add-node mutation: off  candidates: 1500020  real evaluations (after cache): 674132  time: 921s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 27380 candidates
- delta rule (beta=1) (acc 0.858): 626548 candidates
- delta rule (beta=0.5) (acc 0.932): 627572 candidates
- gated delta (alpha=0.9) (acc 0.729): 27380 candidates

## Best rule

```
S' = (-1.088·σ(|(k ⊙ k)|)·((1.096·S + (tanh(v))⊗(k)))((k)⊗(k)) + (1.096·S + (tanh(v))⊗(k)))

Effective program (14 instructions):
  V1 = Tanh(V1)
  s0 = 1.0956
  M2 = Outer(V1, V0)
  M0 = MatScale(s0, M0)
  M3 = Outer(V0, V0)
  V1 = Hadamard(V0, V0)
  M0 = MatAdd(M0, M2)
  s3 = Norm(V1)
  M1 = MatMul(M0, M3)
  s0 = -1.0879
  s2 = Sigmoid(s3)
  s3 = SMul(s0, s2)
  M3 = MatScale(s3, M1)
  M0 = MatAdd(M3, M0)

train acc 0.975
test d16 T12 ow0.3: acc 0.968  margin 0.301
test d16 T12 ow0.0: acc 0.953  margin 0.279
test d16 T12 ow0.6: acc 0.963  margin 0.292
test d32 T24 ow0.3: acc 0.953  margin 0.330
test d8 T6 ow0.3: acc 0.834  margin 0.137
```

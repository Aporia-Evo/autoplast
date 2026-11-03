# Search seed 12

add-node mutation: on  candidates: 1500020  real evaluations (after cache): 736988  time: 2106s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 19060 candidates
- delta rule (beta=1) (acc 0.858): 41332 candidates
- delta rule (beta=0.5) (acc 0.932): 41588 candidates
- gated delta (alpha=0.9) (acc 0.729): 19060 candidates

## Best rule

```
S' = ((σ(0.179)·S + σ(0.179)·S) + ((tanh(v))⊗(tanh(k)) - (σ(σ(0.179))·(σ(0.179)·S)((k)⊗(k)) + σ(σ(0.179))·(σ(0.179)·S)((k)⊗(k)))))

Effective program (14 instructions):
  s0 = 0.1792
  s3 = Sigmoid(s0)
  M3 = Outer(V0, V0)
  V0 = Tanh(V0)
  M2 = MatScale(s3, M0)
  M1 = MatMul(M2, M3)
  M0 = MatAdd(M2, M2)
  s3 = Sigmoid(s3)
  M3 = MatScale(s3, M1)
  V5 = Tanh(V1)
  M2 = Outer(V5, V0)
  M1 = MatAdd(M3, M3)
  M2 = MatSub(M2, M1)
  M0 = MatAdd(M0, M2)

train acc 0.973
test d16 T12 ow0.3: acc 0.966  margin 0.299
test d16 T12 ow0.0: acc 0.955  margin 0.277
test d16 T12 ow0.6: acc 0.963  margin 0.288
test d32 T24 ow0.3: acc 0.969  margin 0.345
test d8 T6 ow0.3: acc 0.831  margin 0.135
```

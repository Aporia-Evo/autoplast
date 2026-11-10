# Search seed 14

add-node mutation: on  candidates: 1500020  real evaluations (after cache): 600592  time: 1811s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 5620 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 5620 candidates

## Best rule

```
S' = ((((tanh(norm(tanh(v))))⊗(k) + |tanh(v)|·S) + |tanh(v)|·(tanh(norm(tanh(v))))⊗(k)) + ((σ(0)·|tanh(v)|·(tanh(norm(tanh(v))))⊗(k))(|tanh(v)|·S))((σ(0)·|tanh(v)|·(tanh(norm(tanh(v))))⊗(k))(|tanh(v)|·S)))

Effective program (14 instructions):
  V5 = Tanh(V1)
  s3 = Sigmoid(s1)
  s0 = Norm(V5)
  V2 = Normalize(V5)
  V5 = Tanh(V2)
  M3 = Outer(V5, V0)
  M0 = MatScale(s0, M0)
  M2 = MatScale(s0, M3)
  M1 = MatScale(s3, M2)
  M1 = MatMul(M1, M0)
  M1 = MatMul(M1, M1)
  M0 = MatAdd(M3, M0)
  M0 = MatAdd(M0, M2)
  M0 = MatAdd(M0, M1)

train acc 0.821
test d16 T12 ow0.3: acc 0.787  margin 0.149
test d16 T12 ow0.0: acc 0.867  margin 0.185
test d16 T12 ow0.6: acc 0.648  margin 0.068
test d32 T24 ow0.3: acc 0.878  margin 0.225
test d8 T6 ow0.3: acc 0.634  margin 0.032
```

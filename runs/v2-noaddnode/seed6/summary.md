# Search seed 6

add-node mutation: off  candidates: 1500020  real evaluations (after cache): 637437  time: 1603s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 13044 candidates
- delta rule (beta=1) (acc 0.858): 109428 candidates
- delta rule (beta=0.5) (acc 0.932): 109940 candidates
- gated delta (alpha=0.9) (acc 0.729): 13044 candidates

## Best rule

```
S' = 1.101·((S + (v)⊗(k)) - σ(σ(3.659))·(((S + (v)⊗(k)))(((v)⊗(k))ᵀ))((v)⊗(k)))

Effective program (12 instructions):
  s2 = 3.6588
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  M2 = Transpose(M3)
  M1 = MatMul(M0, M2)
  s2 = Sigmoid(s2)
  s0 = Sigmoid(s2)
  M2 = MatMul(M1, M3)
  M2 = MatScale(s0, M2)
  s3 = 1.1008
  M0 = MatSub(M0, M2)
  M0 = MatScale(s3, M0)

train acc 0.971
test d16 T12 ow0.3: acc 0.968  margin 0.312
test d16 T12 ow0.0: acc 0.948  margin 0.281
test d16 T12 ow0.6: acc 0.963  margin 0.312
test d32 T24 ow0.3: acc 0.975  margin 0.361
test d8 T6 ow0.3: acc 0.838  margin 0.140
```

# Search seed 3

task: v3  alphabet: 18 ops, without MatVec  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 633314  time: 3724s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 21492 candidates
- delta rule (beta=1) (acc 0.853): 58612 candidates
- delta rule (beta=0.5) (acc 0.901): 60788 candidates
- gated delta (alpha=0.9) (acc 0.713): 58612 candidates

## Best rule

```
S' = (0.673·((tanh(v))⊗(k) - ((S + 0))(((tanh(k))⊗(k))((tanh(k))⊗(k)))) + (S + 0))

Effective program (11 instructions):
  s2 = 0.6732
  M2 = MatAdd(M0, M1)
  V5 = Tanh(V1)
  V2 = Tanh(V0)
  M3 = Outer(V2, V0)
  M1 = MatMul(M3, M3)
  M1 = MatMul(M2, M1)
  M3 = Outer(V5, V0)
  M0 = MatSub(M3, M1)
  M1 = MatScale(s2, M0)
  M0 = MatAdd(M1, M2)

train acc 0.909
test d16 T12 ow0.3: acc 0.917  margin 0.271
test d16 T12 ow0.0: acc 0.883  margin 0.232
test d16 T12 ow0.6: acc 0.944  margin 0.288
test d32 T24 ow0.3: acc 0.983  margin 0.363
test d8 T6 ow0.3: acc 0.795  margin 0.114
test d16 T64 K8 ow0.3: acc 0.853  margin 0.198
test d16 T128 K8 ow0.3: acc 0.856  margin 0.193
```

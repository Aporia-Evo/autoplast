# Search seed 11

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 423636  time: 2687s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 37364 candidates
- delta rule (beta=1) (acc 0.853): 253556 candidates
- delta rule (beta=0.5) (acc 0.901): 258548 candidates
- gated delta (alpha=0.9) (acc 0.713): 45684 candidates

## Best rule

```
S' = (S + (0.674·((v)⊗(tanh(k)) - S))((tanh(k))⊗(tanh(k))))

Effective program (8 instructions):
  V0 = Tanh(V0)
  M2 = Outer(V1, V0)
  s1 = 0.6740
  M1 = Outer(V0, V0)
  M3 = MatSub(M2, M0)
  M3 = MatScale(s1, M3)
  M1 = MatMul(M3, M1)
  M0 = MatAdd(M0, M1)

train acc 0.907
test d16 T12 ow0.3: acc 0.919  margin 0.270
test d16 T12 ow0.0: acc 0.878  margin 0.231
test d16 T12 ow0.6: acc 0.943  margin 0.288
test d32 T24 ow0.3: acc 0.983  margin 0.363
test d8 T6 ow0.3: acc 0.787  margin 0.111
test d16 T64 K8 ow0.3: acc 0.854  margin 0.199
test d16 T128 K8 ow0.3: acc 0.853  margin 0.193
```

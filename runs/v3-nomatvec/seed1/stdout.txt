# Search seed 1

task: v3  alphabet: 18 ops, without MatVec  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 398374  time: 998s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 78068 candidates
- delta rule (beta=1) (acc 0.853): 1076084 candidates
- delta rule (beta=0.5) (acc 0.901): 1076980 candidates
- gated delta (alpha=0.9) (acc 0.713): 99060 candidates

## Best rule

```
S' = (((v)⊗(k) - 1.004·(0 - S)) - (((v)⊗(k) - 1.004·(0 - S)))(0.596·(k)⊗(k)))

Effective program (10 instructions):
  M1 = MatSub(M3, M0)
  M0 = Outer(V1, V0)
  s1 = 1.0042
  M3 = MatScale(s1, M1)
  M0 = MatSub(M0, M3)
  M1 = Outer(V0, V0)
  s1 = 0.5957
  M1 = MatScale(s1, M1)
  M3 = MatMul(M0, M1)
  M0 = MatSub(M0, M3)

train acc 0.908
test d16 T12 ow0.3: acc 0.923  margin 0.272
test d16 T12 ow0.0: acc 0.889  margin 0.237
test d16 T12 ow0.6: acc 0.948  margin 0.287
test d32 T24 ow0.3: acc 0.986  margin 0.365
test d8 T6 ow0.3: acc 0.797  margin 0.117
test d16 T64 K8 ow0.3: acc 0.854  margin 0.191
test d16 T128 K8 ow0.3: acc 0.851  margin 0.184
```

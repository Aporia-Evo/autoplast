# Search seed 6

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 443373  time: 898s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 86516 candidates
- delta rule (beta=1) (acc 0.853): 198004 candidates
- delta rule (beta=0.5) (acc 0.901): 198644 candidates
- gated delta (alpha=0.9) (acc 0.713): 89844 candidates

## Best rule

```
S' = (S + (((tanh(v) + v) - 0.557·S·norm(tanh(k))))⊗(k))

Effective program (10 instructions):
  V5 = Tanh(V1)
  s0 = 0.5567
  V4 = VecAdd(V5, V1)
  M2 = MatScale(s0, M0)
  V5 = Tanh(V0)
  V1 = Normalize(V5)
  V3 = MatVec(M2, V1)
  V1 = VecSub(V4, V3)
  M2 = Outer(V1, V0)
  M0 = MatAdd(M0, M2)

train acc 0.908
test d16 T12 ow0.3: acc 0.923  margin 0.267
test d16 T12 ow0.0: acc 0.890  margin 0.235
test d16 T12 ow0.6: acc 0.945  margin 0.278
test d32 T24 ow0.3: acc 0.985  margin 0.357
test d8 T6 ow0.3: acc 0.792  margin 0.115
test d16 T64 K8 ow0.3: acc 0.851  margin 0.182
test d16 T128 K8 ow0.3: acc 0.847  margin 0.178
```

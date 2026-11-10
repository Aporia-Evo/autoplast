# Search seed 5

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 379379  time: 700s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 130548 candidates
- delta rule (beta=1) (acc 0.853): 814964 candidates
- delta rule (beta=0.5) (acc 0.901): 885748 candidates
- gated delta (alpha=0.9) (acc 0.713): 154228 candidates

## Best rule

```
S' = (S + (0.714·(tanh(v) - |tanh(S·k)|·S·k))⊗(k))

Effective program (10 instructions):
  s1 = 0.7137
  V2 = MatVec(M0, V0)
  V5 = Tanh(V2)
  s3 = Norm(V5)
  V2 = VecScale(s3, V2)
  V5 = Tanh(V1)
  V3 = VecSub(V5, V2)
  V1 = VecScale(s1, V3)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)

train acc 0.918
test d16 T12 ow0.3: acc 0.937  margin 0.259
test d16 T12 ow0.0: acc 0.922  margin 0.235
test d16 T12 ow0.6: acc 0.949  margin 0.266
test d32 T24 ow0.3: acc 0.990  margin 0.348
test d8 T6 ow0.3: acc 0.791  margin 0.109
test d16 T64 K8 ow0.3: acc 0.845  margin 0.175
test d16 T128 K8 ow0.3: acc 0.835  margin 0.171
```

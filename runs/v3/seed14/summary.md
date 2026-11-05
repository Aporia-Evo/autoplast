# Search seed 14

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 524333  time: 999s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 25076 candidates
- delta rule (beta=1) (acc 0.853): not reached
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 28276 candidates

## Best rule

```
S' = ((v)⊗((norm(tanh(tanh(k))) + (tanh(k) + tanh(tanh(k))))) + |tanh(tanh(k))|·S)

Effective program (9 instructions):
  V3 = Tanh(V0)
  V2 = Tanh(V3)
  V5 = Normalize(V2)
  s2 = Norm(V2)
  M2 = MatScale(s2, M0)
  V3 = VecAdd(V3, V2)
  V2 = VecAdd(V5, V3)
  M0 = Outer(V1, V2)
  M0 = MatAdd(M0, M2)

train acc 0.721
test d16 T12 ow0.3: acc 0.776  margin 0.145
test d16 T12 ow0.0: acc 0.788  margin 0.151
test d16 T12 ow0.6: acc 0.702  margin 0.100
test d32 T24 ow0.3: acc 0.856  margin 0.220
test d8 T6 ow0.3: acc 0.639  margin 0.030
test d16 T64 K8 ow0.3: acc 0.561  margin -0.012
test d16 T128 K8 ow0.3: acc 0.550  margin -0.026
```

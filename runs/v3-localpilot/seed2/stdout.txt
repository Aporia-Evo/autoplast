# Search seed 2

task: v3  add-node mutation: on  candidates: 300020  real evaluations (after cache): 98167  time: 199s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 13172 candidates
- delta rule (beta=1) (acc 0.853): 15732 candidates
- delta rule (beta=0.5) (acc 0.901): 18420 candidates
- gated delta (alpha=0.9) (acc 0.713): 14196 candidates

## Best rule

```
S' = (S + ((tanh(tanh(tanh(v))) - 0.595·(S - 0.595·(k)⊗(tanh(tanh(v))))·k))⊗(k))

Effective program (12 instructions):
  V1 = Tanh(V1)
  V5 = Tanh(V1)
  V1 = Tanh(V5)
  M1 = Outer(V0, V5)
  s1 = 0.5951
  M3 = MatScale(s1, M1)
  M2 = MatSub(M0, M3)
  V4 = MatVec(M2, V0)
  V3 = VecScale(s1, V4)
  V1 = VecSub(V1, V3)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)

train acc 0.913
test d16 T12 ow0.3: acc 0.915  margin 0.265
test d16 T12 ow0.0: acc 0.878  margin 0.228
test d16 T12 ow0.6: acc 0.943  margin 0.280
test d32 T24 ow0.3: acc 0.984  margin 0.358
test d8 T6 ow0.3: acc 0.783  margin 0.107
test d16 T64 K8 ow0.3: acc 0.853  margin 0.190
test d16 T128 K8 ow0.3: acc 0.853  margin 0.187
```

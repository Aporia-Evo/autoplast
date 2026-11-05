# Search seed 14

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 529600  time: 1454s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 68980 candidates
- delta rule (beta=1) (acc 0.853): 1014516 candidates
- delta rule (beta=0.5) (acc 0.901): 1022324 candidates
- gated delta (alpha=0.9) (acc 0.713): 70772 candidates

## Best rule

```
S' = ((tanh(((0 - S)·max(tanh(tanh(tanh(tanh(tanh(tanh(k)))))), tanh(tanh(tanh(k)))) + tanh(v))))⊗(tanh(tanh(max(tanh(tanh(tanh(tanh(tanh(tanh(k)))))), tanh(tanh(tanh(k))))))) + S)

Effective program (16 instructions):
  M2 = MatSub(M2, M0)
  V2 = Tanh(V0)
  V2 = Tanh(V2)
  V0 = Tanh(V2)
  V4 = Tanh(V0)
  V3 = Tanh(V4)
  V2 = Tanh(V3)
  V3 = VecMax(V2, V0)
  V2 = MatVec(M2, V3)
  V0 = Tanh(V1)
  V4 = Tanh(V3)
  V5 = Tanh(V4)
  V3 = VecAdd(V2, V0)
  V4 = Tanh(V3)
  M2 = Outer(V4, V5)
  M0 = MatAdd(M2, M0)

train acc 0.904
test d16 T12 ow0.3: acc 0.911  margin 0.267
test d16 T12 ow0.0: acc 0.871  margin 0.224
test d16 T12 ow0.6: acc 0.939  margin 0.285
test d32 T24 ow0.3: acc 0.976  margin 0.363
test d8 T6 ow0.3: acc 0.767  margin 0.099
test d16 T64 K8 ow0.3: acc 0.849  margin 0.196
test d16 T128 K8 ow0.3: acc 0.850  margin 0.188
```

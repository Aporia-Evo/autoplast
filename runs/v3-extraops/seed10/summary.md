# Search seed 10

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 744604  time: 1338s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 14324 candidates
- delta rule (beta=1) (acc 0.853): 20468 candidates
- delta rule (beta=0.5) (acc 0.901): 30708 candidates
- gated delta (alpha=0.9) (acc 0.713): 14708 candidates

## Best rule

```
S' = (((tanh(v) + (0 - S)·tanh(tanh(tanh(k)))))⊗(tanh(0.764·max(tanh(k), tanh(tanh(tanh(k)))))) - (0 - S))

Effective program (13 instructions):
  V2 = Tanh(V0)
  V1 = Tanh(V1)
  V0 = Tanh(V2)
  V0 = Tanh(V0)
  M1 = MatSub(M2, M0)
  s0 = 0.7637
  V3 = MatVec(M1, V0)
  V0 = VecMax(V2, V0)
  V5 = VecAdd(V1, V3)
  V0 = VecScale(s0, V0)
  V3 = Tanh(V0)
  M0 = Outer(V5, V3)
  M0 = MatSub(M0, M1)

train acc 0.908
test d16 T12 ow0.3: acc 0.919  margin 0.269
test d16 T12 ow0.0: acc 0.879  margin 0.230
test d16 T12 ow0.6: acc 0.943  margin 0.284
test d32 T24 ow0.3: acc 0.981  margin 0.363
test d8 T6 ow0.3: acc 0.788  margin 0.107
test d16 T64 K8 ow0.3: acc 0.852  margin 0.195
test d16 T128 K8 ow0.3: acc 0.846  margin 0.187
```

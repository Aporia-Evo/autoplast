# Search seed 8

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 681891  time: 3257s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 11380 candidates
- delta rule (beta=1) (acc 0.853): 765300 candidates
- delta rule (beta=0.5) (acc 0.901): 772468 candidates
- gated delta (alpha=0.9) (acc 0.713): 13300 candidates

## Best rule

```
S' = (((norm(tanh(v)) - |S·tanh(tanh(tanh(tanh(tanh(k)))))|·S·tanh(tanh(tanh(tanh(tanh(k)))))))⊗(max(tanh(k), tanh(tanh(tanh(k))))) - (0 - S))

Effective program (15 instructions):
  V2 = Tanh(V0)
  V0 = Tanh(V2)
  V4 = Tanh(V0)
  V3 = VecMax(V2, V4)
  V0 = Tanh(V4)
  V0 = Tanh(V0)
  V1 = Tanh(V1)
  V4 = MatVec(M0, V0)
  M0 = MatSub(M3, M0)
  s2 = Norm(V4)
  V5 = VecScale(s2, V4)
  V1 = Normalize(V1)
  V1 = VecSub(V1, V5)
  M2 = Outer(V1, V3)
  M0 = MatSub(M2, M0)

train acc 0.918
test d16 T12 ow0.3: acc 0.935  margin 0.268
test d16 T12 ow0.0: acc 0.910  margin 0.233
test d16 T12 ow0.6: acc 0.949  margin 0.283
test d32 T24 ow0.3: acc 0.987  margin 0.369
test d8 T6 ow0.3: acc 0.762  margin 0.099
test d16 T64 K8 ow0.3: acc 0.843  margin 0.197
test d16 T128 K8 ow0.3: acc 0.841  margin 0.189
```

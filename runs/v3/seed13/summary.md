# Search seed 13

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 699426  time: 2000s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 21236 candidates
- delta rule (beta=1) (acc 0.853): 134388 candidates
- delta rule (beta=0.5) (acc 0.901): 138612 candidates
- gated delta (alpha=0.9) (acc 0.713): 37236 candidates

## Best rule

```
S' = ((S + (v)⊗(((tanh(k))⊗(k)·(tanh(tanh(tanh(tanh(tanh(k))))) ⊙ tanh(tanh(tanh(tanh(tanh(tanh(k))))))) + norm((tanh(k))⊗(k)·tanh(tanh(tanh(tanh(tanh(tanh(k)))))))))) - (S·(tanh(k))⊗(k)·tanh(tanh(tanh(tanh(tanh(tanh(k)))))))⊗((tanh(k))⊗(k)·tanh(tanh(tanh(tanh(tanh(tanh(k))))))))

Effective program (17 instructions):
  V3 = Tanh(V0)
  V2 = Tanh(V3)
  M1 = Outer(V3, V0)
  V3 = Tanh(V2)
  V0 = Tanh(V3)
  V0 = Tanh(V0)
  V2 = Tanh(V0)
  V3 = Hadamard(V0, V2)
  V5 = MatVec(M1, V3)
  V0 = MatVec(M1, V2)
  V3 = Normalize(V0)
  V5 = VecAdd(V5, V3)
  M1 = Outer(V1, V5)
  V2 = MatVec(M0, V0)
  M3 = Outer(V2, V0)
  M0 = MatAdd(M0, M1)
  M0 = MatSub(M0, M3)

train acc 0.908
test d16 T12 ow0.3: acc 0.918  margin 0.266
test d16 T12 ow0.0: acc 0.881  margin 0.232
test d16 T12 ow0.6: acc 0.936  margin 0.276
test d32 T24 ow0.3: acc 0.974  margin 0.363
test d8 T6 ow0.3: acc 0.768  margin 0.099
test d16 T64 K8 ow0.3: acc 0.844  margin 0.186
test d16 T128 K8 ow0.3: acc 0.826  margin 0.171
```

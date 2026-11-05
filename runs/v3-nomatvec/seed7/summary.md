# Search seed 7

task: v3  alphabet: 18 ops, without MatVec  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 493999  time: 2862s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 7540 candidates
- delta rule (beta=1) (acc 0.853): 1351028 candidates
- delta rule (beta=0.5) (acc 0.901): 1356532 candidates
- gated delta (alpha=0.9) (acc 0.713): 113140 candidates

## Best rule

```
S' = 1.002·1.002·1.002·((S - (((tanh(tanh(k)))⊗(tanh(tanh(tanh(v)))) - ((0 - (tanh(tanh(tanh(v))))⊗(tanh(tanh(k)))) + S)))(((tanh(tanh(k)))⊗(tanh(tanh(tanh(v)))))((0 - (tanh(tanh(tanh(v))))⊗(tanh(tanh(k))))))) - ((0 - norm(tanh(tanh(v)))))⊗(k))

Effective program (21 instructions):
  V1 = Tanh(V1)
  V5 = Tanh(V1)
  V2 = Tanh(V5)
  V1 = Tanh(V0)
  V5 = Normalize(V5)
  V5 = VecSub(V4, V5)
  V1 = Tanh(V1)
  M3 = Outer(V2, V1)
  M2 = MatSub(M2, M3)
  M1 = Outer(V1, V2)
  M3 = MatAdd(M2, M0)
  M3 = MatSub(M1, M3)
  M1 = MatMul(M1, M2)
  M2 = Outer(V5, V0)
  M3 = MatMul(M3, M1)
  s1 = 1.0024
  M3 = MatSub(M0, M3)
  M3 = MatSub(M3, M2)
  s2 = SMul(s1, s1)
  s2 = SMul(s2, s1)
  M0 = MatScale(s2, M3)

train acc 0.916
test d16 T12 ow0.3: acc 0.919  margin 0.271
test d16 T12 ow0.0: acc 0.882  margin 0.232
test d16 T12 ow0.6: acc 0.946  margin 0.289
test d32 T24 ow0.3: acc 0.982  margin 0.372
test d8 T6 ow0.3: acc 0.784  margin 0.105
test d16 T64 K8 ow0.3: acc 0.847  margin 0.189
test d16 T128 K8 ow0.3: acc 0.843  margin 0.181
```

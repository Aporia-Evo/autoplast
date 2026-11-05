# Search seed 2

task: v3  alphabet: 18 ops, without MatVec  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 807120  time: 5321s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 13044 candidates
- delta rule (beta=1) (acc 0.853): 25332 candidates
- delta rule (beta=0.5) (acc 0.901): 49140 candidates
- gated delta (alpha=0.9) (acc 0.713): 25076 candidates

## Best rule

```
S' = ((S + (tanh(norm(tanh(v))))⊗(tanh(k))) - ((S - (tanh(v))⊗((((tanh(k) - v) ⊙ tanh(norm(tanh(v)))) ⊙ ((tanh(k) - v) ⊙ tanh(norm(tanh(v))))))))(((tanh(tanh(tanh(k))))⊗(tanh(tanh(tanh(k)))))((tanh(tanh(tanh(k))))⊗(tanh(tanh(tanh(k)))))))

Effective program (17 instructions):
  V0 = Tanh(V0)
  V2 = Tanh(V1)
  V5 = VecSub(V0, V1)
  V4 = Tanh(V0)
  V3 = Tanh(V4)
  V4 = Normalize(V2)
  V4 = Tanh(V4)
  M1 = Outer(V4, V0)
  M3 = Outer(V3, V3)
  V1 = Hadamard(V5, V4)
  V1 = Hadamard(V1, V1)
  M1 = MatAdd(M0, M1)
  M2 = Outer(V2, V1)
  M2 = MatSub(M0, M2)
  M0 = MatMul(M3, M3)
  M3 = MatMul(M2, M0)
  M0 = MatSub(M1, M3)

train acc 0.910
test d16 T12 ow0.3: acc 0.918  margin 0.268
test d16 T12 ow0.0: acc 0.881  margin 0.230
test d16 T12 ow0.6: acc 0.943  margin 0.280
test d32 T24 ow0.3: acc 0.977  margin 0.364
test d8 T6 ow0.3: acc 0.766  margin 0.101
test d16 T64 K8 ow0.3: acc 0.847  margin 0.190
test d16 T128 K8 ow0.3: acc 0.842  margin 0.179
```

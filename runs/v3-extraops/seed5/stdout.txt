# Search seed 5

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 656976  time: 4849s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 11252 candidates
- delta rule (beta=1) (acc 0.853): 1294964 candidates
- delta rule (beta=0.5) (acc 0.901): 1301236 candidates
- gated delta (alpha=0.9) (acc 0.713): 12788 candidates

## Best rule

```
S' = (((tanh((0 - S)·tanh(tanh(tanh(tanh(tanh(tanh(k))))))))⊗(tanh(tanh(tanh(tanh(tanh(tanh(k))))))) + (v)⊗(k)) - (0 - S))

Effective program (13 instructions):
  M1 = MatSub(M1, M0)
  M0 = Outer(V1, V0)
  V4 = Tanh(V0)
  V1 = Tanh(V4)
  V2 = Tanh(V1)
  V4 = Tanh(V2)
  V3 = Tanh(V4)
  V3 = Tanh(V3)
  V5 = MatVec(M1, V3)
  V0 = Tanh(V5)
  M2 = Outer(V0, V3)
  M0 = MatAdd(M2, M0)
  M0 = MatSub(M0, M1)

train acc 0.903
test d16 T12 ow0.3: acc 0.916  margin 0.268
test d16 T12 ow0.0: acc 0.876  margin 0.230
test d16 T12 ow0.6: acc 0.941  margin 0.286
test d32 T24 ow0.3: acc 0.975  margin 0.364
test d8 T6 ow0.3: acc 0.779  margin 0.107
test d16 T64 K8 ow0.3: acc 0.849  margin 0.192
test d16 T128 K8 ow0.3: acc 0.847  margin 0.182
```

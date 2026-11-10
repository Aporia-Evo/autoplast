# Search seed 16

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 463061  time: 1927s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 39796 candidates
- delta rule (beta=1) (acc 0.853): 1282804 candidates
- delta rule (beta=0.5) (acc 0.901): 1285876 candidates
- gated delta (alpha=0.9) (acc 0.713): 40436 candidates

## Best rule

```
S' = (((S - 0) + (((v)⊗(k) + (v)⊗(k)) + (v)⊗(k))) - tanh((((tanh((S - 0)·k) ⊙ (S - 0)·k) ⊙ tanh((S - 0)·k)))⊗(tanh(k))))

Effective program (13 instructions):
  M3 = MatSub(M0, M3)
  V2 = MatVec(M3, V0)
  V5 = Tanh(V2)
  V2 = Hadamard(V5, V2)
  M0 = Outer(V1, V0)
  M1 = MatAdd(M0, M0)
  M2 = MatAdd(M1, M0)
  M0 = MatAdd(M3, M2)
  V5 = Hadamard(V2, V5)
  V2 = Tanh(V0)
  M3 = Outer(V5, V2)
  M1 = MatTanh(M3)
  M0 = MatSub(M0, M1)

train acc 0.913
test d16 T12 ow0.3: acc 0.930  margin 0.260
test d16 T12 ow0.0: acc 0.911  margin 0.232
test d16 T12 ow0.6: acc 0.949  margin 0.272
test d32 T24 ow0.3: acc 0.989  margin 0.330
test d8 T6 ow0.3: acc 0.794  margin 0.113
test d16 T64 K8 ow0.3: acc 0.846  margin 0.183
test d16 T128 K8 ow0.3: acc 0.845  margin 0.176
```

# Search seed 2

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 300020  real evaluations (after cache): 83199  time: 388s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 47988 candidates
- delta rule (beta=1) (acc 0.853): not reached
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 49524 candidates

## Best rule

```
S' = tanh((tanh((v)⊗((tanh(k) + tanh(tanh(k))))) + tanh(S)))

Effective program (8 instructions):
  V5 = Tanh(V0)
  V2 = Tanh(V5)
  V5 = VecAdd(V5, V2)
  M3 = Outer(V1, V5)
  M2 = MatTanh(M0)
  M1 = MatTanh(M3)
  M2 = MatAdd(M1, M2)
  M0 = MatTanh(M2)

train acc 0.721
test d16 T12 ow0.3: acc 0.788  margin 0.149
test d16 T12 ow0.0: acc 0.820  margin 0.166
test d16 T12 ow0.6: acc 0.706  margin 0.099
test d32 T24 ow0.3: acc 0.874  margin 0.224
test d8 T6 ow0.3: acc 0.628  margin 0.034
test d16 T64 K8 ow0.3: acc 0.570  margin -0.006
test d16 T128 K8 ow0.3: acc 0.556  margin -0.018
```

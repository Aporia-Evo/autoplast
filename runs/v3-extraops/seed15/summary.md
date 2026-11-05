# Search seed 15

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 402782  time: 924s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 15988 candidates
- delta rule (beta=1) (acc 0.853): 323572 candidates
- delta rule (beta=0.5) (acc 0.901): 325492 candidates
- gated delta (alpha=0.9) (acc 0.713): 17012 candidates

## Best rule

```
S' = ((S + ((tanh(v) - S·k))⊗(0.571·k)) + ((((tanh(v) - S·k))⊗(0.571·k) - (((tanh(v) - S·k))⊗(0.571·k))(((tanh(v) - S·k))⊗(0.571·k))))((((tanh(v) - S·k))⊗(0.571·k))(((tanh(v) - S·k))⊗(0.571·k))))

Effective program (11 instructions):
  V4 = MatVec(M0, V0)
  V1 = Tanh(V1)
  V1 = VecSub(V1, V4)
  s2 = 0.5707
  V5 = VecScale(s2, V0)
  M2 = Outer(V1, V5)
  M0 = MatAdd(M0, M2)
  M3 = MatMul(M2, M2)
  M1 = MatSub(M2, M3)
  M1 = MatMul(M1, M3)
  M0 = MatAdd(M0, M1)

train acc 0.913
test d16 T12 ow0.3: acc 0.922  margin 0.269
test d16 T12 ow0.0: acc 0.884  margin 0.233
test d16 T12 ow0.6: acc 0.944  margin 0.284
test d32 T24 ow0.3: acc 0.985  margin 0.359
test d8 T6 ow0.3: acc 0.792  margin 0.113
test d16 T64 K8 ow0.3: acc 0.854  margin 0.191
test d16 T128 K8 ow0.3: acc 0.855  margin 0.187
```

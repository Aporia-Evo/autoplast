# Search seed 15

add-node mutation: off  candidates: 1500020  real evaluations (after cache): 432207  time: 264s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 8052 candidates
- delta rule (beta=1) (acc 0.858): 806772 candidates
- delta rule (beta=0.5) (acc 0.932): 980852 candidates
- gated delta (alpha=0.9) (acc 0.729): 8052 candidates

## Best rule

```
S' = ((0.824·(v - S·k))⊗(tanh(tanh(k))) + 1.098·S)

Effective program (10 instructions):
  V4 = Tanh(V0)
  V2 = MatVec(M0, V0)
  s1 = 0.8240
  s2 = 1.0983
  V0 = Tanh(V4)
  V3 = VecSub(V1, V2)
  V4 = VecScale(s1, V3)
  M1 = Outer(V4, V0)
  M0 = MatScale(s2, M0)
  M0 = MatAdd(M1, M0)

train acc 0.975
test d16 T12 ow0.3: acc 0.966  margin 0.306
test d16 T12 ow0.0: acc 0.951  margin 0.279
test d16 T12 ow0.6: acc 0.964  margin 0.300
test d32 T24 ow0.3: acc 0.975  margin 0.360
test d8 T6 ow0.3: acc 0.836  margin 0.136
```

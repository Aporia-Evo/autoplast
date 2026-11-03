# Search seed 7

add-node mutation: on  candidates: 1500020  real evaluations (after cache): 683315  time: 1114s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 52212 candidates
- delta rule (beta=1) (acc 0.858): 439924 candidates
- delta rule (beta=0.5) (acc 0.932): 440436 candidates
- gated delta (alpha=0.9) (acc 0.729): 48244 candidates

## Best rule

```
S' = ((0.824·((0 - S)·k + v))⊗(tanh(tanh(k))) - 1.098·(0 - S))

Effective program (11 instructions):
  V3 = Tanh(V0)
  V5 = Tanh(V3)
  M3 = MatSub(M2, M0)
  V3 = MatVec(M3, V0)
  V0 = VecAdd(V3, V1)
  s0 = 0.8238
  V3 = VecScale(s0, V0)
  s1 = 1.0983
  M0 = Outer(V3, V5)
  M1 = MatScale(s1, M3)
  M0 = MatSub(M0, M1)

train acc 0.975
test d16 T12 ow0.3: acc 0.966  margin 0.306
test d16 T12 ow0.0: acc 0.951  margin 0.279
test d16 T12 ow0.6: acc 0.964  margin 0.300
test d32 T24 ow0.3: acc 0.975  margin 0.360
test d8 T6 ow0.3: acc 0.836  margin 0.136
```

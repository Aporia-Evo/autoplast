# Search seed 3

add-node mutation: on  candidates: 1500020  real evaluations (after cache): 516088  time: 716s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 23412 candidates
- delta rule (beta=1) (acc 0.858): 58612 candidates
- delta rule (beta=0.5) (acc 0.932): 61044 candidates
- gated delta (alpha=0.9) (acc 0.729): 23156 candidates

## Best rule

```
S' = 1.098·((0.750·(v - S·k))⊗(tanh(tanh(k))) + S)

Effective program (10 instructions):
  s0 = 0.7501
  V5 = MatVec(M0, V0)
  V1 = VecSub(V1, V5)
  V1 = VecScale(s0, V1)
  V5 = Tanh(V0)
  V2 = Tanh(V5)
  M1 = Outer(V1, V2)
  M0 = MatAdd(M1, M0)
  s2 = 1.0981
  M0 = MatScale(s2, M0)

train acc 0.975
test d16 T12 ow0.3: acc 0.966  margin 0.306
test d16 T12 ow0.0: acc 0.951  margin 0.279
test d16 T12 ow0.6: acc 0.964  margin 0.300
test d32 T24 ow0.3: acc 0.976  margin 0.360
test d8 T6 ow0.3: acc 0.836  margin 0.136
```

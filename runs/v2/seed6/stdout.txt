# Search seed 6

add-node mutation: on  candidates: 1500020  real evaluations (after cache): 643002  time: 934s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 47988 candidates
- delta rule (beta=1) (acc 0.858): 1206260 candidates
- delta rule (beta=0.5) (acc 0.932): 1207284 candidates
- gated delta (alpha=0.9) (acc 0.729): 47988 candidates

## Best rule

```
S' = (((v - S·k))⊗(tanh(tanh(tanh(norm(tanh(k)))))) - 1.153·(0 - S))

Effective program (12 instructions):
  V2 = MatVec(M0, V0)
  s2 = 1.1533
  V5 = Tanh(V0)
  V1 = VecSub(V1, V2)
  M3 = MatSub(M1, M0)
  V4 = Normalize(V5)
  V5 = Tanh(V4)
  V5 = Tanh(V5)
  V4 = Tanh(V5)
  M0 = Outer(V1, V4)
  M3 = MatScale(s2, M3)
  M0 = MatSub(M0, M3)

train acc 0.969
test d16 T12 ow0.3: acc 0.965  margin 0.310
test d16 T12 ow0.0: acc 0.949  margin 0.280
test d16 T12 ow0.6: acc 0.959  margin 0.305
test d32 T24 ow0.3: acc 0.886  margin 0.275
test d8 T6 ow0.3: acc 0.845  margin 0.143
```

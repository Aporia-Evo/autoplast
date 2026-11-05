# Search seed 2

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 643370  time: 1695s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 13172 candidates
- delta rule (beta=1) (acc 0.853): 15732 candidates
- delta rule (beta=0.5) (acc 0.901): 18420 candidates
- gated delta (alpha=0.9) (acc 0.713): 14196 candidates

## Best rule

```
S' = (S + ((tanh(tanh(v)) - 0.580·|(S - 0.580·(k)⊗(v))·k|·(S - 0.580·(k)⊗(v))·k))⊗(k))

Effective program (13 instructions):
  s1 = 0.5796
  M1 = Outer(V0, V1)
  V5 = Tanh(V1)
  V1 = Tanh(V5)
  M3 = MatScale(s1, M1)
  M2 = MatSub(M0, M3)
  V4 = MatVec(M2, V0)
  s2 = Norm(V4)
  s1 = SMul(s1, s2)
  V3 = VecScale(s1, V4)
  V1 = VecSub(V1, V3)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)

train acc 0.918
test d16 T12 ow0.3: acc 0.935  margin 0.265
test d16 T12 ow0.0: acc 0.911  margin 0.232
test d16 T12 ow0.6: acc 0.949  margin 0.279
test d32 T24 ow0.3: acc 0.990  margin 0.356
test d8 T6 ow0.3: acc 0.794  margin 0.108
test d16 T64 K8 ow0.3: acc 0.852  margin 0.192
test d16 T128 K8 ow0.3: acc 0.850  margin 0.188
```

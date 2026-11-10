# Search seed 2

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 528061  time: 2695s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 47988 candidates
- delta rule (beta=1) (acc 0.853): 994036 candidates
- delta rule (beta=0.5) (acc 0.901): 998644 candidates
- gated delta (alpha=0.9) (acc 0.713): 49524 candidates

## Best rule

```
S' = ((tanh((0.722·v - S·tanh(tanh(max(k, tanh(tanh(tanh(k)))))))))⊗(<tanh(tanh(tanh(k))), tanh(tanh(max(k, tanh(tanh(tanh(k))))))>·k) + S)

Effective program (15 instructions):
  V2 = Tanh(V0)
  V2 = Tanh(V2)
  V2 = Tanh(V2)
  V3 = VecMax(V0, V2)
  V5 = Tanh(V3)
  V5 = Tanh(V5)
  s0 = 0.7222
  s2 = Dot(V2, V5)
  V2 = VecScale(s0, V1)
  V4 = MatVec(M0, V5)
  V1 = VecSub(V2, V4)
  V5 = VecScale(s2, V0)
  V0 = Tanh(V1)
  M3 = Outer(V0, V5)
  M0 = MatAdd(M3, M0)

train acc 0.912
test d16 T12 ow0.3: acc 0.914  margin 0.268
test d16 T12 ow0.0: acc 0.871  margin 0.228
test d16 T12 ow0.6: acc 0.943  margin 0.290
test d32 T24 ow0.3: acc 0.974  margin 0.364
test d8 T6 ow0.3: acc 0.776  margin 0.104
test d16 T64 K8 ow0.3: acc 0.850  margin 0.201
test d16 T128 K8 ow0.3: acc 0.845  margin 0.190
```

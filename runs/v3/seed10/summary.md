# Search seed 10

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 732429  time: 4000s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 62580 candidates
- delta rule (beta=1) (acc 0.853): 99572 candidates
- delta rule (beta=0.5) (acc 0.901): 102260 candidates
- gated delta (alpha=0.9) (acc 0.713): 63988 candidates

## Best rule

```
S' = ((tanh(1.203·v))⊗(tanh(k)) - ((S)((σ(0.673)·tanh(k))⊗(tanh(k))) + (0 - S)))

Effective program (13 instructions):
  s1 = 0.6728
  M2 = MatSub(M2, M0)
  s2 = Sigmoid(s1)
  V4 = Tanh(V0)
  V0 = VecScale(s2, V4)
  M3 = Outer(V0, V4)
  M0 = MatMul(M0, M3)
  s0 = 1.2027
  M2 = MatAdd(M0, M2)
  V5 = VecScale(s0, V1)
  V1 = Tanh(V5)
  M0 = Outer(V1, V4)
  M0 = MatSub(M0, M2)

train acc 0.908
test d16 T12 ow0.3: acc 0.920  margin 0.270
test d16 T12 ow0.0: acc 0.883  margin 0.232
test d16 T12 ow0.6: acc 0.944  margin 0.285
test d32 T24 ow0.3: acc 0.984  margin 0.362
test d8 T6 ow0.3: acc 0.788  margin 0.112
test d16 T64 K8 ow0.3: acc 0.853  margin 0.195
test d16 T128 K8 ow0.3: acc 0.854  margin 0.190
```

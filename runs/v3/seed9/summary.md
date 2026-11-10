# Search seed 9

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 863254  time: 2544s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 30964 candidates
- delta rule (beta=1) (acc 0.853): 33652 candidates
- delta rule (beta=0.5) (acc 0.901): 37620 candidates
- gated delta (alpha=0.9) (acc 0.713): 32500 candidates

## Best rule

```
S' = (S - ((tanh((tanh(tanh(tanh(k))) - norm(tanh(tanh(tanh(k)))))))⊗(tanh((tanh(tanh(tanh(k))) - norm(tanh(tanh(tanh(k))))))) - ((tanh(v) + S·((tanh(tanh(tanh(k))) - norm(tanh(tanh(tanh(k))))) - k)))⊗(0.511·k)))

Effective program (16 instructions):
  V1 = Tanh(V1)
  V4 = Tanh(V0)
  V2 = Tanh(V4)
  s0 = 0.5109
  V4 = Tanh(V2)
  V3 = Normalize(V4)
  V5 = VecScale(s0, V0)
  V3 = VecSub(V4, V3)
  V4 = Tanh(V3)
  V3 = VecSub(V3, V0)
  V0 = MatVec(M0, V3)
  V1 = VecAdd(V1, V0)
  M1 = Outer(V1, V5)
  M3 = Outer(V4, V4)
  M2 = MatSub(M3, M1)
  M0 = MatSub(M0, M2)

train acc 0.911
test d16 T12 ow0.3: acc 0.922  margin 0.268
test d16 T12 ow0.0: acc 0.888  margin 0.233
test d16 T12 ow0.6: acc 0.946  margin 0.281
test d32 T24 ow0.3: acc 0.985  margin 0.356
test d8 T6 ow0.3: acc 0.787  margin 0.111
test d16 T64 K8 ow0.3: acc 0.851  margin 0.187
test d16 T128 K8 ow0.3: acc 0.854  margin 0.184
```

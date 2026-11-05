# Search seed 11

add-node mutation: off  candidates: 1500020  real evaluations (after cache): 431650  time: 262s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.772): 25716 candidates
- delta rule (beta=1) (acc 0.858): 1294452 candidates
- delta rule (beta=0.5) (acc 0.932): 1461620 candidates
- gated delta (alpha=0.9) (acc 0.729): 25716 candidates

## Best rule

```
S' = |(v - tanh(S·k))|·(S + (|0.268·(v - tanh(S·k))| + 0.268)·((v - tanh(S·k)))⊗(k))

Effective program (12 instructions):
  V4 = MatVec(M0, V0)
  V4 = Tanh(V4)
  V1 = VecSub(V1, V4)
  s3 = 0.2681
  M3 = Outer(V1, V0)
  V3 = VecScale(s3, V1)
  s2 = Norm(V3)
  s2 = SAdd(s2, s3)
  s0 = Norm(V1)
  M3 = MatScale(s2, M3)
  M0 = MatAdd(M0, M3)
  M0 = MatScale(s0, M0)

train acc 0.954
test d16 T12 ow0.3: acc 0.953  margin 0.280
test d16 T12 ow0.0: acc 0.924  margin 0.253
test d16 T12 ow0.6: acc 0.929  margin 0.250
test d32 T24 ow0.3: acc 0.000  margin 0.000
test d8 T6 ow0.3: acc 0.802  margin 0.114
```

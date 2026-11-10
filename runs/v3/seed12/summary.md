# Search seed 12

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 558122  time: 1593s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 41588 candidates
- delta rule (beta=1) (acc 0.853): 129012 candidates
- delta rule (beta=0.5) (acc 0.901): 133876 candidates
- gated delta (alpha=0.9) (acc 0.713): 49268 candidates

## Best rule

```
S' = ((v)⊗(k) + (S - 0.580·|tanh(S·k)|·(tanh(S·k))⊗(k)))

Effective program (10 instructions):
  M3 = Outer(V1, V0)
  V5 = MatVec(M0, V0)
  s2 = 0.5797
  V5 = Tanh(V5)
  M1 = Outer(V5, V0)
  s3 = Norm(V5)
  s1 = SMul(s2, s3)
  M1 = MatScale(s1, M1)
  M2 = MatSub(M0, M1)
  M0 = MatAdd(M3, M2)

train acc 0.916
test d16 T12 ow0.3: acc 0.937  margin 0.265
test d16 T12 ow0.0: acc 0.916  margin 0.237
test d16 T12 ow0.6: acc 0.950  margin 0.276
test d32 T24 ow0.3: acc 0.990  margin 0.356
test d8 T6 ow0.3: acc 0.799  margin 0.111
test d16 T64 K8 ow0.3: acc 0.850  margin 0.186
test d16 T128 K8 ow0.3: acc 0.843  margin 0.183
```

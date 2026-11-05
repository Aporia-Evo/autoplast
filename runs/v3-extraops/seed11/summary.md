# Search seed 11

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 458938  time: 1340s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 9716 candidates
- delta rule (beta=1) (acc 0.853): 647412 candidates
- delta rule (beta=0.5) (acc 0.901): 698356 candidates
- gated delta (alpha=0.9) (acc 0.713): 11252 candidates

## Best rule

```
S' = (((tanh(v) - S·0.750·k))⊗(0.750·k) + S)

Effective program (7 instructions):
  V1 = Tanh(V1)
  s1 = 0.7496
  V4 = VecScale(s1, V0)
  V5 = MatVec(M0, V4)
  V1 = VecSub(V1, V5)
  M2 = Outer(V1, V4)
  M0 = MatAdd(M2, M0)

train acc 0.907
test d16 T12 ow0.3: acc 0.922  margin 0.268
test d16 T12 ow0.0: acc 0.890  margin 0.235
test d16 T12 ow0.6: acc 0.945  margin 0.279
test d32 T24 ow0.3: acc 0.985  margin 0.357
test d8 T6 ow0.3: acc 0.793  margin 0.115
test d16 T64 K8 ow0.3: acc 0.853  margin 0.184
test d16 T128 K8 ow0.3: acc 0.851  margin 0.180
```

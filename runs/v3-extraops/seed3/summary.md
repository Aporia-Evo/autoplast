# Search seed 3

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 600478  time: 5115s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 15348 candidates
- delta rule (beta=1) (acc 0.853): not reached
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 17652 candidates

## Best rule

```
S' = …

Effective program (14 instructions):
  M2 = MatTanh(M0)
  M0 = MatSub(M2, M0)
  M3 = Transpose(M0)
  M0 = MatSub(M2, M0)
  V4 = Tanh(V1)
  M1 = Outer(V4, V0)
  M2 = MatAdd(M0, M0)
  M0 = MatAdd(M1, M0)
  M1 = MatSub(M0, M3)
  M2 = MatSub(M3, M2)
  M0 = MatMul(M3, M2)
  M3 = MatMul(M2, M0)
  M1 = MatAdd(M1, M3)
  M0 = MatAdd(M3, M1)

train acc 0.789
test d16 T12 ow0.3: acc 0.835  margin 0.186
test d16 T12 ow0.0: acc 0.852  margin 0.189
test d16 T12 ow0.6: acc 0.816  margin 0.164
test d32 T24 ow0.3: acc 0.913  margin 0.269
test d8 T6 ow0.3: acc 0.000  margin 0.000
test d16 T64 K8 ow0.3: acc 0.680  margin 0.064
test d16 T128 K8 ow0.3: acc 0.666  margin 0.049
```

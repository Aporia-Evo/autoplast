# Search seed 6

task: v3  alphabet: 18 ops, without MatVec  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 574497  time: 2393s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 6260 candidates
- delta rule (beta=1) (acc 0.853): not reached
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 180212 candidates

## Best rule

```
S' = (((v)⊗(k) - (-0.092·(0 - S) + (0 - S))) + ((-1.095·((v)⊗(k) - (-0.092·(0 - S) + (0 - S))))(-0.092·(0 - S)))((-1.095·((v)⊗(k) - (-0.092·(0 - S) + (0 - S))))(-0.092·(0 - S))))

Effective program (11 instructions):
  M3 = MatSub(M1, M0)
  s3 = -0.0924
  M1 = MatScale(s3, M3)
  M3 = MatAdd(M1, M3)
  M0 = Outer(V1, V0)
  M0 = MatSub(M0, M3)
  s3 = -1.0953
  M2 = MatScale(s3, M0)
  M2 = MatMul(M2, M1)
  M3 = MatMul(M2, M2)
  M0 = MatAdd(M0, M3)

train acc 0.728
test d16 T12 ow0.3: acc 0.771  margin 0.144
test d16 T12 ow0.0: acc 0.790  margin 0.152
test d16 T12 ow0.6: acc 0.705  margin 0.100
test d32 T24 ow0.3: acc 0.737  margin 0.162
test d8 T6 ow0.3: acc 0.645  margin 0.035
test d16 T64 K8 ow0.3: acc 0.571  margin -0.008
test d16 T128 K8 ow0.3: acc 0.552  margin -0.026
```

# Search seed 8

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 221222  time: 539s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 4596 candidates
- delta rule (beta=1) (acc 0.853): not reached
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 93940 candidates

## Best rule

```
S' = ((v)⊗(k) + 0.907·S)

Effective program (4 instructions):
  M1 = Outer(V1, V0)
  s3 = 0.9070
  M3 = MatScale(s3, M0)
  M0 = MatAdd(M1, M3)

train acc 0.725
test d16 T12 ow0.3: acc 0.769  margin 0.144
test d16 T12 ow0.0: acc 0.789  margin 0.152
test d16 T12 ow0.6: acc 0.705  margin 0.101
test d32 T24 ow0.3: acc 0.734  margin 0.161
test d8 T6 ow0.3: acc 0.646  margin 0.036
test d16 T64 K8 ow0.3: acc 0.571  margin -0.008
test d16 T128 K8 ow0.3: acc 0.555  margin -0.025
```

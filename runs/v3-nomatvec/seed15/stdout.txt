# Search seed 15

task: v3  alphabet: 18 ops, without MatVec  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 288560  time: 382s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 17396 candidates
- delta rule (beta=1) (acc 0.853): not reached
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 45428 candidates

## Best rule

```
S' = (σ(2.278)·S + (v)⊗(k))

Effective program (5 instructions):
  s2 = 2.2776
  s3 = Sigmoid(s2)
  M3 = Outer(V1, V0)
  M0 = MatScale(s3, M0)
  M0 = MatAdd(M0, M3)

train acc 0.725
test d16 T12 ow0.3: acc 0.769  margin 0.144
test d16 T12 ow0.0: acc 0.789  margin 0.151
test d16 T12 ow0.6: acc 0.705  margin 0.101
test d32 T24 ow0.3: acc 0.734  margin 0.161
test d8 T6 ow0.3: acc 0.646  margin 0.036
test d16 T64 K8 ow0.3: acc 0.571  margin -0.008
test d16 T128 K8 ow0.3: acc 0.555  margin -0.025
```

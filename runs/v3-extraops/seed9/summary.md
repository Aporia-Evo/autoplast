# Search seed 9

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 420080  time: 1450s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 174836 candidates
- delta rule (beta=1) (acc 0.853): not reached
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 175348 candidates

## Best rule

```
S' = σ(2.453)·(tanh(S) + (v)⊗(tanh(k)))

Effective program (7 instructions):
  s2 = 2.4532
  V3 = Tanh(V0)
  M1 = MatTanh(M0)
  M0 = Outer(V1, V3)
  M2 = MatAdd(M1, M0)
  s1 = Sigmoid(s2)
  M0 = MatScale(s1, M2)

train acc 0.727
test d16 T12 ow0.3: acc 0.772  margin 0.146
test d16 T12 ow0.0: acc 0.796  margin 0.155
test d16 T12 ow0.6: acc 0.715  margin 0.103
test d32 T24 ow0.3: acc 0.767  margin 0.180
test d8 T6 ow0.3: acc 0.639  margin 0.038
test d16 T64 K8 ow0.3: acc 0.578  margin -0.004
test d16 T128 K8 ow0.3: acc 0.551  margin -0.021
```

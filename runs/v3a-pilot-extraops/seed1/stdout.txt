# Search seed 1

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 300020  real evaluations (after cache): 70955  time: 253s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 18548 candidates
- delta rule (beta=1) (acc 0.853): not reached
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 20084 candidates

## Best rule

```
S' = ((1.101·(v)⊗(k) + (v)⊗(k)) - tanh((0 - S)))

Effective program (7 instructions):
  M0 = MatSub(M2, M0)
  M2 = MatTanh(M0)
  s0 = 1.1008
  M0 = Outer(V1, V0)
  M3 = MatScale(s0, M0)
  M1 = MatAdd(M3, M0)
  M0 = MatSub(M1, M2)

train acc 0.724
test d16 T12 ow0.3: acc 0.796  margin 0.152
test d16 T12 ow0.0: acc 0.854  margin 0.181
test d16 T12 ow0.6: acc 0.686  margin 0.091
test d32 T24 ow0.3: acc 0.881  margin 0.226
test d8 T6 ow0.3: acc 0.640  margin 0.038
test d16 T64 K8 ow0.3: acc 0.542  margin -0.013
test d16 T128 K8 ow0.3: acc 0.538  margin -0.025
```

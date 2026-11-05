# Search seed 4

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 234037  time: 792s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 25844 candidates
- delta rule (beta=1) (acc 0.853): not reached
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 26996 candidates

## Best rule

```
S' = (tanh(S) + (v)⊗((k + k)))

Effective program (4 instructions):
  V5 = VecAdd(V0, V0)
  M2 = MatTanh(M0)
  M0 = Outer(V1, V5)
  M0 = MatAdd(M2, M0)

train acc 0.720
test d16 T12 ow0.3: acc 0.797  margin 0.152
test d16 T12 ow0.0: acc 0.860  margin 0.184
test d16 T12 ow0.6: acc 0.680  margin 0.088
test d32 T24 ow0.3: acc 0.882  margin 0.226
test d8 T6 ow0.3: acc 0.645  margin 0.039
test d16 T64 K8 ow0.3: acc 0.532  margin -0.016
test d16 T128 K8 ow0.3: acc 0.537  margin -0.029
```

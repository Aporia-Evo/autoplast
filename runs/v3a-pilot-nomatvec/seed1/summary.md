# Search seed 1

task: v3  alphabet: 18 ops, without MatVec  add-node mutation: on  candidates: 300020  real evaluations (after cache): 112227  time: 196s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 81140 candidates
- delta rule (beta=1) (acc 0.853): not reached
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 83316 candidates

## Best rule

```
S' = ((v)⊗(<norm((tanh(k) - (tanh(v) ⊙ tanh(k)))), k>·k) + <tanh(k), tanh(k)>·S)

Effective program (12 instructions):
  V2 = Tanh(V0)
  s3 = Dot(V2, V2)
  M3 = MatScale(s3, M0)
  V5 = Tanh(V1)
  V2 = Hadamard(V5, V2)
  V3 = Tanh(V0)
  V4 = VecSub(V3, V2)
  V2 = Normalize(V4)
  s0 = Dot(V2, V0)
  V3 = VecScale(s0, V0)
  M0 = Outer(V1, V3)
  M0 = MatAdd(M0, M3)

train acc 0.723
test d16 T12 ow0.3: acc 0.768  margin 0.142
test d16 T12 ow0.0: acc 0.771  margin 0.143
test d16 T12 ow0.6: acc 0.710  margin 0.103
test d32 T24 ow0.3: acc 0.849  margin 0.218
test d8 T6 ow0.3: acc 0.639  margin 0.027
test d16 T64 K8 ow0.3: acc 0.566  margin -0.009
test d16 T128 K8 ow0.3: acc 0.559  margin -0.024
```

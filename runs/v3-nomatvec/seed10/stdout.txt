# Search seed 10

task: v3  alphabet: 18 ops, without MatVec  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 645191  time: 2190s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 16244 candidates
- delta rule (beta=1) (acc 0.853): not reached
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 25588 candidates

## Best rule

```
S' = ((v)⊗(tanh(k)) + <v, tanh(v)>·(S - (<((tanh(v) + (tanh(v) ⊙ tanh(v))) + v), tanh(k)>·S)((v)⊗(tanh(k)))))

Effective program (13 instructions):
  V2 = Tanh(V1)
  V3 = Tanh(V0)
  V4 = Hadamard(V2, V2)
  V0 = VecAdd(V2, V4)
  V0 = VecAdd(V0, V1)
  s1 = Dot(V0, V3)
  M1 = Outer(V1, V3)
  s0 = Dot(V1, V2)
  M2 = MatScale(s1, M0)
  M2 = MatMul(M2, M1)
  M3 = MatSub(M0, M2)
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M1, M3)

train acc 0.755
test d16 T12 ow0.3: acc 0.808  margin 0.159
test d16 T12 ow0.0: acc 0.835  margin 0.171
test d16 T12 ow0.6: acc 0.721  margin 0.109
test d32 T24 ow0.3: acc 0.893  margin 0.232
test d8 T6 ow0.3: acc 0.644  margin 0.037
test d16 T64 K8 ow0.3: acc 0.568  margin -0.000
test d16 T128 K8 ow0.3: acc 0.540  margin -0.022
```

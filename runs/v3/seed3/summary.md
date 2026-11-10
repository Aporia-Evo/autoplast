# Search seed 3

task: v3  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 692274  time: 1535s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 20340 candidates
- delta rule (beta=1) (acc 0.853): 20596 candidates
- delta rule (beta=0.5) (acc 0.901): 258164 candidates
- gated delta (alpha=0.9) (acc 0.713): 20596 candidates

## Best rule

```
S' = (σ(<tanh(v), tanh(v)>·|tanh(((k ⊙ tanh(v)) + S·tanh(tanh(k))))|)·((tanh(v) - S·tanh(tanh(k))))⊗(tanh(k)) + S)

Effective program (15 instructions):
  V1 = Tanh(V1)
  V5 = Hadamard(V0, V1)
  V4 = Tanh(V0)
  V0 = Tanh(V4)
  V0 = MatVec(M0, V0)
  V2 = VecSub(V1, V0)
  M1 = Outer(V2, V4)
  V0 = VecAdd(V5, V0)
  V3 = Tanh(V0)
  s3 = Norm(V3)
  s1 = Dot(V1, V1)
  s1 = SMul(s1, s3)
  s2 = Sigmoid(s1)
  M1 = MatScale(s2, M1)
  M0 = MatAdd(M1, M0)

train acc 0.914
test d16 T12 ow0.3: acc 0.921  margin 0.263
test d16 T12 ow0.0: acc 0.886  margin 0.229
test d16 T12 ow0.6: acc 0.944  margin 0.275
test d32 T24 ow0.3: acc 0.983  margin 0.357
test d8 T6 ow0.3: acc 0.783  margin 0.107
test d16 T64 K8 ow0.3: acc 0.849  margin 0.181
test d16 T128 K8 ow0.3: acc 0.840  margin 0.173
```

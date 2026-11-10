# Search seed 7

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 579539  time: 821s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 27508 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = (σ(((|tanh(v)| + |tanh(v)|) + <v, k>))·S + σ(<v, k>)·(v)⊗(k))

Effective program (11 instructions):
  s1 = Dot(V1, V0)
  V4 = Tanh(V1)
  s3 = Norm(V4)
  s2 = SAdd(s3, s3)
  s3 = SAdd(s2, s1)
  s0 = Sigmoid(s3)
  M1 = MatScale(s0, M0)
  s3 = Sigmoid(s1)
  M0 = Outer(V1, V0)
  M0 = MatScale(s3, M0)
  M0 = MatAdd(M1, M0)

train acc 0.511
test regime collision3: acc 0.506  margin -0.052
test d16 T12 ow0.3: acc 0.717  margin 0.115
test d16 T12 ow0.0: acc 0.689  margin 0.093
test d16 T12 ow0.6: acc 0.715  margin 0.108
test d32 T24 ow0.3: acc 0.627  margin 0.089
test d8 T6 ow0.3: acc 0.624  margin 0.025
test d16 T64 K8 ow0.3: acc 0.569  margin -0.019
test d16 T128 K8 ow0.3: acc 0.555  margin -0.036
```

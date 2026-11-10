# Search seed 12

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 422705  time: 1444s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 7668 candidates
- delta rule (beta=1) (acc 0.853): not reached
- delta rule (beta=0.5) (acc 0.901): not reached
- gated delta (alpha=0.9) (acc 0.713): 8564 candidates

## Best rule

```
S' = ((v)⊗((k + k)) + σ(abs(sum(max(0.786·(σ⃗(((tanh((k + k)) + tanh(S)·tanh((k + k))) + (k + k))) - relu(tanh(S)·tanh((k + k)))), (relu(tanh(S)·tanh((k + k))) ⊙ (σ⃗(((tanh((k + k)) + tanh(S)·tanh((k + k))) + (k + k))) - relu(tanh(S)·tanh((k + k)))))))))·S)

Effective program (19 instructions):
  M1 = MatTanh(M0)
  V2 = VecAdd(V0, V0)
  M3 = Outer(V1, V2)
  V0 = Tanh(V2)
  V1 = MatVec(M1, V0)
  V3 = VecAdd(V0, V1)
  V2 = VecAdd(V3, V2)
  V3 = VecSigmoid(V2)
  V0 = VecRelu(V1)
  s0 = 0.7855
  V2 = VecSub(V3, V0)
  V4 = VecScale(s0, V2)
  V2 = Hadamard(V0, V2)
  V0 = VecMax(V4, V2)
  s2 = VecSum(V0)
  s1 = SAbs(s2)
  s3 = Sigmoid(s1)
  M2 = MatScale(s3, M0)
  M0 = MatAdd(M3, M2)

train acc 0.763
test d16 T12 ow0.3: acc 0.805  margin 0.156
test d16 T12 ow0.0: acc 0.900  margin 0.198
test d16 T12 ow0.6: acc 0.753  margin 0.120
test d32 T24 ow0.3: acc 0.852  margin 0.214
test d8 T6 ow0.3: acc 0.654  margin 0.032
test d16 T64 K8 ow0.3: acc 0.582  margin -0.010
test d16 T128 K8 ow0.3: acc 0.554  margin -0.031
```

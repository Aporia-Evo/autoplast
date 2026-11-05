# Search seed 1

task: v3  alphabet: 29 ops, with extra ops  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 662252  time: 4313s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.571): 18548 candidates
- delta rule (beta=1) (acc 0.853): 1215732 candidates
- delta rule (beta=0.5) (acc 0.901): 1253492 candidates
- gated delta (alpha=0.9) (acc 0.713): 20084 candidates

## Best rule

```
S' = ((((0 - S))((tanh((k - tanh((k - 0.638·tanh(k))))))⊗(norm(tanh((k - 0.638·tanh(k)))))) + (tanh(v))⊗(k)) - (0 - S))

Effective program (15 instructions):
  M2 = MatSub(M1, M0)
  s3 = 0.6384
  V3 = Tanh(V1)
  M0 = Outer(V3, V0)
  V4 = Tanh(V0)
  V4 = VecScale(s3, V4)
  V1 = VecSub(V0, V4)
  V2 = Tanh(V1)
  V4 = Normalize(V2)
  V3 = VecSub(V0, V2)
  V5 = Tanh(V3)
  M1 = Outer(V5, V4)
  M3 = MatMul(M2, M1)
  M1 = MatAdd(M3, M0)
  M0 = MatSub(M1, M2)

train acc 0.909
test d16 T12 ow0.3: acc 0.919  margin 0.270
test d16 T12 ow0.0: acc 0.884  margin 0.233
test d16 T12 ow0.6: acc 0.944  margin 0.286
test d32 T24 ow0.3: acc 0.983  margin 0.362
test d8 T6 ow0.3: acc 0.793  margin 0.115
test d16 T64 K8 ow0.3: acc 0.853  margin 0.195
test d16 T128 K8 ow0.3: acc 0.852  margin 0.190
```

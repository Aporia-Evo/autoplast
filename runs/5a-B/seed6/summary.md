# Search seed 6

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 397399  time: 4828s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 15860 candidates
- delta rule (beta=1) (acc 0.578): 1189236 candidates
- delta rule (beta=0.5) (acc 0.617): 1225332 candidates
- gated delta (alpha=0.9) (acc 0.519): 114676 candidates

## Best rule

```
S' = tanh(((((v)⊗(tanh(k)) + (S - 0)) + (v)⊗(tanh(k))) - (tanh(tanh(norm(tanh((((v)⊗(tanh(k)) + (S - 0)) + (v)⊗(tanh(k))))·tanh(max(tanh(k), k))))))⊗(tanh(max(tanh(k), k)))))
o = S·q

Effective program (15 instructions):
  M3 = MatSub(M0, M1)
  V3 = Tanh(V0)
  M0 = Outer(V1, V3)
  M2 = MatAdd(M0, M3)
  V0 = VecMax(V3, V0)
  M2 = MatAdd(M2, M0)
  M0 = MatTanh(M2)
  V3 = Tanh(V0)
  V1 = MatVec(M0, V3)
  V1 = Normalize(V1)
  V0 = Tanh(V1)
  V2 = Tanh(V0)
  M1 = Outer(V2, V3)
  M3 = MatSub(M2, M1)
  M0 = MatTanh(M3)

train acc 0.613
test regime collision3: acc 0.621  margin 0.030
test d16 T12 ow0.3: acc 0.897  margin 0.234
test d16 T12 ow0.0: acc 0.869  margin 0.216
test d16 T12 ow0.6: acc 0.899  margin 0.228
test d32 T24 ow0.3: acc 0.973  margin 0.326
test d8 T6 ow0.3: acc 0.754  margin 0.092
test d16 T64 K8 ow0.3: acc 0.775  margin 0.127
test d16 T128 K8 ow0.3: acc 0.759  margin 0.116
```

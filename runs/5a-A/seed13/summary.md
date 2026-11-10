# Search seed 13

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 803476  time: 4382s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 25204 candidates
- delta rule (beta=1) (acc 0.578): 66804 candidates
- delta rule (beta=0.5) (acc 0.617): 69748 candidates
- gated delta (alpha=0.9) (acc 0.519): 66804 candidates

## Best rule

```
S' = ((S - ((S)((tanh(tanh(tanh(tanh(k)))))⊗(tanh(tanh(tanh(k))))))((tanh(tanh(tanh(tanh(k)))))⊗(tanh(tanh(tanh(k)))))) + (v)⊗(norm((((tanh(tanh(tanh(tanh(k)))) - tanh(k)))⊗(v)·tanh(tanh(tanh(tanh(k)))) + tanh(tanh(tanh(k)))))))

Effective program (15 instructions):
  V2 = Tanh(V0)
  V3 = Tanh(V2)
  V0 = Tanh(V3)
  V5 = Tanh(V0)
  V3 = VecSub(V5, V2)
  M1 = Outer(V3, V1)
  V2 = MatVec(M1, V5)
  M2 = Outer(V5, V0)
  M3 = MatMul(M0, M2)
  V2 = VecAdd(V2, V0)
  V0 = Normalize(V2)
  M3 = MatMul(M3, M2)
  M1 = Outer(V1, V0)
  M0 = MatSub(M0, M3)
  M0 = MatAdd(M0, M1)

train acc 0.623
test regime collision3: acc 0.635  margin 0.044
test d16 T12 ow0.3: acc 0.921  margin 0.266
test d16 T12 ow0.0: acc 0.888  margin 0.233
test d16 T12 ow0.6: acc 0.939  margin 0.274
test d32 T24 ow0.3: acc 0.978  margin 0.364
test d8 T6 ow0.3: acc 0.759  margin 0.098
test d16 T64 K8 ow0.3: acc 0.837  margin 0.180
test d16 T128 K8 ow0.3: acc 0.838  margin 0.167
```

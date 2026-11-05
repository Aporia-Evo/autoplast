# Search seed 11

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 792762  time: 1341s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 90356 candidates
- delta rule (beta=1) (acc 0.578): 91764 candidates
- delta rule (beta=0.5) (acc 0.617): 99444 candidates
- gated delta (alpha=0.9) (acc 0.519): 91764 candidates

## Best rule

```
S' = (((tanh(v) - σ(σ(0))·(v - (0 - S)·tanh(tanh(k)))))⊗(tanh(tanh(k))) - 1.008·(0 - S))

Effective program (14 instructions):
  M0 = MatSub(M2, M0)
  V0 = Tanh(V0)
  s0 = Sigmoid(s1)
  s0 = Sigmoid(s0)
  V3 = Tanh(V0)
  V4 = MatVec(M0, V3)
  V2 = VecSub(V1, V4)
  V5 = VecScale(s0, V2)
  V4 = Tanh(V1)
  V5 = VecSub(V4, V5)
  s1 = 1.0084
  M2 = MatScale(s1, M0)
  M0 = Outer(V5, V3)
  M0 = MatSub(M0, M2)

train acc 0.624
test regime collision3: acc 0.642  margin 0.049
test d16 T12 ow0.3: acc 0.929  margin 0.264
test d16 T12 ow0.0: acc 0.907  margin 0.237
test d16 T12 ow0.6: acc 0.944  margin 0.262
test d32 T24 ow0.3: acc 0.990  margin 0.363
test d8 T6 ow0.3: acc 0.764  margin 0.099
test d16 T64 K8 ow0.3: acc 0.818  margin 0.144
test d16 T128 K8 ow0.3: acc 0.783  margin 0.126
```

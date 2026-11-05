# Search seed 7

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 230260  time: 1196s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 131956 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = tanh(((v)⊗((k + k)) + tanh(S)))
o = (tanh(max(norm(tanh(q)), σ⃗(0))) ⊙ S·q)

Effective program (5 instructions):
  V2 = VecAdd(V0, V0)
  M2 = MatTanh(M0)
  M0 = Outer(V1, V2)
  M0 = MatAdd(M0, M2)
  M0 = MatTanh(M0)

train acc 0.513
test regime collision3: acc 0.521  margin -0.024
test d16 T12 ow0.3: acc 0.782  margin 0.148
test d16 T12 ow0.0: acc 0.808  margin 0.159
test d16 T12 ow0.6: acc 0.718  margin 0.108
test d32 T24 ow0.3: acc 0.873  margin 0.224
test d8 T6 ow0.3: acc 0.642  margin 0.032
test d16 T64 K8 ow0.3: acc 0.584  margin -0.000
test d16 T128 K8 ow0.3: acc 0.568  margin -0.011
```

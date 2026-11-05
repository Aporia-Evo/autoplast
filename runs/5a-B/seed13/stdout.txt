# Search seed 13

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 279561  time: 1664s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 39284 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 1040500 candidates

## Best rule

```
S' = (|tanh(k)|·tanh(tanh(S)) + <k, tanh(k)>·|tanh(k)|·(v)⊗(k))
o = S·q

Effective program (10 instructions):
  V2 = Tanh(V0)
  M0 = MatTanh(M0)
  M2 = MatTanh(M0)
  M1 = Outer(V1, V0)
  s1 = Norm(V2)
  M0 = MatScale(s1, M1)
  M2 = MatScale(s1, M2)
  s1 = Dot(V0, V2)
  M1 = MatScale(s1, M0)
  M0 = MatAdd(M2, M1)

train acc 0.515
test regime collision3: acc 0.517  margin -0.023
test d16 T12 ow0.3: acc 0.791  margin 0.152
test d16 T12 ow0.0: acc 0.829  margin 0.171
test d16 T12 ow0.6: acc 0.703  margin 0.098
test d32 T24 ow0.3: acc 0.876  margin 0.227
test d8 T6 ow0.3: acc 0.642  margin 0.037
test d16 T64 K8 ow0.3: acc 0.563  margin -0.008
test d16 T128 K8 ow0.3: acc 0.544  margin -0.022
```

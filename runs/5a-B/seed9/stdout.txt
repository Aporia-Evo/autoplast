# Search seed 9

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 255309  time: 1852s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 157044 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 1374964 candidates

## Best rule

```
S' = ((v)⊗(k) + tanh((tanh((S + S)) - tanh(S))))
o = (tanh(S·q) - abs(-0.122)·abs(norm(S·q)))

Effective program (7 instructions):
  M2 = MatAdd(M0, M0)
  M2 = MatTanh(M2)
  M3 = MatTanh(M0)
  M2 = MatSub(M2, M3)
  M0 = Outer(V1, V0)
  M3 = MatTanh(M2)
  M0 = MatAdd(M0, M3)

train acc 0.519
test regime collision3: acc 0.516  margin -0.031
test d16 T12 ow0.3: acc 0.769  margin 0.137
test d16 T12 ow0.0: acc 0.787  margin 0.144
test d16 T12 ow0.6: acc 0.716  margin 0.104
test d32 T24 ow0.3: acc 0.867  margin 0.217
test d8 T6 ow0.3: acc 0.617  margin 0.017
test d16 T64 K8 ow0.3: acc 0.572  margin -0.008
test d16 T128 K8 ow0.3: acc 0.558  margin -0.018
```

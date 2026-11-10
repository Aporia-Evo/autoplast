# Search seed 1

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 421185  time: 518s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 14324 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((v)⊗(tanh((k + k))) + σ(1.831)·S)

Effective program (7 instructions):
  V0 = VecAdd(V0, V0)
  s1 = 1.8310
  s1 = Sigmoid(s1)
  M0 = MatScale(s1, M0)
  V2 = Tanh(V0)
  M2 = Outer(V1, V2)
  M0 = MatAdd(M2, M0)

train acc 0.510
test regime collision3: acc 0.509  margin -0.051
test d16 T12 ow0.3: acc 0.716  margin 0.116
test d16 T12 ow0.0: acc 0.685  margin 0.089
test d16 T12 ow0.6: acc 0.723  margin 0.113
test d32 T24 ow0.3: acc 0.598  margin 0.064
test d8 T6 ow0.3: acc 0.632  margin 0.029
test d16 T64 K8 ow0.3: acc 0.573  margin -0.017
test d16 T128 K8 ow0.3: acc 0.542  margin -0.037
```

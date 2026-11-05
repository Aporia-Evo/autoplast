# Search seed 10

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 403509  time: 550s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 12788 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = (0.862·S + (v)⊗(tanh((k + k))))

Effective program (6 instructions):
  V0 = VecAdd(V0, V0)
  s0 = 0.8619
  V5 = Tanh(V0)
  M3 = MatScale(s0, M0)
  M0 = Outer(V1, V5)
  M0 = MatAdd(M3, M0)

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

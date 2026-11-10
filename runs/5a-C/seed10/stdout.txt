# Search seed 10

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 191700  time: 317s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 9844 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = (0.874·S + (v)⊗(tanh(tanh(k))))
o = S·q

Effective program (6 instructions):
  V4 = Tanh(V0)
  V2 = Tanh(V4)
  M2 = Outer(V1, V2)
  s0 = 0.8741
  M1 = MatScale(s0, M0)
  M0 = MatAdd(M1, M2)

train acc 0.509
test regime collision3: acc 0.516  margin -0.043
test d16 T12 ow0.3: acc 0.734  margin 0.126
test d16 T12 ow0.0: acc 0.712  margin 0.108
test d16 T12 ow0.6: acc 0.728  margin 0.112
test d32 T24 ow0.3: acc 0.629  margin 0.092
test d8 T6 ow0.3: acc 0.641  margin 0.033
test d16 T64 K8 ow0.3: acc 0.583  margin -0.010
test d16 T128 K8 ow0.3: acc 0.550  margin -0.030
```

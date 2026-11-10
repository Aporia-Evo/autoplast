# Search seed 16

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 758737  time: 1064s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 9076 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = σ(<tanh((k + k)), (tanh(v) + (k + k))>·0.617)·((norm(tanh(v)))⊗(tanh((k + k))) - (0 - S))

Effective program (13 instructions):
  s1 = 0.6171
  V2 = Tanh(V1)
  V4 = VecAdd(V0, V0)
  V1 = Normalize(V2)
  V0 = Tanh(V4)
  V3 = VecAdd(V2, V4)
  s0 = Dot(V0, V3)
  M3 = MatSub(M1, M0)
  M0 = Outer(V1, V0)
  M0 = MatSub(M0, M3)
  s1 = SMul(s0, s1)
  s1 = Sigmoid(s1)
  M0 = MatScale(s1, M0)

train acc 0.511
test regime collision3: acc 0.517  margin -0.038
test d16 T12 ow0.3: acc 0.743  margin 0.133
test d16 T12 ow0.0: acc 0.731  margin 0.119
test d16 T12 ow0.6: acc 0.713  margin 0.108
test d32 T24 ow0.3: acc 0.716  margin 0.149
test d8 T6 ow0.3: acc 0.627  margin 0.028
test d16 T64 K8 ow0.3: acc 0.578  margin -0.010
test d16 T128 K8 ow0.3: acc 0.550  margin -0.029
```

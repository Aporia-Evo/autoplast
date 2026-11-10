# Search seed 15

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 860571  time: 1768s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 6132 candidates
- delta rule (beta=1) (acc 0.578): 351860 candidates
- delta rule (beta=0.5) (acc 0.617): 354676 candidates
- gated delta (alpha=0.9) (acc 0.519): 351604 candidates

## Best rule

```
S' = ((tanh(<tanh(tanh((tanh(v) ⊙ tanh(v)))), (0·k - tanh(tanh((tanh(v) ⊙ tanh(v)))))>·S·tanh(tanh((k + k)))))⊗((tanh(tanh((k + k))) + tanh((k + k)))) + (S + (v)⊗((k + k))))

Effective program (18 instructions):
  V3 = Tanh(V1)
  V4 = Hadamard(V3, V3)
  V3 = Tanh(V4)
  V2 = Tanh(V3)
  V5 = VecAdd(V0, V0)
  V3 = MatVec(M3, V0)
  V3 = VecSub(V3, V2)
  s3 = Dot(V2, V3)
  M2 = Outer(V1, V5)
  M1 = MatScale(s3, M0)
  M3 = MatAdd(M0, M2)
  V0 = Tanh(V5)
  V5 = Tanh(V0)
  V2 = MatVec(M1, V5)
  V1 = VecAdd(V5, V0)
  V0 = Tanh(V2)
  M1 = Outer(V0, V1)
  M0 = MatAdd(M1, M3)

train acc 0.621
test regime collision3: acc 0.634  margin 0.040
test d16 T12 ow0.3: acc 0.917  margin 0.264
test d16 T12 ow0.0: acc 0.884  margin 0.231
test d16 T12 ow0.6: acc 0.933  margin 0.270
test d32 T24 ow0.3: acc 0.985  margin 0.337
test d8 T6 ow0.3: acc 0.785  margin 0.109
test d16 T64 K8 ow0.3: acc 0.832  margin 0.176
test d16 T128 K8 ow0.3: acc 0.818  margin 0.158
```

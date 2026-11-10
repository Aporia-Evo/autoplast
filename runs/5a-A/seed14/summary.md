# Search seed 14

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 484720  time: 706s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 13940 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((σ(1.831)·(S)ᵀ + (tanh((k + k)))⊗(v)))ᵀ

Effective program (9 instructions):
  M1 = Transpose(M0)
  s0 = 1.8310
  s1 = Sigmoid(s0)
  V3 = VecAdd(V0, V0)
  V0 = Tanh(V3)
  M3 = MatScale(s1, M1)
  M1 = Outer(V0, V1)
  M2 = MatAdd(M3, M1)
  M0 = Transpose(M2)

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

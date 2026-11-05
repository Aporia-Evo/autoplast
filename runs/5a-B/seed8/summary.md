# Search seed 8

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 273716  time: 2345s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 42868 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 577780 candidates

## Best rule

```
S' = (tanh(tanh((((tanh(v))⊗(k) + tanh(S)) + (tanh(v))⊗(k)))) - (tanh((((tanh(v))⊗(k) + tanh(S)) + (tanh(v))⊗(k))) ⊙ (tanh(v))⊗(k)))
o = S·q

Effective program (9 instructions):
  M3 = MatTanh(M0)
  V5 = Tanh(V1)
  M0 = Outer(V5, V0)
  M3 = MatAdd(M0, M3)
  M3 = MatAdd(M3, M0)
  M3 = MatTanh(M3)
  M1 = MatHadamard(M3, M0)
  M0 = MatTanh(M3)
  M0 = MatSub(M0, M1)

train acc 0.518
test regime collision3: acc 0.518  margin -0.035
test d16 T12 ow0.3: acc 0.749  margin 0.134
test d16 T12 ow0.0: acc 0.755  margin 0.130
test d16 T12 ow0.6: acc 0.730  margin 0.111
test d32 T24 ow0.3: acc 0.849  margin 0.215
test d8 T6 ow0.3: acc 0.600  margin 0.004
test d16 T64 K8 ow0.3: acc 0.587  margin -0.003
test d16 T128 K8 ow0.3: acc 0.566  margin -0.015
```

# Search seed 5

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 868690  time: 1491s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 18292 candidates
- delta rule (beta=1) (acc 0.578): 21108 candidates
- delta rule (beta=0.5) (acc 0.617): 21748 candidates
- gated delta (alpha=0.9) (acc 0.519): 21108 candidates

## Best rule

```
S' = (S + -0.696·-0.696·((v - S·k))⊗((k + ((((v - S·k) ⊙ (v - tanh(k))) ⊙ tanh(((v - S·k) ⊙ (v - tanh(k))))) ⊙ tanh(tanh((v - S·k)))))))

Effective program (16 instructions):
  s2 = -0.6963
  V3 = MatVec(M0, V0)
  V4 = Tanh(V0)
  V2 = VecSub(V1, V4)
  V3 = VecSub(V1, V3)
  V5 = Tanh(V3)
  V5 = Tanh(V5)
  V1 = Hadamard(V3, V2)
  V2 = Tanh(V1)
  V4 = Hadamard(V1, V2)
  V4 = Hadamard(V4, V5)
  V1 = VecAdd(V0, V4)
  M1 = Outer(V3, V1)
  M3 = MatScale(s2, M1)
  M3 = MatScale(s2, M3)
  M0 = MatAdd(M0, M3)

train acc 0.625
test regime collision3: acc 0.640  margin 0.047
test d16 T12 ow0.3: acc 0.922  margin 0.256
test d16 T12 ow0.0: acc 0.903  margin 0.236
test d16 T12 ow0.6: acc 0.932  margin 0.255
test d32 T24 ow0.3: acc 0.987  margin 0.348
test d8 T6 ow0.3: acc 0.774  margin 0.099
test d16 T64 K8 ow0.3: acc 0.821  margin 0.143
test d16 T128 K8 ow0.3: acc 0.786  margin 0.131
```

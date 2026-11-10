# Search seed 2

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 300020  real evaluations (after cache): 88920  time: 177s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 25204 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = (|tanh(tanh(tanh(v)))|·(((v + v))⊗(k) + S) - 0)
o = (((σ(0.955)·S·q ⊙ tanh(S·q)) ⊙ tanh(S·q)) + tanh(S·q))

Effective program (9 instructions):
  V5 = Tanh(V1)
  V5 = Tanh(V5)
  V5 = Tanh(V5)
  V2 = VecAdd(V1, V1)
  M2 = Outer(V2, V0)
  s3 = Norm(V5)
  M0 = MatAdd(M2, M0)
  M3 = MatScale(s3, M0)
  M0 = MatSub(M3, M1)

train acc 0.513
test regime collision3: acc 0.517  margin -0.043
test d16 T12 ow0.3: acc 0.727  margin 0.123
test d16 T12 ow0.0: acc 0.704  margin 0.105
test d16 T12 ow0.6: acc 0.722  margin 0.110
test d32 T24 ow0.3: acc 0.793  margin 0.193
test d8 T6 ow0.3: acc 0.632  margin 0.020
test d16 T64 K8 ow0.3: acc 0.582  margin -0.011
test d16 T128 K8 ow0.3: acc 0.560  margin -0.029
```

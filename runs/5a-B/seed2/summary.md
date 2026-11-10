# Search seed 2

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 406229  time: 3405s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 6260 candidates
- delta rule (beta=1) (acc 0.578): 1355892 candidates
- delta rule (beta=0.5) (acc 0.617): 1356788 candidates
- gated delta (alpha=0.9) (acc 0.519): 51188 candidates

## Best rule

```
S' = (((v)⊗(k) + tanh(S)) + ((S ⊙ (v)⊗(k)) - (((v)⊗(k) + tanh(S))·tanh(k))⊗(σ(0)·k)))
o = S·q

Effective program (11 instructions):
  M3 = Outer(V1, V0)
  s1 = Sigmoid(s2)
  M1 = MatTanh(M0)
  M1 = MatAdd(M3, M1)
  M3 = MatHadamard(M0, M3)
  V3 = Tanh(V0)
  V5 = MatVec(M1, V3)
  V4 = VecScale(s1, V0)
  M0 = Outer(V5, V4)
  M2 = MatSub(M3, M0)
  M0 = MatAdd(M1, M2)

train acc 0.623
test regime collision3: acc 0.636  margin 0.044
test d16 T12 ow0.3: acc 0.918  margin 0.253
test d16 T12 ow0.0: acc 0.892  margin 0.229
test d16 T12 ow0.6: acc 0.936  margin 0.254
test d32 T24 ow0.3: acc 0.985  margin 0.345
test d8 T6 ow0.3: acc 0.768  margin 0.099
test d16 T64 K8 ow0.3: acc 0.826  margin 0.157
test d16 T128 K8 ow0.3: acc 0.826  margin 0.152
```

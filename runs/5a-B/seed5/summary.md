# Search seed 5

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 238105  time: 1677s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 10740 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 1162740 candidates

## Best rule

```
S' = tanh(((σ(|(tanh(S) - ((tanh(S))(tanh(S)))ᵀ)·max(tanh((tanh(S))(tanh(S))·k), (v ⊙ (0 - σ⃗(k))))|)·(v)⊗(k) + (v)⊗(k)) + tanh(S)))
o = S·q

Effective program (18 instructions):
  V4 = VecSigmoid(V0)
  V5 = VecSub(V2, V4)
  M1 = MatTanh(M0)
  M0 = Outer(V1, V0)
  M2 = MatMul(M1, M1)
  V3 = MatVec(M2, V0)
  M3 = Transpose(M2)
  M3 = MatSub(M1, M3)
  V4 = Hadamard(V1, V5)
  V0 = Tanh(V3)
  V3 = VecMax(V0, V4)
  V0 = MatVec(M3, V3)
  s0 = Norm(V0)
  s2 = Sigmoid(s0)
  M2 = MatScale(s2, M0)
  M3 = MatAdd(M2, M0)
  M0 = MatAdd(M3, M1)
  M0 = MatTanh(M0)

train acc 0.528
test regime collision3: acc 0.519  margin -0.023
test d16 T12 ow0.3: acc 0.795  margin 0.153
test d16 T12 ow0.0: acc 0.828  margin 0.169
test d16 T12 ow0.6: acc 0.729  margin 0.108
test d32 T24 ow0.3: acc 0.887  margin 0.229
test d8 T6 ow0.3: acc 0.646  margin 0.039
test d16 T64 K8 ow0.3: acc 0.578  margin -0.002
test d16 T128 K8 ow0.3: acc 0.569  margin -0.012
```

# Search seed 2

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 971576  time: 1968s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 34804 candidates
- delta rule (beta=1) (acc 0.578): 75380 candidates
- delta rule (beta=0.5) (acc 0.617): 78068 candidates
- gated delta (alpha=0.9) (acc 0.519): 67700 candidates

## Best rule

```
S' = (S - (|S·k|·((|tanh(|S·k|·tanh((S·k - (σ(0)·tanh(k) ⊙ (v)⊗(tanh(tanh(k)))·tanh(k)))))|·tanh((S·k - (σ(0)·tanh(k) ⊙ (v)⊗(tanh(tanh(k)))·tanh(k)))) + (tanh(|S·k|·tanh((S·k - (σ(0)·tanh(k) ⊙ (v)⊗(tanh(tanh(k)))·tanh(k))))) + tanh(v))))⊗(σ(0)·tanh(k)) - (v)⊗(tanh(tanh(k)))))

Effective program (22 instructions):
  V4 = MatVec(M0, V0)
  V5 = Tanh(V0)
  V2 = Tanh(V5)
  s0 = Sigmoid(s2)
  V0 = VecScale(s0, V5)
  M2 = Outer(V1, V2)
  V3 = MatVec(M2, V5)
  V5 = Hadamard(V0, V3)
  s3 = Norm(V4)
  V3 = VecSub(V4, V5)
  V2 = Tanh(V3)
  V4 = VecScale(s3, V2)
  V3 = Tanh(V4)
  V1 = Tanh(V1)
  s0 = Norm(V3)
  V1 = VecAdd(V3, V1)
  V3 = VecScale(s0, V2)
  V5 = VecAdd(V3, V1)
  M1 = Outer(V5, V0)
  M3 = MatScale(s3, M1)
  M2 = MatSub(M3, M2)
  M0 = MatSub(M0, M2)

train acc 0.642
test regime collision3: acc 0.660  margin 0.054
test d16 T12 ow0.3: acc 0.924  margin 0.243
test d16 T12 ow0.0: acc 0.942  margin 0.233
test d16 T12 ow0.6: acc 0.916  margin 0.230
test d32 T24 ow0.3: acc 0.983  margin 0.337
test d8 T6 ow0.3: acc 0.737  margin 0.085
test d16 T64 K8 ow0.3: acc 0.789  margin 0.124
test d16 T128 K8 ow0.3: acc 0.777  margin 0.113
```

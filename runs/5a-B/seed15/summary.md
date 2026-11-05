# Search seed 15

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 285789  time: 1772s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 260468 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 627828 candidates

## Best rule

```
S' = tanh((tanh(S) + ((v)⊗(k) + tanh((v)⊗(k)))))
o = (S·q ⊙ σ⃗((abs(q) ⊙ σ⃗(q))))

Effective program (6 instructions):
  M0 = MatTanh(M0)
  M1 = Outer(V1, V0)
  M2 = MatTanh(M1)
  M1 = MatAdd(M1, M2)
  M2 = MatAdd(M0, M1)
  M0 = MatTanh(M2)

train acc 0.516
test regime collision3: acc 0.521  margin -0.025
test d16 T12 ow0.3: acc 0.784  margin 0.147
test d16 T12 ow0.0: acc 0.809  margin 0.159
test d16 T12 ow0.6: acc 0.717  margin 0.107
test d32 T24 ow0.3: acc 0.872  margin 0.224
test d8 T6 ow0.3: acc 0.636  margin 0.032
test d16 T64 K8 ow0.3: acc 0.583  margin -0.000
test d16 T128 K8 ow0.3: acc 0.566  margin -0.011
```

# Search seed 6

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 567993  time: 1175s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 37236 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 568308 candidates

## Best rule

```
S' = (((((v + norm(tanh(tanh(v)))))⊗(k) + ((v + norm(tanh(tanh(v)))))⊗(k)) + 0.442·(((v + norm(tanh(tanh(v)))))⊗(k) + (((v + norm(tanh(tanh(v)))))⊗(k) + S))) + ((((v + norm(tanh(tanh(v)))))⊗(k) + ((v + norm(tanh(tanh(v)))))⊗(k)) + 0.442·(((v + norm(tanh(tanh(v)))))⊗(k) + (((v + norm(tanh(tanh(v)))))⊗(k) + S))))
o = (σ(<norm((S·q ⊙ S·q)), tanh((S·q - norm((S·q ⊙ S·q))))>)·tanh((S·q - norm((S·q ⊙ S·q)))) + (S·q - norm((S·q ⊙ S·q))))

Effective program (12 instructions):
  V3 = Tanh(V1)
  V5 = Tanh(V3)
  V5 = Normalize(V5)
  V4 = VecAdd(V1, V5)
  s0 = 0.4421
  M2 = Outer(V4, V0)
  M0 = MatAdd(M2, M0)
  M3 = MatAdd(M2, M0)
  M0 = MatScale(s0, M3)
  M1 = MatAdd(M2, M2)
  M1 = MatAdd(M1, M0)
  M0 = MatAdd(M1, M1)

train acc 0.514
test regime collision3: acc 0.521  margin -0.040
test d16 T12 ow0.3: acc 0.737  margin 0.129
test d16 T12 ow0.0: acc 0.731  margin 0.119
test d16 T12 ow0.6: acc 0.721  margin 0.107
test d32 T24 ow0.3: acc 0.654  margin 0.110
test d8 T6 ow0.3: acc 0.639  margin 0.036
test d16 T64 K8 ow0.3: acc 0.579  margin -0.011
test d16 T128 K8 ow0.3: acc 0.558  margin -0.028
```

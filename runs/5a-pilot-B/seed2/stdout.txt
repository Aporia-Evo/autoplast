# Search seed 2

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 300020  real evaluations (after cache): 77281  time: 636s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 6260 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 51188 candidates

## Best rule

```
S' = ((tanh((v)⊗(k)) + tanh(tanh(S))) + (tanh(tanh((v)⊗(k))) - (… ⊙ …)))
o = S·q

Effective program (15 instructions):
  M3 = Outer(V1, V0)
  M0 = MatTanh(M0)
  M1 = MatTanh(M0)
  M2 = MatTanh(M3)
  M1 = MatAdd(M2, M1)
  M3 = MatSub(M1, M0)
  M0 = MatHadamard(M0, M3)
  M3 = MatHadamard(M0, M0)
  M0 = MatSub(M0, M3)
  M3 = MatAdd(M2, M0)
  M0 = MatAdd(M0, M3)
  M0 = MatHadamard(M0, M0)
  M3 = MatTanh(M2)
  M2 = MatSub(M3, M0)
  M0 = MatAdd(M1, M2)

train acc 0.519
test regime collision3: acc 0.527  margin -0.030
test d16 T12 ow0.3: acc 0.765  margin 0.140
test d16 T12 ow0.0: acc 0.776  margin 0.140
test d16 T12 ow0.6: acc 0.734  margin 0.114
test d32 T24 ow0.3: acc 0.869  margin 0.222
test d8 T6 ow0.3: acc 0.608  margin 0.000
test d16 T64 K8 ow0.3: acc 0.593  margin 0.001
test d16 T128 K8 ow0.3: acc 0.574  margin -0.012
```

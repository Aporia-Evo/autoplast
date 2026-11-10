# Search seed 4

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 311078  time: 521s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 105844 candidates
- delta rule (beta=1) (acc 0.578): 123636 candidates
- delta rule (beta=0.5) (acc 0.617): 128756 candidates
- gated delta (alpha=0.9) (acc 0.519): 113652 candidates

## Best rule

```
S' = ((((0 - S)·k + v))⊗((k ⊙ tanh(σ⃗(tanh(v))))) - (0 - S))
o = tanh(S·q)

Effective program (9 instructions):
  V5 = Tanh(V1)
  V5 = VecSigmoid(V5)
  V4 = Tanh(V5)
  M1 = MatSub(M3, M0)
  V2 = Hadamard(V0, V4)
  V5 = MatVec(M1, V0)
  V5 = VecAdd(V5, V1)
  M0 = Outer(V5, V2)
  M0 = MatSub(M0, M1)

train acc 0.624
test regime collision3: acc 0.638  margin 0.046
test d16 T12 ow0.3: acc 0.923  margin 0.254
test d16 T12 ow0.0: acc 0.903  margin 0.236
test d16 T12 ow0.6: acc 0.933  margin 0.251
test d32 T24 ow0.3: acc 0.986  margin 0.343
test d8 T6 ow0.3: acc 0.788  margin 0.106
test d16 T64 K8 ow0.3: acc 0.811  margin 0.139
test d16 T128 K8 ow0.3: acc 0.788  margin 0.130
```

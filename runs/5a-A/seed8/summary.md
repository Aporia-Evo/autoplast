# Search seed 8

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 647410  time: 955s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 4212 candidates
- delta rule (beta=1) (acc 0.578): 110580 candidates
- delta rule (beta=0.5) (acc 0.617): 113652 candidates
- gated delta (alpha=0.9) (acc 0.519): 109684 candidates

## Best rule

```
S' = (S + σ(<((tanh(v) ⊙ tanh(k)) + (0 - S)·tanh(k)), v>·|(v + (0 - S)·tanh(k))|)·((v + (0 - S)·tanh(k)))⊗(tanh(k)))

Effective program (14 instructions):
  M2 = MatSub(M1, M0)
  V0 = Tanh(V0)
  V3 = Tanh(V1)
  V5 = Hadamard(V3, V0)
  V3 = MatVec(M2, V0)
  V5 = VecAdd(V5, V3)
  s0 = Dot(V5, V1)
  V3 = VecAdd(V1, V3)
  M1 = Outer(V3, V0)
  s2 = Norm(V3)
  s1 = SMul(s0, s2)
  s2 = Sigmoid(s1)
  M3 = MatScale(s2, M1)
  M0 = MatAdd(M0, M3)

train acc 0.632
test regime collision3: acc 0.640  margin 0.044
test d16 T12 ow0.3: acc 0.927  margin 0.255
test d16 T12 ow0.0: acc 0.899  margin 0.234
test d16 T12 ow0.6: acc 0.934  margin 0.249
test d32 T24 ow0.3: acc 0.985  margin 0.346
test d8 T6 ow0.3: acc 0.777  margin 0.103
test d16 T64 K8 ow0.3: acc 0.826  margin 0.143
test d16 T128 K8 ow0.3: acc 0.796  margin 0.132
```

# Search seed 12

task: regime collision3  alphabet: 29 ops, with extra ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 445654  time: 697s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 25972 candidates
- delta rule (beta=1) (acc 0.578): 76148 candidates
- delta rule (beta=0.5) (acc 0.617): 111732 candidates
- gated delta (alpha=0.9) (acc 0.519): 74612 candidates

## Best rule

```
S' = (((v + S·(|S·tanh((0 - k))|·σ⃗((((norm(S·tanh((0 - k))) - tanh((0 - k))) + (norm(S·tanh((0 - k))) + v)) ⊙ (norm(S·tanh((0 - k))) - tanh((0 - k))))) ⊙ tanh((0 - k)))))⊗(k) + S)
o = tanh(tanh(S·q))

Effective program (16 instructions):
  V2 = VecSub(V5, V0)
  V4 = Tanh(V2)
  V3 = MatVec(M0, V4)
  s1 = Norm(V3)
  V3 = Normalize(V3)
  V2 = VecSub(V3, V4)
  V5 = VecAdd(V3, V1)
  V5 = VecAdd(V2, V5)
  V3 = Hadamard(V5, V2)
  V3 = VecSigmoid(V3)
  V2 = VecScale(s1, V3)
  V4 = Hadamard(V2, V4)
  V5 = MatVec(M0, V4)
  V5 = VecAdd(V1, V5)
  M3 = Outer(V5, V0)
  M0 = MatAdd(M3, M0)

train acc 0.631
test regime collision3: acc 0.640  margin 0.049
test d16 T12 ow0.3: acc 0.938  margin 0.262
test d16 T12 ow0.0: acc 0.917  margin 0.233
test d16 T12 ow0.6: acc 0.949  margin 0.272
test d32 T24 ow0.3: acc 0.991  margin 0.351
test d8 T6 ow0.3: acc 0.796  margin 0.111
test d16 T64 K8 ow0.3: acc 0.845  margin 0.182
test d16 T128 K8 ow0.3: acc 0.840  margin 0.178
```

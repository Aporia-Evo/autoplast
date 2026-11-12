# Search seed 9

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 978926  time: 2383s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3700 candidates
* linear attention: 19956 candidates
* decayed linear attention: 26356 candidates
* gated delta rule: 248692 candidates
* delta rule: 249588 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 19956 candidates
- delta rule (beta=1) (acc 0.578): 248948 candidates
- delta rule (beta=0.5) (acc 0.617): 257524 candidates
- gated delta (alpha=0.9) (acc 0.519): 85364 candidates

## Best rule

```
S' = ((P2 + ((((norm(tanh(v)) + norm(tanh(v))) + (norm(tanh(v)) + norm(tanh(v)))) + (norm(tanh(v)) + norm(tanh(v)))))⊗(norm(σ(0)·σ(0)·(P1)ᵀ·k))) - (P1 - (P1·<norm(σ(0)·σ(0)·(P1)ᵀ·k), norm(σ(0)·σ(0)·(P1)ᵀ·k)>·k)⊗(norm(σ(0)·σ(0)·(P1)ᵀ·k))))
P1' = (P1 - (P1·<norm(σ(0)·σ(0)·(P1)ᵀ·k), norm(σ(0)·σ(0)·(P1)ᵀ·k)>·k)⊗(norm(σ(0)·σ(0)·(P1)ᵀ·k)))
P2' = σ(1.390)·(P2 + ((((norm(tanh(v)) + norm(tanh(v))) + (norm(tanh(v)) + norm(tanh(v)))) + (norm(tanh(v)) + norm(tanh(v)))))⊗(norm(σ(0)·σ(0)·(P1)ᵀ·k)))

Effective program (22 instructions):
  V3 = Tanh(V1)
  s2 = Sigmoid(s1)
  M3 = Transpose(M1)
  V2 = MatVec(M3, V0)
  V4 = Normalize(V3)
  s2 = SMul(s2, s2)
  V5 = VecScale(s2, V2)
  V1 = Normalize(V5)
  s2 = Dot(V1, V1)
  V5 = VecScale(s2, V0)
  s3 = 1.3898
  V0 = MatVec(M1, V5)
  M3 = Outer(V0, V1)
  V2 = VecAdd(V4, V4)
  V3 = VecAdd(V2, V2)
  V5 = VecAdd(V3, V2)
  s0 = Sigmoid(s3)
  M0 = Outer(V5, V1)
  M0 = MatAdd(M2, M0)
  M2 = MatScale(s0, M0)
  M1 = MatSub(M1, M3)
  M0 = MatSub(M0, M1)

structure: unclassified  [a=0.817 b=3.724 c=-0.024 g=-0.000, erase c/a=0.030, R²=0.4273, 1408 steps]

train acc 0.863 ±0.010
test regime collision3: acc 0.855  margin 0.229  ±0.004
test d16 T12 ow0.3: acc 0.954  margin 0.327  ±0.003
test d16 T12 ow0.0: acc 0.981  margin 0.343  ±0.002
test d16 T12 ow0.6: acc 0.909  margin 0.262  ±0.005
test d32 T24 ow0.3: acc 0.918  margin 0.361  ±0.004
test d8 T6 ow0.3: acc 0.799  margin 0.130  ±0.008
test d16 T64 K8 ow0.3: acc 0.940  margin 0.304  ±0.005
test d16 T128 K8 ow0.3: acc 0.885  margin 0.256  ±0.010
```

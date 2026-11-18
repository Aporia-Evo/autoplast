# Search seed 6

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1106960  time: 4791s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 300020 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 628 candidates
* unclassified: 4724 candidates
* linear attention: 5236 candidates
* delta rule: 120564 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5236 candidates
- delta rule (beta=1) (acc 0.578): 117492 candidates
- delta rule (beta=0.5) (acc 0.617): 126836 candidates
- gated delta (alpha=0.9) (acc 0.519): 89460 candidates

## Best rule

```
S' = -1.011·((((v)⊗((k + P1·tanh(k))) + S))((norm(norm((k + P1·tanh(k)))))⊗(norm((k + P1·tanh(k))))) - ((v)⊗((k + P1·tanh(k))) + S))
P1' = (σ(1/(0.199))·P1 - |σ(0.199·2.148)·(k + P1·tanh(k))|·|σ(0.199·2.148)·(k + P1·tanh(k))|·(norm(norm((k + P1·tanh(k)))))⊗(norm((k + P1·tanh(k)))))
P2' = |σ(0.199·2.148)·(k + P1·tanh(k))|·|σ(0.199·2.148)·(k + P1·tanh(k))|·(norm(norm((k + P1·tanh(k)))))⊗(norm((k + P1·tanh(k))))

Effective program (24 instructions):
  V2 = Tanh(V0)
  s2 = 0.1986
  V4 = MatVec(M1, V2)
  s3 = Recip(s2)
  s1 = Sigmoid(s3)
  s3 = -1.0114
  s0 = 2.1480
  V4 = VecAdd(V0, V4)
  M3 = Outer(V1, V4)
  V3 = Normalize(V4)
  M0 = MatAdd(M3, M0)
  s0 = SMul(s2, s0)
  s2 = Sigmoid(s0)
  V2 = Normalize(V3)
  M2 = Outer(V2, V3)
  M3 = MatScale(s1, M1)
  V5 = VecScale(s2, V4)
  s1 = Norm(V5)
  M1 = MatMul(M0, M2)
  s2 = SMul(s1, s1)
  M2 = MatScale(s2, M2)
  M0 = MatSub(M1, M0)
  M0 = MatScale(s3, M0)
  M1 = MatSub(M3, M2)

structure: unclassified  [a=0.000 b=0.000 c=0.000 g=0.000, erase c/a=0.000, R²=0.1052, 1408 steps]

train acc 0.909 ±0.008
test regime collision3: acc 0.893  margin 0.240  ±0.004
test d16 T12 ow0.3: acc 0.991  margin 0.360  ±0.001
test d16 T12 ow0.0: acc 0.977  margin 0.314  ±0.002
test d16 T12 ow0.6: acc 0.995  margin 0.378  ±0.001
test d32 T24 ow0.3: acc 0.999  margin 0.446  ±0.000
test d8 T6 ow0.3: acc 0.931  margin 0.195  ±0.005
test d16 T64 K8 ow0.3: acc 0.997  margin 0.377  ±0.001
test d16 T128 K8 ow0.3: acc 0.995  margin 0.370  ±0.002
```

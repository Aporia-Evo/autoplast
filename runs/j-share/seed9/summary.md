# Search seed 9

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1010986  time: 2772s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 300020 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3700 candidates
* decayed linear attention: 13428 candidates
* delta rule: 211828 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 13428 candidates
- delta rule (beta=1) (acc 0.578): 207732 candidates
- delta rule (beta=0.5) (acc 0.617): 211828 candidates
- gated delta (alpha=0.9) (acc 0.519): 112884 candidates

## Best rule

```
S' = (((((v)⊗((k + k))·0 - S·tanh(tanh(k))) + 0))⊗(k) - (σ(1/((0 + <k, tanh(tanh(k))>)))·(P2 - (v)⊗((k + k))) - S))
P1' = ((((v)⊗((k + k))·0 - S·tanh(tanh(k))) + 0))⊗(k)
P2' = σ(1/((0 + <k, tanh(tanh(k))>)))·(P2 - (v)⊗((k + k)))

Effective program (17 instructions):
  V5 = VecAdd(V0, V0)
  M1 = Outer(V1, V5)
  V5 = Tanh(V0)
  V3 = Tanh(V5)
  V4 = MatVec(M0, V3)
  s2 = Dot(V0, V3)
  V5 = MatVec(M1, V2)
  V4 = VecSub(V5, V4)
  M1 = MatSub(M2, M1)
  s3 = SAdd(s0, s2)
  s2 = Recip(s3)
  s2 = Sigmoid(s2)
  M2 = MatScale(s2, M1)
  V5 = VecAdd(V4, V2)
  M1 = Outer(V5, V0)
  M3 = MatSub(M2, M0)
  M0 = MatSub(M1, M3)

structure: unclassified  [a=1.052 b=1.509 c=-0.836 g=-0.003, erase c/a=0.795, R²=0.8277, 1408 steps]

train acc 0.698 ±0.013
test regime collision3: acc 0.694  margin 0.089  ±0.006
test d16 T12 ow0.3: acc 0.929  margin 0.259  ±0.004
test d16 T12 ow0.0: acc 0.922  margin 0.242  ±0.003
test d16 T12 ow0.6: acc 0.904  margin 0.227  ±0.006
test d32 T24 ow0.3: acc 0.976  margin 0.364  ±0.002
test d8 T6 ow0.3: acc 0.694  margin 0.066  ±0.010
test d16 T64 K8 ow0.3: acc 0.861  margin 0.190  ±0.008
test d16 T128 K8 ow0.3: acc 0.868  margin 0.189  ±0.011
```

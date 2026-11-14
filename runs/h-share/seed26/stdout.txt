# Search seed 26

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 951708  time: 619s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3572 candidates
* unclassified: 4340 candidates
* linear attention: 24308 candidates
* delta rule: 341876 candidates
* gated delta rule: 474612 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 24820 candidates
- delta rule (beta=1) (acc 0.858): 49396 candidates
- delta rule (beta=0.5) (acc 0.932): 430708 candidates
- gated delta (alpha=0.9) (acc 0.729): 24308 candidates

## Best rule

```
S' = ((σ((0 + σ(0))) + σ((0 + σ(0))))·σ((0 + σ(0)))·((v - S·tanh((k - 0))))⊗(tanh((k - 0))) - ((σ((0 + σ(0))) + σ((0 + σ(0))))·σ((0 + σ(0)))·(σ((0 + σ(0))) + σ((0 + σ(0))))·σ((0 + σ(0))) + (0 + σ(0)))·(0 - S))

Effective program (17 instructions):
  M1 = MatSub(M1, M0)
  V0 = VecSub(V0, V2)
  V3 = Tanh(V0)
  V2 = MatVec(M0, V3)
  V5 = VecSub(V1, V2)
  V2 = Tanh(V0)
  M0 = Outer(V5, V2)
  s1 = Sigmoid(s2)
  s2 = SAdd(s3, s1)
  s1 = Sigmoid(s2)
  s3 = SAdd(s1, s1)
  s1 = SMul(s3, s1)
  s0 = SMul(s1, s1)
  s3 = SAdd(s0, s2)
  M1 = MatScale(s3, M1)
  M2 = MatScale(s1, M0)
  M0 = MatSub(M2, M1)

structure: gated delta rule  [a=1.100 b=0.737 c=-0.701 g=0.005, erase c/a=0.637, R²=0.9988, 384 steps]

train acc 0.970 ±0.006
test d16 T12 ow0.3: acc 0.967  margin 0.299  ±0.003
test d16 T12 ow0.0: acc 0.957  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.959  margin 0.285  ±0.004
test d32 T24 ow0.3: acc 0.963  margin 0.340  ±0.003
test d8 T6 ow0.3: acc 0.834  margin 0.133  ±0.008
test d16 T64 K8 ow0.3: acc 0.058  margin -0.524  ±0.005
test d16 T128 K8 ow0.3: acc 0.019  margin -0.637  ±0.004
```

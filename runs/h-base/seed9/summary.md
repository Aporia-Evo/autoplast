# Search seed 9

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 393982  time: 200s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2164 candidates
* linear, not error-correcting: 2804 candidates
* unclassified: 5492 candidates
* linear attention: 93044 candidates
* delta rule: 1299444 candidates
* gated delta rule: 1370996 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 93044 candidates
- delta rule (beta=1) (acc 0.858): 1299572 candidates
- delta rule (beta=0.5) (acc 0.932): 1349108 candidates
- gated delta (alpha=0.9) (acc 0.729): 93044 candidates

## Best rule

```
S' = (σ(σ(-1.515)) + σ(σ(-1.515)))·((tanh(σ(σ(σ(σ(-1.515))))·(v - S·k)))⊗(k) - (0 - S))

Effective program (14 instructions):
  s1 = -1.5148
  s1 = Sigmoid(s1)
  M2 = MatSub(M3, M0)
  V2 = MatVec(M0, V0)
  V2 = VecSub(V1, V2)
  s1 = Sigmoid(s1)
  s3 = Sigmoid(s1)
  s0 = Sigmoid(s3)
  V5 = VecScale(s0, V2)
  V1 = Tanh(V5)
  M0 = Outer(V1, V0)
  M0 = MatSub(M0, M2)
  s2 = SAdd(s1, s1)
  M0 = MatScale(s2, M0)

structure: gated delta rule  [a=1.090 b=0.691 c=-0.686 g=0.031, erase c/a=0.630, R²=0.9994, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.967  margin 0.297  ±0.003
test d16 T12 ow0.0: acc 0.956  margin 0.278  ±0.003
test d16 T12 ow0.6: acc 0.961  margin 0.285  ±0.004
test d32 T24 ow0.3: acc 0.961  margin 0.342  ±0.003
test d8 T6 ow0.3: acc 0.832  margin 0.135  ±0.008
test d16 T64 K8 ow0.3: acc 0.063  margin -0.508  ±0.005
test d16 T128 K8 ow0.3: acc 0.010  margin -0.627  ±0.003
```

# Search seed 4

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 739223  time: 322s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1524 candidates
* linear, not error-correcting: 2036 candidates
* unclassified: 3060 candidates
* linear attention: 172404 candidates
* delta + Kronecker mix: 371444 candidates
* delta rule: 371700 candidates
* gated delta rule: 413684 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 172404 candidates
- delta rule (beta=1) (acc 0.858): 363380 candidates
- delta rule (beta=0.5) (acc 0.932): 372596 candidates
- gated delta (alpha=0.9) (acc 0.729): 172148 candidates

## Best rule

```
S' = (σ(|σ(|(v - S·tanh(k))|)·σ(|(v - S·tanh(k))|)·S·tanh(k)|) + σ(|(v - S·tanh(k))|)·σ(|(v - S·tanh(k))|))·(((v - S·tanh(k)))⊗(σ(|(v - S·tanh(k))|)·σ(|(v - S·tanh(k))|)·k) + S)

Effective program (14 instructions):
  V5 = Tanh(V0)
  V4 = MatVec(M0, V5)
  V1 = VecSub(V1, V4)
  s1 = Norm(V1)
  s3 = Sigmoid(s1)
  s2 = SMul(s3, s3)
  V4 = VecScale(s2, V4)
  s0 = Norm(V4)
  s0 = Sigmoid(s0)
  V3 = VecScale(s2, V0)
  s1 = SAdd(s0, s2)
  M3 = Outer(V1, V3)
  M0 = MatAdd(M3, M0)
  M0 = MatScale(s1, M0)

structure: unclassified  [a=1.194 b=0.652 c=-0.691 g=-0.473, erase c/a=0.578, R²=0.9357, 384 steps]

train acc 0.981 ±0.005
test d16 T12 ow0.3: acc 0.971  margin 0.287  ±0.003
test d16 T12 ow0.0: acc 0.958  margin 0.271  ±0.003
test d16 T12 ow0.6: acc 0.961  margin 0.263  ±0.004
test d32 T24 ow0.3: acc 0.693  margin 0.120  ±0.007
test d8 T6 ow0.3: acc 0.819  margin 0.125  ±0.008
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

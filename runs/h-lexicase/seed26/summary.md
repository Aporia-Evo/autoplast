# Search seed 26

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 699179  time: 314s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1396 candidates
* linear, not error-correcting: 1780 candidates
* decayed linear attention: 1780 candidates
* linear attention: 14708 candidates
* delta rule: 28660 candidates
* gated delta rule: 267636 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 14708 candidates
- delta rule (beta=1) (acc 0.858): 23284 candidates
- delta rule (beta=0.5) (acc 0.932): 24308 candidates
- gated delta (alpha=0.9) (acc 0.729): 14708 candidates

## Best rule

```
S' = (σ(|tanh(S·k)|)·σ(|tanh(S·k)|) + σ(1.167))·(S + ((v - tanh(S·k)))⊗(σ(|tanh(S·k)|)·k))

Effective program (13 instructions):
  s3 = 1.1668
  V2 = MatVec(M0, V0)
  V3 = Tanh(V2)
  s0 = Norm(V3)
  V3 = VecSub(V1, V3)
  s1 = Sigmoid(s3)
  s0 = Sigmoid(s0)
  V0 = VecScale(s0, V0)
  s0 = SMul(s0, s0)
  M2 = Outer(V3, V0)
  M0 = MatAdd(M0, M2)
  s3 = SAdd(s0, s1)
  M0 = MatScale(s3, M0)

structure: unclassified  [a=1.220 b=0.718 c=-0.804 g=-0.075, erase c/a=0.659, R²=0.9391, 384 steps]

train acc 0.978 ±0.005
test d16 T12 ow0.3: acc 0.970  margin 0.303  ±0.003
test d16 T12 ow0.0: acc 0.940  margin 0.270  ±0.003
test d16 T12 ow0.6: acc 0.953  margin 0.285  ±0.004
test d32 T24 ow0.3: acc 0.686  margin 0.104  ±0.007
test d8 T6 ow0.3: acc 0.821  margin 0.129  ±0.008
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

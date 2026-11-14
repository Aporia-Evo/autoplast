# Search seed 21

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 717214  time: 416s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2036 candidates
* linear, not error-correcting: 2420 candidates
* unclassified: 3316 candidates
* linear attention: 21620 candidates
* delta rule: 267124 candidates
* gated delta rule: 276980 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 21620 candidates
- delta rule (beta=1) (acc 0.858): 259828 candidates
- delta rule (beta=0.5) (acc 0.932): 267124 candidates
- gated delta (alpha=0.9) (acc 0.729): 21620 candidates

## Best rule

```
S' = (((1.113·S + 0) - σ(1.113·|1.113·S·k|·σ(0))·(1.113·S·k)⊗(k)) + (v)⊗(tanh(k)))

Effective program (15 instructions):
  s0 = 1.1126
  M1 = MatScale(s0, M0)
  V5 = MatVec(M1, V0)
  s1 = Norm(V5)
  s0 = SMul(s0, s1)
  s1 = Sigmoid(s3)
  M0 = MatAdd(M1, M3)
  s2 = SMul(s0, s1)
  M1 = Outer(V5, V0)
  s0 = Sigmoid(s2)
  M3 = MatScale(s0, M1)
  M3 = MatSub(M0, M3)
  V4 = Tanh(V0)
  M0 = Outer(V1, V4)
  M0 = MatAdd(M3, M0)

structure: gated delta rule  [a=1.113 b=0.951 c=-0.750 g=0.014, erase c/a=0.674, R²=0.9970, 384 steps]

train acc 0.977 ±0.005
test d16 T12 ow0.3: acc 0.970  margin 0.306  ±0.003
test d16 T12 ow0.0: acc 0.957  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.299  ±0.004
test d32 T24 ow0.3: acc 0.981  margin 0.357  ±0.002
test d8 T6 ow0.3: acc 0.844  margin 0.140  ±0.008
test d16 T64 K8 ow0.3: acc 0.221  margin -0.356  ±0.009
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

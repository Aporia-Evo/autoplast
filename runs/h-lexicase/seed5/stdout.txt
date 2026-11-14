# Search seed 5

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 604407  time: 311s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1524 candidates
* decayed linear attention: 2036 candidates
* linear, not error-correcting: 2804 candidates
* gated delta rule: 27380 candidates
* linear attention: 28660 candidates
* delta rule: 361716 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 29044 candidates
- delta rule (beta=1) (acc 0.858): 307060 candidates
- delta rule (beta=0.5) (acc 0.932): 312948 candidates
- gated delta (alpha=0.9) (acc 0.729): 28660 candidates

## Best rule

```
S' = (σ(<(0 - S)·k, (0 - S)·k>)·((v + (0 - S)·k))⊗(k) - 1.111·(0 - S))

Effective program (10 instructions):
  M3 = MatSub(M2, M0)
  V4 = MatVec(M3, V0)
  V3 = VecAdd(V1, V4)
  s1 = Dot(V4, V4)
  M0 = Outer(V3, V0)
  s1 = Sigmoid(s1)
  M2 = MatScale(s1, M0)
  s1 = 1.1109
  M1 = MatScale(s1, M3)
  M0 = MatSub(M2, M1)

structure: unclassified  [a=1.111 b=0.557 c=-0.633 g=-0.021, erase c/a=0.569, R²=0.9855, 384 steps]

train acc 0.977 ±0.005
test d16 T12 ow0.3: acc 0.971  margin 0.286  ±0.003
test d16 T12 ow0.0: acc 0.962  margin 0.269  ±0.002
test d16 T12 ow0.6: acc 0.964  margin 0.277  ±0.004
test d32 T24 ow0.3: acc 0.991  margin 0.363  ±0.001
test d8 T6 ow0.3: acc 0.827  margin 0.129  ±0.008
test d16 T64 K8 ow0.3: acc 0.178  margin -0.372  ±0.008
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

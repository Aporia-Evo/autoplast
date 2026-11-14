# Search seed 6

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 765238  time: 406s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1268 candidates
* decayed linear attention: 2420 candidates
* linear, not error-correcting: 3188 candidates
* linear attention: 13172 candidates
* delta rule: 164212 candidates
* gated delta rule: 355060 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 13172 candidates
- delta rule (beta=1) (acc 0.858): 150644 candidates
- delta rule (beta=0.5) (acc 0.932): 165236 candidates
- gated delta (alpha=0.9) (acc 0.729): 13172 candidates

## Best rule

```
S' = (((σ(|(0 - S)·k|)·1.038·(v + (0 - S)·k))⊗(k) - 0.167·(0 - S)) - (0 - S))

Effective program (13 instructions):
  M1 = MatSub(M2, M0)
  V3 = MatVec(M1, V0)
  s1 = Norm(V3)
  s1 = Sigmoid(s1)
  s2 = 1.0383
  V2 = VecAdd(V1, V3)
  s0 = SMul(s1, s2)
  V4 = VecScale(s0, V2)
  s0 = 0.1669
  M3 = MatScale(s0, M1)
  M0 = Outer(V4, V0)
  M0 = MatSub(M0, M3)
  M0 = MatSub(M0, M1)

structure: unclassified  [a=1.167 b=0.647 c=-0.752 g=-0.023, erase c/a=0.645, R²=0.9842, 384 steps]

train acc 0.977 ±0.005
test d16 T12 ow0.3: acc 0.974  margin 0.294  ±0.002
test d16 T12 ow0.0: acc 0.961  margin 0.274  ±0.002
test d16 T12 ow0.6: acc 0.963  margin 0.281  ±0.004
test d32 T24 ow0.3: acc 0.942  margin 0.305  ±0.004
test d8 T6 ow0.3: acc 0.841  margin 0.138  ±0.008
test d16 T64 K8 ow0.3: acc 0.036  margin -0.611  ±0.004
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

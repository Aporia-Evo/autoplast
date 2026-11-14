# Search seed 20

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 705032  time: 346s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1268 candidates
* linear, not error-correcting: 1908 candidates
* unclassified: 2676 candidates
* linear attention: 11380 candidates
* delta rule: 11892 candidates
* gated delta rule: 128372 candidates
* delta + Kronecker mix: 130804 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 11380 candidates
- delta rule (beta=1) (acc 0.858): 11892 candidates
- delta rule (beta=0.5) (acc 0.932): 13044 candidates
- gated delta (alpha=0.9) (acc 0.729): 11380 candidates

## Best rule

```
S' = (0.555·(S + S) - σ(<S·k, S·k>)·((v - S·k))⊗((0 - (k - 0))))

Effective program (12 instructions):
  V5 = VecSub(V0, V2)
  V0 = MatVec(M0, V0)
  V1 = VecSub(V1, V0)
  s0 = 0.5554
  M3 = MatAdd(M0, M0)
  M0 = MatScale(s0, M3)
  s0 = Dot(V0, V0)
  s0 = Sigmoid(s0)
  V4 = VecSub(V2, V5)
  M3 = Outer(V1, V4)
  M3 = MatScale(s0, M3)
  M0 = MatSub(M0, M3)

structure: unclassified  [a=1.111 b=0.557 c=-0.633 g=-0.021, erase c/a=0.569, R²=0.9855, 384 steps]

train acc 0.977 ±0.005
test d16 T12 ow0.3: acc 0.971  margin 0.286  ±0.003
test d16 T12 ow0.0: acc 0.962  margin 0.269  ±0.002
test d16 T12 ow0.6: acc 0.964  margin 0.277  ±0.004
test d32 T24 ow0.3: acc 0.991  margin 0.364  ±0.001
test d8 T6 ow0.3: acc 0.826  margin 0.129  ±0.008
test d16 T64 K8 ow0.3: acc 0.180  margin -0.371  ±0.008
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

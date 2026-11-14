# Search seed 28

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 771173  time: 456s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1012 candidates
* linear, not error-correcting: 1396 candidates
* unclassified: 2164 candidates
* linear attention: 34548 candidates
* delta rule: 45172 candidates
* gated delta rule: 126964 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 34548 candidates
- delta rule (beta=1) (acc 0.858): 45172 candidates
- delta rule (beta=0.5) (acc 0.932): 52468 candidates
- gated delta (alpha=0.9) (acc 0.729): 34548 candidates

## Best rule

```
S' = (σ(σ(|v|)·|S·k|)·(((S + 0) + ((v - (S·k - tanh(v))))⊗(k)) - σ(|v|)·(S + 0)) + (S + 0))

Effective program (16 instructions):
  s1 = Norm(V1)
  V5 = Tanh(V1)
  M1 = MatAdd(M0, M3)
  V4 = MatVec(M0, V0)
  s2 = Norm(V4)
  s0 = Sigmoid(s1)
  M3 = MatScale(s0, M1)
  V4 = VecSub(V4, V5)
  s1 = SMul(s0, s2)
  s0 = Sigmoid(s1)
  V4 = VecSub(V1, V4)
  M0 = Outer(V4, V0)
  M0 = MatAdd(M1, M0)
  M3 = MatSub(M0, M3)
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M3, M1)

structure: unclassified  [a=1.200 b=1.311 c=-0.787 g=-0.040, erase c/a=0.656, R²=0.9783, 384 steps]

train acc 0.979 ±0.005
test d16 T12 ow0.3: acc 0.975  margin 0.297  ±0.002
test d16 T12 ow0.0: acc 0.960  margin 0.276  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.281  ±0.004
test d32 T24 ow0.3: acc 0.790  margin 0.197  ±0.006
test d8 T6 ow0.3: acc 0.838  margin 0.138  ±0.008
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

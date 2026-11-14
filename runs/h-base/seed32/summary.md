# Search seed 32

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 553684  time: 283s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* decayed linear attention: 884 candidates
* linear, not error-correcting: 1396 candidates
* linear attention: 9972 candidates
* delta rule: 62964 candidates
* gated delta rule: 88052 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 9972 candidates
- delta rule (beta=1) (acc 0.858): 63732 candidates
- delta rule (beta=0.5) (acc 0.932): 66292 candidates
- gated delta (alpha=0.9) (acc 0.729): 9972 candidates

## Best rule

```
S' = (((v - S·tanh(tanh(k))))⊗(tanh(tanh(tanh(k)))) + 0.554·(S + S))

Effective program (10 instructions):
  V5 = Tanh(V0)
  V4 = Tanh(V5)
  V2 = MatVec(M0, V4)
  V0 = Tanh(V4)
  M1 = MatAdd(M0, M0)
  V1 = VecSub(V1, V2)
  M0 = Outer(V1, V0)
  s1 = 0.5536
  M2 = MatScale(s1, M1)
  M0 = MatAdd(M0, M2)

structure: gated delta rule  [a=1.107 b=0.877 c=-0.800 g=0.012, erase c/a=0.722, R²=0.9933, 384 steps]

train acc 0.970 ±0.006
test d16 T12 ow0.3: acc 0.966  margin 0.310  ±0.003
test d16 T12 ow0.0: acc 0.947  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.307  ±0.004
test d32 T24 ow0.3: acc 0.979  margin 0.369  ±0.002
test d8 T6 ow0.3: acc 0.828  margin 0.133  ±0.008
test d16 T64 K8 ow0.3: acc 0.058  margin -0.531  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

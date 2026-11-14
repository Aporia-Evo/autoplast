# Search seed 21

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 561190  time: 283s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 6004 candidates
* decayed linear attention: 6516 candidates
* linear attention: 7028 candidates
* delta rule: 197748 candidates
* gated delta rule: 198260 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 7028 candidates
- delta rule (beta=1) (acc 0.858): 198260 candidates
- delta rule (beta=0.5) (acc 0.932): 198516 candidates
- gated delta (alpha=0.9) (acc 0.729): 7028 candidates

## Best rule

```
S' = (1.070·1.070·S + ((tanh(v) - S·tanh(k)))⊗(tanh(tanh(tanh(k)))))

Effective program (11 instructions):
  s1 = 1.0699
  s1 = SMul(s1, s1)
  M2 = MatScale(s1, M0)
  V4 = Tanh(V0)
  V5 = Tanh(V4)
  V0 = Tanh(V5)
  V2 = MatVec(M0, V4)
  V3 = Tanh(V1)
  V1 = VecSub(V3, V2)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M2, M1)

structure: gated delta rule  [a=1.145 b=0.834 c=-0.834 g=0.012, erase c/a=0.729, R²=0.9931, 384 steps]

train acc 0.970 ±0.006
test d16 T12 ow0.3: acc 0.966  margin 0.308  ±0.003
test d16 T12 ow0.0: acc 0.953  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.957  margin 0.297  ±0.004
test d32 T24 ow0.3: acc 0.906  margin 0.291  ±0.004
test d8 T6 ow0.3: acc 0.839  margin 0.138  ±0.008
test d16 T64 K8 ow0.3: acc 0.030  margin -0.635  ±0.004
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

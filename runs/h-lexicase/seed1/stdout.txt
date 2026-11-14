# Search seed 1

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 727559  time: 342s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2548 candidates
* decayed linear attention: 3188 candidates
* linear, not error-correcting: 3444 candidates
* linear attention: 33780 candidates
* gated delta rule: 487796 candidates
* delta rule: 487924 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 33780 candidates
- delta rule (beta=1) (acc 0.858): 488820 candidates
- delta rule (beta=0.5) (acc 0.932): 497140 candidates
- gated delta (alpha=0.9) (acc 0.729): 33780 candidates

## Best rule

```
S' = …

Effective program (17 instructions):
  V2 = MatVec(M0, V0)
  V3 = Tanh(V1)
  V3 = VecSub(V3, V2)
  s1 = Dot(V2, V2)
  s3 = SAdd(s1, s1)
  s3 = Sigmoid(s3)
  s2 = SMul(s3, s3)
  s1 = Sigmoid(s2)
  V2 = VecScale(s1, V0)
  V5 = Tanh(V2)
  M3 = Outer(V3, V5)
  M0 = MatAdd(M3, M0)
  s0 = Sigmoid(s3)
  s1 = SMul(s2, s0)
  s3 = Sigmoid(s1)
  M3 = MatScale(s3, M0)
  M0 = MatAdd(M3, M3)

structure: unclassified  [a=1.169 b=0.643 c=-0.731 g=-0.050, erase c/a=0.625, R²=0.9698, 384 steps]

train acc 0.982 ±0.005
test d16 T12 ow0.3: acc 0.975  margin 0.299  ±0.002
test d16 T12 ow0.0: acc 0.959  margin 0.276  ±0.003
test d16 T12 ow0.6: acc 0.959  margin 0.279  ±0.004
test d32 T24 ow0.3: acc 0.734  margin 0.165  ±0.007
test d8 T6 ow0.3: acc 0.829  margin 0.134  ±0.008
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

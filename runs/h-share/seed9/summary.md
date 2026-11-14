# Search seed 9

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 951237  time: 888s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2164 candidates
* linear, not error-correcting: 2804 candidates
* unclassified: 3828 candidates
* delta rule: 15220 candidates
* gated delta rule: 1158900 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 15220 candidates
- delta rule (beta=1) (acc 0.858): 15220 candidates
- delta rule (beta=0.5) (acc 0.932): 31988 candidates
- gated delta (alpha=0.9) (acc 0.729): 15220 candidates

## Best rule

```
S' = ((S - ((((S - 0) - 0)·k - v))⊗(k)) + σ(|v|)·0.233·((S - 0) - 0))

Effective program (12 instructions):
  M2 = MatSub(M0, M1)
  M3 = MatSub(M2, M3)
  V3 = MatVec(M3, V0)
  V4 = VecSub(V3, V1)
  M1 = Outer(V4, V0)
  M2 = MatSub(M0, M1)
  s2 = Norm(V1)
  s3 = Sigmoid(s2)
  s2 = 0.2328
  M0 = MatScale(s2, M3)
  M3 = MatScale(s3, M0)
  M0 = MatAdd(M2, M3)

structure: gated delta rule  [a=1.170 b=1.000 c=-1.000 g=0.000, erase c/a=0.855, R²=1.0000, 384 steps]

train acc 0.960 ±0.007
test d16 T12 ow0.3: acc 0.956  margin 0.315  ±0.003
test d16 T12 ow0.0: acc 0.938  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.955  margin 0.320  ±0.004
test d32 T24 ow0.3: acc 0.854  margin 0.247  ±0.005
test d8 T6 ow0.3: acc 0.841  margin 0.147  ±0.008
test d16 T64 K8 ow0.3: acc 0.022  margin -0.646  ±0.003
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

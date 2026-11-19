# Search seed 30

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 726396  time: 425s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1396 candidates
* decayed linear attention: 1396 candidates
* linear, not error-correcting: 2036 candidates
* linear attention: 25716 candidates
* delta rule: 48116 candidates
* gated delta rule: 1103476 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 26100 candidates
- delta rule (beta=1) (acc 0.858): 39028 candidates
- delta rule (beta=0.5) (acc 0.932): 48628 candidates
- gated delta (alpha=0.9) (acc 0.729): 25716 candidates

## Best rule

```
S' = (0.551 + 0.551)·(((v - tanh((|S·k| + 0.551)·S·k)))⊗(0.551·k) + S)

Effective program (12 instructions):
  s3 = 0.5510
  V3 = MatVec(M0, V0)
  s1 = Norm(V3)
  s0 = SAdd(s1, s3)
  V3 = VecScale(s0, V3)
  V4 = Tanh(V3)
  V1 = VecSub(V1, V4)
  V5 = VecScale(s3, V0)
  M3 = Outer(V1, V5)
  M0 = MatAdd(M3, M0)
  s0 = SAdd(s3, s3)
  M0 = MatScale(s0, M0)

structure: gated delta rule  [a=1.102 b=0.607 c=-0.730 g=0.019, erase c/a=0.662, R²=0.9929, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.970  margin 0.305  ±0.003
test d16 T12 ow0.0: acc 0.957  margin 0.278  ±0.003
test d16 T12 ow0.6: acc 0.965  margin 0.302  ±0.004
test d32 T24 ow0.3: acc 0.982  margin 0.365  ±0.002
test d8 T6 ow0.3: acc 0.841  margin 0.137  ±0.008
test d16 T64 K8 ow0.3: acc 0.063  margin -0.523  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

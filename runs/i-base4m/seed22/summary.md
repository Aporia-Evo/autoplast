# Search seed 22

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 906105  time: 452s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 628 candidates
* linear, not error-correcting: 1908 candidates
* unclassified: 2548 candidates
* linear attention: 11380 candidates
* delta rule: 2341748 candidates
* gated delta rule: 2342644 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 11380 candidates
- delta rule (beta=1) (acc 0.858): 2342388 candidates
- delta rule (beta=0.5) (acc 0.932): 2342644 candidates
- gated delta (alpha=0.9) (acc 0.729): 11380 candidates

## Best rule

```
S' = (0.950·((v - S·tanh(0.950·k)))⊗(tanh(0.950·k)) + 1.107·S)

Effective program (10 instructions):
  s2 = 1.1070
  s3 = 0.9504
  V2 = VecScale(s3, V0)
  V0 = Tanh(V2)
  V4 = MatVec(M0, V0)
  V1 = VecSub(V1, V4)
  M3 = Outer(V1, V0)
  M0 = MatScale(s2, M0)
  M1 = MatScale(s3, M3)
  M0 = MatAdd(M1, M0)

structure: gated delta rule  [a=1.107 b=0.863 c=-0.784 g=0.005, erase c/a=0.708, R²=0.9989, 384 steps]

train acc 0.972 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.310  ±0.003
test d16 T12 ow0.0: acc 0.950  margin 0.281  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.305  ±0.004
test d32 T24 ow0.3: acc 0.971  margin 0.355  ±0.003
test d8 T6 ow0.3: acc 0.839  margin 0.138  ±0.008
test d16 T64 K8 ow0.3: acc 0.062  margin -0.532  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

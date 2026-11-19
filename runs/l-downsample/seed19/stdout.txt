# Search seed 19

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 435600  time: 277s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1268 candidates
* decayed linear attention: 1524 candidates
* linear attention: 9716 candidates
* delta rule: 1111028 candidates
* linear, not error-correcting: 1112308 candidates
* gated delta rule: 1282164 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 9716 candidates
- delta rule (beta=1) (acc 0.858): 1111028 candidates
- delta rule (beta=0.5) (acc 0.932): 1138932 candidates
- gated delta (alpha=0.9) (acc 0.729): 9716 candidates

## Best rule

```
S' = ((tanh((0.619·v - S·tanh(σ(|v|)·tanh(k)))))⊗(k) + 1.086·S)

Effective program (14 instructions):
  s0 = Norm(V1)
  V3 = Tanh(V0)
  s3 = Sigmoid(s0)
  s0 = 1.0857
  V5 = VecScale(s3, V3)
  V3 = Tanh(V5)
  s3 = 0.6187
  V2 = MatVec(M0, V3)
  V3 = VecScale(s3, V1)
  M0 = MatScale(s0, M0)
  V3 = VecSub(V3, V2)
  V5 = Tanh(V3)
  M3 = Outer(V5, V0)
  M0 = MatAdd(M3, M0)

structure: gated delta rule  [a=1.086 b=0.602 c=-0.657 g=0.031, erase c/a=0.605, R²=0.9992, 384 steps]

train acc 0.973 ±0.006
test d16 T12 ow0.3: acc 0.964  margin 0.293  ±0.003
test d16 T12 ow0.0: acc 0.957  margin 0.276  ±0.003
test d16 T12 ow0.6: acc 0.959  margin 0.277  ±0.004
test d32 T24 ow0.3: acc 0.966  margin 0.347  ±0.003
test d8 T6 ow0.3: acc 0.825  margin 0.130  ±0.008
test d16 T64 K8 ow0.3: acc 0.075  margin -0.486  ±0.006
test d16 T128 K8 ow0.3: acc 0.008  margin -0.627  ±0.003
```

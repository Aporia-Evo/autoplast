# Search seed 4

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 664501  time: 432s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2932 candidates
* linear, not error-correcting: 4340 candidates
* unclassified: 5748 candidates
* linear attention: 6644 candidates
* delta rule: 355700 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 6644 candidates
- delta rule (beta=1) (acc 0.858): 355700 candidates
- delta rule (beta=0.5) (acc 0.932): 359028 candidates
- gated delta (alpha=0.9) (acc 0.729): 6644 candidates

## Best rule

```
S' = ((S - 0) - (((tanh(v) + v) - <(tanh(S·k) - norm(tanh(norm(tanh(S·k))))), tanh(S·k)>·tanh(norm(tanh(norm(tanh(S·k)))))))⊗((0 - k)))

Effective program (16 instructions):
  V2 = MatVec(M0, V0)
  V3 = VecSub(V4, V0)
  V0 = Tanh(V1)
  V1 = VecAdd(V0, V1)
  V2 = Tanh(V2)
  V4 = Normalize(V2)
  V4 = Tanh(V4)
  V4 = Normalize(V4)
  V0 = Tanh(V4)
  V4 = VecSub(V2, V4)
  s3 = Dot(V4, V2)
  V0 = VecScale(s3, V0)
  M3 = MatSub(M0, M1)
  V1 = VecSub(V1, V0)
  M0 = Outer(V1, V3)
  M0 = MatSub(M3, M0)

structure: unclassified  [a=1.000 b=1.947 c=-0.461 g=0.016, erase c/a=0.461, R²=0.9575, 384 steps]

train acc 0.955 ±0.007
test d16 T12 ow0.3: acc 0.941  margin 0.255  ±0.004
test d16 T12 ow0.0: acc 0.921  margin 0.223  ±0.003
test d16 T12 ow0.6: acc 0.953  margin 0.272  ±0.004
test d32 T24 ow0.3: acc 0.991  margin 0.356  ±0.001
test d8 T6 ow0.3: acc 0.740  margin 0.085  ±0.009
test d16 T64 K8 ow0.3: acc 0.843  margin 0.186  ±0.008
test d16 T128 K8 ow0.3: acc 0.843  margin 0.182  ±0.011
```

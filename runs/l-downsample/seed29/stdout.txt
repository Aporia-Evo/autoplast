# Search seed 29

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 613586  time: 568s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1268 candidates
* decayed linear attention: 2420 candidates
* linear attention: 47860 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 50548 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 47860 candidates

## Best rule

```
S' = (|tanh(v)|·(((S - ((tanh(v) - norm(tanh(v))))⊗((tanh(v) - norm(tanh(v))))))ᵀ + (k)⊗(tanh(norm(tanh(v))))))ᵀ

Effective program (12 instructions):
  V3 = Tanh(V1)
  V2 = Normalize(V3)
  V4 = VecSub(V3, V2)
  V1 = Tanh(V2)
  M2 = Outer(V4, V4)
  M3 = MatSub(M0, M2)
  M1 = Outer(V0, V1)
  M2 = Transpose(M3)
  M1 = MatAdd(M2, M1)
  s0 = Norm(V3)
  M2 = MatScale(s0, M1)
  M0 = Transpose(M2)

structure: linear attention  [a=0.952 b=0.907 c=-0.001 g=0.006, erase c/a=0.001, R²=0.9956, 384 steps]

train acc 0.818 ±0.013
test d16 T12 ow0.3: acc 0.787  margin 0.149  ±0.006
test d16 T12 ow0.0: acc 0.866  margin 0.185  ±0.004
test d16 T12 ow0.6: acc 0.647  margin 0.069  ±0.009
test d32 T24 ow0.3: acc 0.879  margin 0.226  ±0.005
test d8 T6 ow0.3: acc 0.635  margin 0.033  ±0.010
test d16 T64 K8 ow0.3: acc 0.449  margin -0.056  ±0.011
test d16 T128 K8 ow0.3: acc 0.446  margin -0.079  ±0.016
```

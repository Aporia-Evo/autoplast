# Search seed 25

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 883897  time: 423s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1780 candidates
* decayed linear attention: 2932 candidates
* linear attention: 14196 candidates
* delta rule: 3169780 candidates
* gated delta rule: 3170804 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 14196 candidates
- delta rule (beta=1) (acc 0.858): 3170676 candidates
- delta rule (beta=0.5) (acc 0.932): 3171060 candidates
- gated delta (alpha=0.9) (acc 0.729): 14196 candidates

## Best rule

```
S' = (((|tanh(v)|·(v - S·tanh(k)) + (v - 0)))⊗(|tanh(v)|·tanh(tanh(k))) + 1.110·S)

Effective program (14 instructions):
  V0 = Tanh(V0)
  V5 = MatVec(M0, V0)
  V5 = VecSub(V1, V5)
  V2 = VecSub(V1, V4)
  V1 = Tanh(V1)
  s2 = Norm(V1)
  s1 = 1.1101
  M3 = MatScale(s1, M0)
  V4 = VecScale(s2, V5)
  V2 = VecAdd(V4, V2)
  V4 = Tanh(V0)
  V3 = VecScale(s2, V4)
  M0 = Outer(V2, V3)
  M0 = MatAdd(M0, M3)

structure: gated delta rule  [a=1.110 b=1.691 c=-0.786 g=0.016, erase c/a=0.708, R²=0.9961, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.967  margin 0.308  ±0.003
test d16 T12 ow0.0: acc 0.954  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.303  ±0.004
test d32 T24 ow0.3: acc 0.975  margin 0.363  ±0.002
test d8 T6 ow0.3: acc 0.829  margin 0.131  ±0.008
test d16 T64 K8 ow0.3: acc 0.056  margin -0.548  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

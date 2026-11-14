# Search seed 7

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 952047  time: 1176s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4084 candidates
* linear, not error-correcting: 4980 candidates
* unclassified: 5236 candidates
* linear attention: 25844 candidates
* delta rule: 29044 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 25844 candidates
- delta rule (beta=1) (acc 0.858): 29044 candidates
- delta rule (beta=0.5) (acc 0.932): 29044 candidates
- gated delta (alpha=0.9) (acc 0.729): 25844 candidates

## Best rule

```
S' = ((0 + S) + σ(σ(0))·(tanh((v - tanh(S·tanh(k)))))⊗(norm(k)))

Effective program (12 instructions):
  M1 = MatAdd(M3, M0)
  V5 = Tanh(V0)
  V2 = MatVec(M0, V5)
  V0 = Normalize(V0)
  V2 = Tanh(V2)
  s2 = Sigmoid(s2)
  s1 = Sigmoid(s2)
  V4 = VecSub(V1, V2)
  V5 = Tanh(V4)
  M0 = Outer(V5, V0)
  M3 = MatScale(s1, M0)
  M0 = MatAdd(M1, M3)

structure: linear, not error-correcting  [a=1.000 b=0.588 c=-0.549 g=0.057, erase c/a=0.549, R²=0.9983, 384 steps]

train acc 0.931 ±0.009
test d16 T12 ow0.3: acc 0.921  margin 0.266  ±0.004
test d16 T12 ow0.0: acc 0.894  margin 0.236  ±0.004
test d16 T12 ow0.6: acc 0.941  margin 0.273  ±0.004
test d32 T24 ow0.3: acc 0.984  margin 0.359  ±0.002
test d8 T6 ow0.3: acc 0.784  margin 0.110  ±0.009
test d16 T64 K8 ow0.3: acc 0.843  margin 0.173  ±0.008
test d16 T128 K8 ow0.3: acc 0.838  margin 0.168  ±0.012
```

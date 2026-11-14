# Search seed 24

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 947556  time: 685s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 5236 candidates
* linear, not error-correcting: 6388 candidates
* unclassified: 8308 candidates
* linear attention: 12276 candidates
* gated delta rule: 78324 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 12276 candidates
- delta rule (beta=1) (acc 0.858): 56692 candidates
- delta rule (beta=0.5) (acc 0.932): 78324 candidates
- gated delta (alpha=0.9) (acc 0.729): 12276 candidates

## Best rule

```
S' = (-1.094·(0 - S) + ((v)⊗(norm(k)) - ((0 - S))((((tanh(k) - (0 ⊙ 0)) - (0 ⊙ 0)))⊗(-0.794·(tanh(k) - (0 ⊙ 0))))))

Effective program (15 instructions):
  s1 = -1.0936
  M2 = MatSub(M1, M0)
  V3 = Normalize(V0)
  M0 = Outer(V1, V3)
  V3 = Hadamard(V5, V2)
  V0 = Tanh(V0)
  V5 = VecSub(V0, V3)
  V3 = VecSub(V5, V3)
  s3 = -0.7943
  V4 = VecScale(s3, V5)
  M1 = Outer(V3, V4)
  M1 = MatMul(M2, M1)
  M3 = MatSub(M0, M1)
  M2 = MatScale(s1, M2)
  M0 = MatAdd(M2, M3)

structure: gated delta rule  [a=1.094 b=1.000 c=-0.718 g=0.005, erase c/a=0.657, R²=0.9995, 384 steps]

train acc 0.969 ±0.006
test d16 T12 ow0.3: acc 0.967  margin 0.302  ±0.003
test d16 T12 ow0.0: acc 0.954  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.294  ±0.004
test d32 T24 ow0.3: acc 0.976  margin 0.359  ±0.002
test d8 T6 ow0.3: acc 0.836  margin 0.135  ±0.008
test d16 T64 K8 ow0.3: acc 0.083  margin -0.474  ±0.006
test d16 T128 K8 ow0.3: acc 0.021  margin -0.639  ±0.004
```

# Search seed 27

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 708845  time: 341s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1652 candidates
* decayed linear attention: 2420 candidates
* linear, not error-correcting: 3188 candidates
* linear attention: 56820 candidates
* delta rule: 114036 candidates
* gated delta rule: 409844 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 56820 candidates
- delta rule (beta=1) (acc 0.858): 110836 candidates
- delta rule (beta=0.5) (acc 0.932): 114036 candidates
- gated delta (alpha=0.9) (acc 0.729): 56820 candidates

## Best rule

```
S' = (1.109·S + (((tanh(v) - S·k) + ((tanh(v) - S·k) + S·0.570·tanh(tanh(k)))))⊗(0.570·tanh(tanh(k))))

Effective program (14 instructions):
  V4 = MatVec(M0, V0)
  s2 = 0.5701
  V5 = Tanh(V0)
  V3 = Tanh(V5)
  V3 = VecScale(s2, V3)
  s3 = 1.1092
  V1 = Tanh(V1)
  V1 = VecSub(V1, V4)
  V0 = MatVec(M0, V3)
  V5 = VecAdd(V1, V0)
  V5 = VecAdd(V1, V5)
  M3 = Outer(V5, V3)
  M1 = MatScale(s3, M0)
  M0 = MatAdd(M1, M3)

structure: gated delta rule  [a=1.109 b=0.988 c=-0.769 g=0.006, erase c/a=0.693, R²=0.9961, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.968  margin 0.308  ±0.003
test d16 T12 ow0.0: acc 0.952  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.300  ±0.004
test d32 T24 ow0.3: acc 0.962  margin 0.341  ±0.003
test d8 T6 ow0.3: acc 0.834  margin 0.138  ±0.008
test d16 T64 K8 ow0.3: acc 0.050  margin -0.547  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

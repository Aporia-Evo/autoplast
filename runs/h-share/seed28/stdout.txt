# Search seed 28

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 900191  time: 574s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3956 candidates
* decayed linear attention: 4724 candidates
* linear, not error-correcting: 5236 candidates
* linear attention: 13684 candidates
* delta rule: 163444 candidates
* gated delta rule: 479988 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 13684 candidates
- delta rule (beta=1) (acc 0.858): 41716 candidates
- delta rule (beta=0.5) (acc 0.932): 163444 candidates
- gated delta (alpha=0.9) (acc 0.729): 13684 candidates

## Best rule

```
S' = (((0 + 0))⊗(norm((0 ⊙ norm(0)))) + (1.174·S + ((v - S·k))⊗(k)))

Effective program (12 instructions):
  V5 = MatVec(M0, V0)
  V1 = VecSub(V1, V5)
  V3 = VecAdd(V2, V3)
  M3 = Outer(V1, V0)
  s0 = 1.1744
  M0 = MatScale(s0, M0)
  M0 = MatAdd(M0, M3)
  V0 = Normalize(V2)
  V2 = Hadamard(V2, V0)
  V0 = Normalize(V2)
  M2 = Outer(V3, V0)
  M0 = MatAdd(M2, M0)

structure: gated delta rule  [a=1.174 b=1.000 c=-1.000 g=-0.000, erase c/a=0.852, R²=1.0000, 384 steps]

train acc 0.960 ±0.007
test d16 T12 ow0.3: acc 0.956  margin 0.314  ±0.003
test d16 T12 ow0.0: acc 0.938  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.954  margin 0.319  ±0.004
test d32 T24 ow0.3: acc 0.840  margin 0.234  ±0.006
test d8 T6 ow0.3: acc 0.842  margin 0.147  ±0.008
test d16 T64 K8 ow0.3: acc 0.021  margin -0.650  ±0.003
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

# Search seed 22

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 938256  time: 717s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 628 candidates
* linear, not error-correcting: 1908 candidates
* unclassified: 2676 candidates
* linear attention: 6132 candidates
* delta rule: 103924 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 6132 candidates
- delta rule (beta=1) (acc 0.858): 103924 candidates
- delta rule (beta=0.5) (acc 0.932): 123124 candidates
- gated delta (alpha=0.9) (acc 0.729): 6132 candidates

## Best rule

```
S' = (((norm((S·norm(k) + v)) - S·norm(k)))⊗(k) + (((v)⊗(norm(k)) + S) - 0))

Effective program (10 instructions):
  V4 = Normalize(V0)
  M2 = Outer(V1, V4)
  V5 = MatVec(M0, V4)
  V2 = VecAdd(V5, V1)
  M3 = MatAdd(M2, M0)
  M2 = MatSub(M3, M1)
  V2 = Normalize(V2)
  V3 = VecSub(V2, V5)
  M0 = Outer(V3, V0)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=1.000 b=1.696 c=-0.446 g=-0.172, erase c/a=0.446, R²=0.9789, 384 steps]

train acc 0.943 ±0.008
test d16 T12 ow0.3: acc 0.934  margin 0.258  ±0.004
test d16 T12 ow0.0: acc 0.942  margin 0.245  ±0.003
test d16 T12 ow0.6: acc 0.939  margin 0.254  ±0.005
test d32 T24 ow0.3: acc 0.986  margin 0.344  ±0.002
test d8 T6 ow0.3: acc 0.786  margin 0.106  ±0.009
test d16 T64 K8 ow0.3: acc 0.832  margin 0.160  ±0.008
test d16 T128 K8 ow0.3: acc 0.822  margin 0.154  ±0.012
```

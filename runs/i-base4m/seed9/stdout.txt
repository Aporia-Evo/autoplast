# Search seed 9

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1535116  time: 738s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2164 candidates
* linear, not error-correcting: 2804 candidates
* unclassified: 5492 candidates
* linear attention: 93044 candidates
* delta rule: 1299444 candidates
* gated delta rule: 1370996 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 93044 candidates
- delta rule (beta=1) (acc 0.858): 1299572 candidates
- delta rule (beta=0.5) (acc 0.932): 1349108 candidates
- gated delta (alpha=0.9) (acc 0.729): 93044 candidates

## Best rule

```
S' = 1.095·((tanh(0.681·(v - S·k)))⊗(k) - (0 - S))

Effective program (10 instructions):
  M2 = MatSub(M3, M0)
  V2 = MatVec(M0, V0)
  V2 = VecSub(V1, V2)
  s0 = 0.6810
  V5 = VecScale(s0, V2)
  V1 = Tanh(V5)
  M0 = Outer(V1, V0)
  M0 = MatSub(M0, M2)
  s0 = 1.0954
  M0 = MatScale(s0, M0)

structure: gated delta rule  [a=1.095 b=0.721 c=-0.715 g=0.034, erase c/a=0.653, R²=0.9992, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.967  margin 0.301  ±0.003
test d16 T12 ow0.0: acc 0.955  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.961  margin 0.290  ±0.004
test d32 T24 ow0.3: acc 0.957  margin 0.341  ±0.003
test d8 T6 ow0.3: acc 0.832  margin 0.137  ±0.008
test d16 T64 K8 ow0.3: acc 0.053  margin -0.539  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

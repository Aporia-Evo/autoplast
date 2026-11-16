# Search seed 11

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1658326  time: 2692s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1908 candidates
* linear, not error-correcting: 3060 candidates
* unclassified: 3060 candidates
* linear attention: 10484 candidates
* delta rule: 2836852 candidates
* gated delta rule: 3167732 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 10484 candidates
- delta rule (beta=1) (acc 0.858): 2421748 candidates
- delta rule (beta=0.5) (acc 0.932): 2840948 candidates
- gated delta (alpha=0.9) (acc 0.729): 10484 candidates

## Best rule

```
S' = ((v)⊗(k) - (1.099·(0 - S) - ((0 - S))(0.798·(k)⊗(k))))

Effective program (10 instructions):
  M1 = MatSub(M3, M0)
  M0 = Outer(V1, V0)
  M2 = Outer(V0, V0)
  s1 = 1.0994
  s2 = 0.7977
  M2 = MatScale(s2, M2)
  M2 = MatMul(M1, M2)
  M1 = MatScale(s1, M1)
  M1 = MatSub(M1, M2)
  M0 = MatSub(M0, M1)

structure: gated delta rule  [a=1.099 b=1.000 c=-0.798 g=0.000, erase c/a=0.726, R²=1.0000, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.311  ±0.003
test d16 T12 ow0.0: acc 0.948  margin 0.281  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.312  ±0.004
test d32 T24 ow0.3: acc 0.976  margin 0.363  ±0.002
test d8 T6 ow0.3: acc 0.838  margin 0.139  ±0.008
test d16 T64 K8 ow0.3: acc 0.087  margin -0.475  ±0.006
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

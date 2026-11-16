# Search seed 30

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1887383  time: 943s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 5620 candidates
* decayed linear attention: 6644 candidates
* linear, not error-correcting: 8692 candidates
* linear attention: 79220 candidates
* gated delta rule: 3355636 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 79220 candidates
- delta rule (beta=1) (acc 0.858): 2661236 candidates
- delta rule (beta=0.5) (acc 0.932): 2682612 candidates
- gated delta (alpha=0.9) (acc 0.729): 79220 candidates

## Best rule

```
S' = (((tanh(1.147·v) - S·tanh((tanh(1.147·v) + (k - tanh(tanh(1.147·v)))))))⊗(norm(tanh((tanh(1.147·v) + (k - tanh(tanh(1.147·v))))))) - 1.147·(0 - S))

Effective program (14 instructions):
  s2 = 1.1475
  M1 = MatSub(M1, M0)
  V1 = VecScale(s2, V1)
  V5 = Tanh(V1)
  V4 = Tanh(V5)
  V0 = VecSub(V0, V4)
  V1 = VecAdd(V5, V0)
  V4 = Tanh(V1)
  V2 = MatVec(M0, V4)
  V3 = VecSub(V5, V2)
  M1 = MatScale(s2, M1)
  V1 = Normalize(V4)
  M0 = Outer(V3, V1)
  M0 = MatSub(M0, M1)

structure: gated delta rule  [a=1.147 b=1.071 c=-0.950 g=0.008, erase c/a=0.828, R²=0.9931, 384 steps]

train acc 0.969 ±0.006
test d16 T12 ow0.3: acc 0.960  margin 0.315  ±0.003
test d16 T12 ow0.0: acc 0.939  margin 0.278  ±0.003
test d16 T12 ow0.6: acc 0.958  margin 0.318  ±0.004
test d32 T24 ow0.3: acc 0.912  margin 0.301  ±0.004
test d8 T6 ow0.3: acc 0.837  margin 0.142  ±0.008
test d16 T64 K8 ow0.3: acc 0.017  margin -0.683  ±0.003
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

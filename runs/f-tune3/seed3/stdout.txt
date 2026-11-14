# Search seed 3

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500120  real evaluations (after cache): 628010  time: 287s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 3

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1268 candidates
* linear, not error-correcting: 1911 candidates
* linear attention: 127502 candidates
* gated delta rule: 212130 candidates
* delta rule: 212592 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 127502 candidates
- delta rule (beta=1) (acc 0.858): 212592 candidates
- delta rule (beta=0.5) (acc 0.932): 212911 candidates
- gated delta (alpha=0.9) (acc 0.729): 126987 candidates

## Best rule

```
S' = (1.107·S - ((v + S·(0 - tanh(tanh(k)))))⊗(tanh((0 - tanh(tanh(k))))))

Effective program (10 instructions):
  V2 = Tanh(V0)
  V2 = Tanh(V2)
  V5 = VecSub(V5, V2)
  s2 = 1.1072
  V0 = MatVec(M0, V5)
  V1 = VecAdd(V1, V0)
  M0 = MatScale(s2, M0)
  V3 = Tanh(V5)
  M2 = Outer(V1, V3)
  M0 = MatSub(M0, M2)

structure: gated delta rule  [a=1.107 b=0.877 c=-0.800 g=0.012, erase c/a=0.722, R²=0.9933, 384 steps]

train acc 0.970 ±0.006
test d16 T12 ow0.3: acc 0.966  margin 0.310  ±0.003
test d16 T12 ow0.0: acc 0.947  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.307  ±0.004
test d32 T24 ow0.3: acc 0.979  margin 0.369  ±0.002
test d8 T6 ow0.3: acc 0.828  margin 0.133  ±0.008
test d16 T64 K8 ow0.3: acc 0.058  margin -0.531  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

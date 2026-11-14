# Search seed 3

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 977775  time: 674s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1268 candidates
* linear, not error-correcting: 2164 candidates
* linear attention: 19572 candidates
* delta rule: 52724 candidates
* gated delta rule: 195572 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 19572 candidates
- delta rule (beta=1) (acc 0.858): 51956 candidates
- delta rule (beta=0.5) (acc 0.932): 119412 candidates
- gated delta (alpha=0.9) (acc 0.729): 19572 candidates

## Best rule

```
S' = (1.092·(0 + S) - σ(σ(1.092))·((1.092·(0 + S)·(k + 0))⊗(k) - ((0 + (0 + v)))⊗((k + 0))))

Effective program (14 instructions):
  V2 = VecAdd(V5, V1)
  s1 = 1.0919
  V4 = VecAdd(V3, V2)
  M3 = MatAdd(M2, M0)
  M3 = MatScale(s1, M3)
  V5 = VecAdd(V0, V5)
  M1 = Outer(V4, V5)
  V5 = MatVec(M3, V5)
  s2 = Sigmoid(s1)
  s3 = Sigmoid(s2)
  M0 = Outer(V5, V0)
  M2 = MatSub(M0, M1)
  M2 = MatScale(s3, M2)
  M0 = MatSub(M3, M2)

structure: gated delta rule  [a=1.092 b=0.679 c=-0.741 g=-0.000, erase c/a=0.679, R²=1.0000, 384 steps]

train acc 0.969 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.306  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.302  ±0.004
test d32 T24 ow0.3: acc 0.977  margin 0.359  ±0.002
test d8 T6 ow0.3: acc 0.838  margin 0.138  ±0.008
test d16 T64 K8 ow0.3: acc 0.099  margin -0.445  ±0.007
test d16 T128 K8 ow0.3: acc 0.021  margin -0.633  ±0.004
```

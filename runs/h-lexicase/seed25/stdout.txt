# Search seed 25

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 805286  time: 815s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 4084 candidates
* decayed linear attention: 6388 candidates
* linear attention: 17652 candidates
* delta rule: 25076 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 17652 candidates
- delta rule (beta=1) (acc 0.858): 25076 candidates
- delta rule (beta=0.5) (acc 0.932): 27636 candidates
- gated delta (alpha=0.9) (acc 0.729): 17268 candidates

## Best rule

```
S' = (((S·tanh(k) - v))⊗(norm((norm(k) - k))) - ((((tanh(norm((norm(k) - k))) + 0.308·S·tanh(k)))⊗(tanh(norm((norm(k) - k)))))(1.040·(0 - S)) + 1.040·(0 - S)))

Effective program (18 instructions):
  V4 = Tanh(V0)
  s2 = 1.0398
  V5 = MatVec(M0, V4)
  M0 = MatSub(M1, M0)
  s3 = 0.3081
  V3 = VecSub(V5, V1)
  V2 = Normalize(V0)
  V0 = VecSub(V2, V0)
  M0 = MatScale(s2, M0)
  V2 = Normalize(V0)
  M2 = Outer(V3, V2)
  V1 = Tanh(V2)
  V5 = VecScale(s3, V5)
  V4 = VecAdd(V1, V5)
  M3 = Outer(V4, V1)
  M1 = MatMul(M3, M0)
  M3 = MatAdd(M1, M0)
  M0 = MatSub(M2, M3)

structure: unclassified  [a=1.057 b=0.485 c=-0.456 g=0.012, erase c/a=0.431, R²=0.9782, 384 steps]

train acc 0.948 ±0.008
test d16 T12 ow0.3: acc 0.935  margin 0.249  ±0.004
test d16 T12 ow0.0: acc 0.955  margin 0.253  ±0.003
test d16 T12 ow0.6: acc 0.894  margin 0.211  ±0.006
test d32 T24 ow0.3: acc 0.970  margin 0.319  ±0.003
test d8 T6 ow0.3: acc 0.772  margin 0.105  ±0.009
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

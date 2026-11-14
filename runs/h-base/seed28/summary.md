# Search seed 28

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 275266  time: 235s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3956 candidates
* decayed linear attention: 4724 candidates
* linear, not error-correcting: 5236 candidates
* linear attention: 8180 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 8180 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 8180 candidates

## Best rule

```
S' = ((0.952·(S + (v)⊗(k)) + (v)⊗(k)) - (((S + (v)⊗(k)))((v)⊗(k)))(0.952·(v)⊗(k)))

Effective program (9 instructions):
  M2 = Outer(V1, V0)
  M0 = MatAdd(M0, M2)
  M3 = MatMul(M0, M2)
  s1 = 0.9522
  M0 = MatScale(s1, M0)
  M1 = MatScale(s1, M2)
  M1 = MatMul(M3, M1)
  M2 = MatAdd(M0, M2)
  M0 = MatSub(M2, M1)

structure: unclassified  [a=0.952 b=1.891 c=-0.061 g=-0.021, erase c/a=0.064, R²=0.9847, 384 steps]

train acc 0.834 ±0.013
test d16 T12 ow0.3: acc 0.809  margin 0.160  ±0.006
test d16 T12 ow0.0: acc 0.867  margin 0.187  ±0.004
test d16 T12 ow0.6: acc 0.700  margin 0.097  ±0.009
test d32 T24 ow0.3: acc 0.869  margin 0.227  ±0.005
test d8 T6 ow0.3: acc 0.661  margin 0.046  ±0.010
test d16 T64 K8 ow0.3: acc 0.521  margin -0.020  ±0.011
test d16 T128 K8 ow0.3: acc 0.516  margin -0.042  ±0.016
```

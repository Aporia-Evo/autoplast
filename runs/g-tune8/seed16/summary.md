# Search seed 16

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500012  real evaluations (after cache): 1024689  time: 2134s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3188 candidates
* linear attention: 5372 candidates
* unclassified: 7556 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5372 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((v)⊗(norm(tanh((k + (k + k))))) + (P2)(S))
P2' = σ(0)·1.755·P1

Effective program (11 instructions):
  V3 = VecAdd(V0, V0)
  V0 = VecAdd(V0, V3)
  s3 = Sigmoid(s2)
  V0 = Tanh(V0)
  V5 = Normalize(V0)
  M3 = Outer(V1, V5)
  M2 = MatMul(M2, M0)
  M0 = MatAdd(M3, M2)
  s0 = 1.7552
  M3 = MatScale(s0, M1)
  M2 = MatScale(s3, M3)

structure: unclassified  [a=0.878 b=0.981 c=-0.000 g=0.000, erase c/a=0.000, R²=0.9631, 1408 steps]

train acc 0.514 ±0.014
test regime collision3: acc 0.514  margin -0.043  ±0.006
test d16 T12 ow0.3: acc 0.735  margin 0.127  ±0.007
test d16 T12 ow0.0: acc 0.712  margin 0.107  ±0.006
test d16 T12 ow0.6: acc 0.713  margin 0.108  ±0.009
test d32 T24 ow0.3: acc 0.636  margin 0.097  ±0.007
test d8 T6 ow0.3: acc 0.628  margin 0.027  ±0.010
test d16 T64 K8 ow0.3: acc 0.572  margin -0.013  ±0.011
test d16 T128 K8 ow0.3: acc 0.545  margin -0.031  ±0.016
```

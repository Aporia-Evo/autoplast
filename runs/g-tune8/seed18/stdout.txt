# Search seed 18

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500084  real evaluations (after cache): 816348  time: 1588s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2676 candidates
* unclassified: 4980 candidates
* linear attention: 6772 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6772 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = σ(<tanh((0 - norm(tanh(k)))), ((0 - norm(tanh(k))) - tanh(norm(tanh(k))))>)·((v)⊗(tanh(tanh(norm(tanh(norm(tanh(k))))))) + S)
P1' = (v)⊗(tanh(tanh(norm(tanh(norm(tanh(k)))))))

Effective program (14 instructions):
  V0 = Tanh(V0)
  V2 = Normalize(V0)
  V3 = Tanh(V2)
  V5 = VecSub(V5, V2)
  V0 = VecSub(V5, V3)
  V4 = Tanh(V5)
  s0 = Dot(V4, V0)
  V4 = Normalize(V3)
  V5 = Tanh(V4)
  V5 = Tanh(V5)
  M1 = Outer(V1, V5)
  M0 = MatAdd(M1, M0)
  s0 = Sigmoid(s0)
  M0 = MatScale(s0, M0)

structure: unclassified  [a=0.864 b=0.785 c=0.000 g=0.002, erase c/a=-0.000, R²=0.9858, 1408 steps]

train acc 0.511 ±0.014
test regime collision3: acc 0.512  margin -0.048  ±0.006
test d16 T12 ow0.3: acc 0.723  margin 0.120  ±0.007
test d16 T12 ow0.0: acc 0.693  margin 0.094  ±0.006
test d16 T12 ow0.6: acc 0.724  margin 0.112  ±0.009
test d32 T24 ow0.3: acc 0.623  margin 0.088  ±0.007
test d8 T6 ow0.3: acc 0.628  margin 0.028  ±0.010
test d16 T64 K8 ow0.3: acc 0.575  margin -0.015  ±0.011
test d16 T128 K8 ow0.3: acc 0.544  margin -0.035  ±0.016
```

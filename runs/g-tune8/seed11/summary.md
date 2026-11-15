# Search seed 11

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500084  real evaluations (after cache): 857483  time: 1466s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2564 candidates
* decayed linear attention: 3332 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 27684 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = (0.862·S - (v)⊗(tanh(((0 - k) + (0 - k)))))
P2' = (v)⊗(tanh(((0 - k) + (0 - k))))

Effective program (7 instructions):
  V5 = VecSub(V2, V0)
  V3 = VecAdd(V5, V5)
  s2 = 0.8618
  M0 = MatScale(s2, M0)
  V5 = Tanh(V3)
  M2 = Outer(V1, V5)
  M0 = MatSub(M0, M2)

structure: unclassified  [a=0.862 b=1.653 c=-0.000 g=0.004, erase c/a=0.000, R²=0.9862, 1408 steps]

train acc 0.510 ±0.014
test regime collision3: acc 0.509  margin -0.052  ±0.006
test d16 T12 ow0.3: acc 0.716  margin 0.116  ±0.007
test d16 T12 ow0.0: acc 0.684  margin 0.089  ±0.006
test d16 T12 ow0.6: acc 0.723  margin 0.113  ±0.009
test d32 T24 ow0.3: acc 0.597  margin 0.064  ±0.007
test d8 T6 ow0.3: acc 0.632  margin 0.029  ±0.010
test d16 T64 K8 ow0.3: acc 0.573  margin -0.017  ±0.011
test d16 T128 K8 ow0.3: acc 0.542  margin -0.037  ±0.016
```

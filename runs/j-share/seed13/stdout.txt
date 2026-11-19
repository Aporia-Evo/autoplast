# Search seed 13

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 958767  time: 3147s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* unclassified: 3060 candidates
* linear attention: 4340 candidates
* delta rule: 525556 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 4340 candidates
- delta rule (beta=1) (acc 0.578): 513652 candidates
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 171252 candidates

## Best rule

```
S' = (((v - (0.396·S + 0.396·S)·(0 + k)))⊗((0 + k)) + σ((<v, v> + 1/(0.396))·1/(0.396))·S)
P1' = σ((<v, v> + 1/(0.396))·1/(0.396))·S
P2' = 0.396·S

Effective program (15 instructions):
  V5 = VecAdd(V3, V0)
  s3 = Dot(V1, V1)
  V4 = VecAdd(V4, V0)
  s1 = 0.3958
  M2 = MatScale(s1, M0)
  M1 = MatAdd(M2, M2)
  V5 = MatVec(M1, V5)
  V1 = VecSub(V1, V5)
  M3 = Outer(V1, V4)
  s1 = Recip(s1)
  s3 = SAdd(s3, s1)
  s2 = SMul(s3, s1)
  s2 = Sigmoid(s2)
  M1 = MatScale(s2, M0)
  M0 = MatAdd(M3, M1)

structure: delta rule  [a=1.000 b=1.000 c=-0.792 g=-0.000, erase c/a=0.792, R²=1.0000, 1408 steps]

train acc 0.603 ±0.014
test regime collision3: acc 0.622  margin 0.020  ±0.006
test d16 T12 ow0.3: acc 0.897  margin 0.270  ±0.005
test d16 T12 ow0.0: acc 0.841  margin 0.216  ±0.005
test d16 T12 ow0.6: acc 0.937  margin 0.308  ±0.005
test d32 T24 ow0.3: acc 0.972  margin 0.364  ±0.002
test d8 T6 ow0.3: acc 0.782  margin 0.109  ±0.009
test d16 T64 K8 ow0.3: acc 0.854  margin 0.231  ±0.008
test d16 T128 K8 ow0.3: acc 0.863  margin 0.229  ±0.011
```

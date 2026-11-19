# Search seed 3

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 973241  time: 2926s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* decayed linear attention: 1268 candidates
* linear, not error-correcting: 1268 candidates
* gated delta rule: 117492 candidates
* delta rule: 1002740 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5620 candidates
- delta rule (beta=1) (acc 0.578): 433780 candidates
- delta rule (beta=0.5) (acc 0.617): 1002740 candidates
- gated delta (alpha=0.9) (acc 0.519): 117492 candidates

## Best rule

```
S' = (((1/((0.814 + 0.814)) + -1.015)·(v + P2·(0 + k)))⊗((0 + k)) - (-1.015·(((v + P2·(0 + k)))⊗((0 + k)) - P2) + 0))
P1' = ((1/((0.814 + 0.814)) + -1.015)·(v + P2·(0 + k)))⊗((0 + k))
P2' = -1.015·(((v + P2·(0 + k)))⊗((0 + k)) - P2)

Effective program (15 instructions):
  s1 = -1.0149
  V3 = VecAdd(V4, V0)
  V5 = MatVec(M2, V3)
  V0 = VecAdd(V1, V5)
  M0 = Outer(V0, V3)
  M2 = MatSub(M0, M2)
  M2 = MatScale(s1, M2)
  s0 = 0.8145
  s3 = SAdd(s0, s0)
  s3 = Recip(s3)
  s3 = SAdd(s3, s1)
  V5 = VecScale(s3, V0)
  M0 = MatAdd(M2, M3)
  M1 = Outer(V5, V3)
  M0 = MatSub(M1, M0)

structure: unclassified  [a=1.016 b=0.614 c=-0.610 g=0.003, erase c/a=0.601, R²=0.4824, 1408 steps]

train acc 0.618 ±0.014
test regime collision3: acc 0.634  margin 0.020  ±0.006
test d16 T12 ow0.3: acc 0.854  margin 0.225  ±0.005
test d16 T12 ow0.0: acc 0.780  margin 0.163  ±0.005
test d16 T12 ow0.6: acc 0.917  margin 0.267  ±0.005
test d32 T24 ow0.3: acc 0.945  margin 0.315  ±0.003
test d8 T6 ow0.3: acc 0.727  margin 0.074  ±0.009
test d16 T64 K8 ow0.3: acc 0.838  margin 0.211  ±0.008
test d16 T128 K8 ow0.3: acc 0.845  margin 0.204  ±0.011
```

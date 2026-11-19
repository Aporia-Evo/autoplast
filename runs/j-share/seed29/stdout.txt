# Search seed 29

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 935728  time: 2596s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* unclassified: 3956 candidates
* linear attention: 11508 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 10868 candidates
- delta rule (beta=1) (acc 0.578): 232692 candidates
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 45684 candidates

## Best rule

```
S' = (((0 - P2) + ((v + 0))⊗(k)) + ((P2 + ((v + 0))⊗(k))·σ((0 + 0))·(k + 0))⊗((k + 0)))
P1' = ((P2 + ((v + 0))⊗(k))·σ((0 + 0))·(k + 0))⊗((k + 0))
P2' = -1.017·(((0 - P2) + ((v + 0))⊗(k)) + ((P2 + ((v + 0))⊗(k))·σ((0 + 0))·(k + 0))⊗((k + 0)))

Effective program (14 instructions):
  V4 = VecAdd(V1, V3)
  s3 = SAdd(s3, s0)
  s0 = Sigmoid(s3)
  M0 = Outer(V4, V0)
  M1 = MatAdd(M2, M0)
  s2 = -1.0174
  M3 = MatSub(M3, M2)
  V1 = VecAdd(V0, V5)
  V4 = VecScale(s0, V1)
  V3 = MatVec(M1, V4)
  M1 = Outer(V3, V1)
  M3 = MatAdd(M3, M0)
  M0 = MatAdd(M3, M1)
  M2 = MatScale(s2, M0)

structure: unclassified  [a=1.017 b=1.499 c=-0.509 g=0.000, erase c/a=0.500, R²=0.8520, 1408 steps]

train acc 0.604 ±0.014
test regime collision3: acc 0.636  margin 0.040  ±0.006
test d16 T12 ow0.3: acc 0.922  margin 0.237  ±0.004
test d16 T12 ow0.0: acc 0.899  margin 0.214  ±0.004
test d16 T12 ow0.6: acc 0.938  margin 0.235  ±0.005
test d32 T24 ow0.3: acc 0.990  margin 0.320  ±0.002
test d8 T6 ow0.3: acc 0.749  margin 0.092  ±0.009
test d16 T64 K8 ow0.3: acc 0.763  margin 0.106  ±0.009
test d16 T128 K8 ow0.3: acc 0.667  margin 0.058  ±0.015
```

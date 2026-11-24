# Search seed 802

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 611236  time: 1152s  pop: 500  tournament: 10

commit: dce11aa  task seed: 802  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4084 candidates
* unclassified: 5364 candidates
* linear attention: 24692 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.408): 24692 candidates
- delta rule (beta=1) (acc 0.643): not reached
- delta rule (beta=0.5) (acc 0.672): not reached
- gated delta (alpha=0.9) (acc 0.583): 1143028 candidates

## Best rule

```
S' = ((v)⊗((k + tanh(k))) - <tanh(v), tanh(v)>·(P1 - S))
P1' = (-0.460 + <tanh(v), tanh(k)>)·P1
P2' = (P1 - S)

Effective program (12 instructions):
  V5 = Tanh(V1)
  M2 = MatSub(M1, M0)
  V2 = Tanh(V0)
  s3 = -0.4602
  V3 = VecAdd(V0, V2)
  s1 = Dot(V5, V2)
  s0 = Dot(V5, V5)
  M0 = Outer(V1, V3)
  M3 = MatScale(s0, M2)
  M0 = MatSub(M0, M3)
  s2 = SAdd(s3, s1)
  M1 = MatScale(s2, M1)

structure: unclassified  [a=0.890 b=1.950 c=0.010 g=0.003, erase c/a=-0.012, R²=0.8611, 1408 steps]

train acc 0.580 ±0.014
test regime collision3: acc 0.517  margin -0.034  ±0.006
test d16 T12 ow0.3: acc 0.751  margin 0.136  ±0.006
test d16 T12 ow0.0: acc 0.756  margin 0.134  ±0.005
test d16 T12 ow0.6: acc 0.699  margin 0.096  ±0.009
test d32 T24 ow0.3: acc 0.844  margin 0.213  ±0.005
test d8 T6 ow0.3: acc 0.629  margin 0.022  ±0.010
test d16 T64 K8 ow0.3: acc 0.573  margin -0.007  ±0.011
test d16 T128 K8 ow0.3: acc 0.564  margin -0.025  ±0.015
```

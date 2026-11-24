# Search seed 806

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 700853  time: 1147s  pop: 500  tournament: 10

commit: dce11aa  task seed: 806  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 6260 candidates
* decayed linear attention: 7028 candidates
* linear attention: 7668 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.392): 7668 candidates
- delta rule (beta=1) (acc 0.619): not reached
- delta rule (beta=0.5) (acc 0.646): not reached
- gated delta (alpha=0.9) (acc 0.537): not reached

## Best rule

```
S' = (σ((1/(<(tanh(tanh(v)) + k), v>) + <(tanh(tanh(v)) + k), v>))·S + σ((-0.145 + σ((1/(<(tanh(tanh(v)) + k), v>) + <(tanh(tanh(v)) + k), v>))))·(tanh(v))⊗(k))
P1' = σ((-0.145 + σ((1/(<(tanh(tanh(v)) + k), v>) + <(tanh(tanh(v)) + k), v>))))·(tanh(v))⊗(k)
P2' = σ((1/(<(tanh(tanh(v)) + k), v>) + <(tanh(tanh(v)) + k), v>))·S

Effective program (14 instructions):
  V4 = Tanh(V1)
  V2 = Tanh(V4)
  V5 = VecAdd(V2, V0)
  s3 = Dot(V5, V1)
  M1 = Outer(V4, V0)
  s1 = Recip(s3)
  s2 = SAdd(s1, s3)
  s0 = Sigmoid(s2)
  s2 = -0.1453
  M2 = MatScale(s0, M0)
  s3 = SAdd(s2, s0)
  s3 = Sigmoid(s3)
  M1 = MatScale(s3, M1)
  M0 = MatAdd(M2, M1)

structure: decayed linear attention  [a=0.892 b=0.644 c=-0.000 g=0.002, erase c/a=0.000, R²=0.9972, 1408 steps]

train acc 0.529 ±0.014
test regime collision3: acc 0.521  margin -0.035  ±0.006
test d16 T12 ow0.3: acc 0.748  margin 0.136  ±0.007
test d16 T12 ow0.0: acc 0.751  margin 0.132  ±0.006
test d16 T12 ow0.6: acc 0.720  margin 0.107  ±0.009
test d32 T24 ow0.3: acc 0.661  margin 0.116  ±0.007
test d8 T6 ow0.3: acc 0.639  margin 0.035  ±0.010
test d16 T64 K8 ow0.3: acc 0.577  margin -0.007  ±0.011
test d16 T128 K8 ow0.3: acc 0.556  margin -0.025  ±0.016
```

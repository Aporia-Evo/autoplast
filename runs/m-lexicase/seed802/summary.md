# Search seed 802

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 685903  time: 1158s  pop: 500  tournament: 10

commit: dce11aa  task seed: 802  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1524 candidates
* decayed linear attention: 2164 candidates
* linear attention: 8948 candidates
* gated delta rule: 65908 candidates
* delta rule: 67060 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.408): 8948 candidates
- delta rule (beta=1) (acc 0.643): 67060 candidates
- delta rule (beta=0.5) (acc 0.672): 74100 candidates
- gated delta (alpha=0.9) (acc 0.583): 65908 candidates

## Best rule

```
S' = (((σ(0)·P1·tanh(k) - 0.489·(S·tanh(k) - v)))⊗((tanh(k) + σ(0)·P1·tanh(k))) - (σ(0)·P1 - S))
P1' = (0.489·(S·tanh(k) - v))⊗((tanh(k) + σ(0)·P1·tanh(k)))
P2' = σ(0)·P1

Effective program (14 instructions):
  s2 = 0.4887
  V5 = Tanh(V0)
  V4 = MatVec(M0, V5)
  s3 = Sigmoid(s1)
  M2 = MatScale(s3, M1)
  M1 = MatSub(M2, M0)
  V3 = VecSub(V4, V1)
  V2 = VecScale(s2, V3)
  V0 = MatVec(M2, V5)
  V3 = VecSub(V0, V2)
  V5 = VecAdd(V5, V0)
  M0 = Outer(V3, V5)
  M0 = MatSub(M0, M1)
  M1 = Outer(V2, V5)

structure: unclassified  [a=1.007 b=0.470 c=-0.444 g=-0.005, erase c/a=0.441, R²=0.6076, 1408 steps]

train acc 0.697 ±0.013
test regime collision3: acc 0.652  margin 0.047  ±0.006
test d16 T12 ow0.3: acc 0.916  margin 0.253  ±0.004
test d16 T12 ow0.0: acc 0.883  margin 0.221  ±0.004
test d16 T12 ow0.6: acc 0.934  margin 0.258  ±0.005
test d32 T24 ow0.3: acc 0.976  margin 0.347  ±0.002
test d8 T6 ow0.3: acc 0.737  margin 0.090  ±0.009
test d16 T64 K8 ow0.3: acc 0.854  margin 0.193  ±0.008
test d16 T128 K8 ow0.3: acc 0.851  margin 0.188  ±0.011
```

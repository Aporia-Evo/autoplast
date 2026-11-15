# Search seed 2

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500052  real evaluations (after cache): 992287  time: 3301s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1268 candidates
* decayed linear attention: 2164 candidates
* linear attention: 4596 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 4596 candidates
- delta rule (beta=1) (acc 0.578): 594332 candidates
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 589668 candidates

## Best rule

```
S' = (((v)⊗(k) + S) - (P1)(0.177·S))
P1' = ((0.548·(0 - v) + ((v)⊗(k) + S)·k))⊗(((v)⊗(k) + S)·k)
P2' = ((v)⊗(k) + S)

Effective program (12 instructions):
  M2 = Outer(V1, V0)
  M2 = MatAdd(M2, M0)
  s0 = 0.1769
  M0 = MatScale(s0, M0)
  M1 = MatMul(M1, M0)
  V3 = VecSub(V3, V1)
  M0 = MatSub(M2, M1)
  V0 = MatVec(M2, V0)
  s3 = 0.5483
  V5 = VecScale(s3, V3)
  V1 = VecAdd(V5, V0)
  M1 = Outer(V1, V0)

structure: unclassified  [a=0.905 b=1.001 c=-0.031 g=-0.006, erase c/a=0.034, R²=0.8819, 1408 steps]

train acc 0.608 ±0.014
test regime collision3: acc 0.618  margin 0.024  ±0.006
test d16 T12 ow0.3: acc 0.902  margin 0.223  ±0.004
test d16 T12 ow0.0: acc 0.923  margin 0.227  ±0.003
test d16 T12 ow0.6: acc 0.884  margin 0.200  ±0.006
test d32 T24 ow0.3: acc 0.975  margin 0.312  ±0.002
test d8 T6 ow0.3: acc 0.723  margin 0.079  ±0.009
test d16 T64 K8 ow0.3: acc 0.739  margin 0.089  ±0.010
test d16 T128 K8 ow0.3: acc 0.695  margin 0.074  ±0.014
```

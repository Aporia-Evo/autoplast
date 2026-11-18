# Search seed 13

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 792477  time: 2608s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1140 candidates
* linear attention: 4340 candidates
* unclassified: 7668 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 4340 candidates
- delta rule (beta=1) (acc 0.578): 176628 candidates
- delta rule (beta=0.5) (acc 0.617): 196084 candidates
- gated delta (alpha=0.9) (acc 0.519): 150900 candidates

## Best rule

```
S' = (((v)⊗((k - 0)) + -0.997·(P1 - S)) + P2)
P1' = (tanh(σ(0.267)·-0.997·(P1 - S)·k))⊗((k - 0))
P2' = (P2)((v)⊗((k - 0)))

Effective program (14 instructions):
  s3 = -0.9965
  s2 = 0.2668
  M0 = MatSub(M1, M0)
  M1 = MatScale(s3, M0)
  V3 = VecSub(V0, V2)
  M3 = Outer(V1, V3)
  M0 = MatAdd(M3, M1)
  M0 = MatAdd(M0, M2)
  V0 = MatVec(M1, V0)
  s2 = Sigmoid(s2)
  V0 = VecScale(s2, V0)
  M2 = MatMul(M2, M3)
  V4 = Tanh(V0)
  M1 = Outer(V4, V3)

structure: unclassified  [a=0.926 b=1.001 c=-0.017 g=0.012, erase c/a=0.019, R²=0.7642, 1408 steps]

train acc 0.624 ±0.014
test regime collision3: acc 0.625  margin 0.034  ±0.006
test d16 T12 ow0.3: acc 0.890  margin 0.236  ±0.005
test d16 T12 ow0.0: acc 0.900  margin 0.228  ±0.004
test d16 T12 ow0.6: acc 0.871  margin 0.223  ±0.006
test d32 T24 ow0.3: acc 0.969  margin 0.338  ±0.003
test d8 T6 ow0.3: acc 0.702  margin 0.061  ±0.010
test d16 T64 K8 ow0.3: acc 0.803  margin 0.149  ±0.009
test d16 T128 K8 ow0.3: acc 0.791  margin 0.143  ±0.013
```

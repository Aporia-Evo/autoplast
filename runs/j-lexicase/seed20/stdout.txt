# Search seed 20

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 772833  time: 2421s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2292 candidates
* decayed linear attention: 3060 candidates
* linear attention: 9332 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 9332 candidates
- delta rule (beta=1) (acc 0.578): 236404 candidates
- delta rule (beta=0.5) (acc 0.617): 245748 candidates
- gated delta (alpha=0.9) (acc 0.519): 216436 candidates

## Best rule

```
S' = (((v)⊗(k) - (P2 - S)) + 0.731·((P2 - S) + S))
P1' = (v)⊗(k)
P2' = (((((v)⊗(k) - (P2 - S)) + 0.731·((P2 - S) + S)) - (v)⊗(k))·(tanh(k) + tanh(k)))⊗(tanh(k))

Effective program (12 instructions):
  V4 = Tanh(V0)
  M2 = MatSub(M2, M0)
  M0 = MatAdd(M2, M0)
  s0 = 0.7312
  M1 = Outer(V1, V0)
  V5 = VecAdd(V4, V4)
  M3 = MatScale(s0, M0)
  M2 = MatSub(M1, M2)
  M0 = MatAdd(M2, M3)
  M2 = MatSub(M0, M1)
  V0 = MatVec(M2, V5)
  M2 = Outer(V0, V4)

structure: unclassified  [a=0.943 b=1.001 c=-0.033 g=-0.001, erase c/a=0.036, R²=0.8038, 1408 steps]

train acc 0.622 ±0.014
test regime collision3: acc 0.629  margin 0.037  ±0.006
test d16 T12 ow0.3: acc 0.910  margin 0.238  ±0.004
test d16 T12 ow0.0: acc 0.903  margin 0.226  ±0.004
test d16 T12 ow0.6: acc 0.882  margin 0.216  ±0.006
test d32 T24 ow0.3: acc 0.979  margin 0.337  ±0.002
test d8 T6 ow0.3: acc 0.723  margin 0.081  ±0.009
test d16 T64 K8 ow0.3: acc 0.771  margin 0.122  ±0.009
test d16 T128 K8 ow0.3: acc 0.755  margin 0.110  ±0.013
```

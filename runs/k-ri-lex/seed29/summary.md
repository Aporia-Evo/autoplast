# Search seed 29

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 962484  time: 4854s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 356652 attempts, 219709 blocks inserted, 241043 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1908 candidates
* decayed linear attention: 2164 candidates
* delta rule: 233076 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6900 candidates
- delta rule (beta=1) (acc 0.578): 233076 candidates
- delta rule (beta=0.5) (acc 0.617): 233076 candidates
- gated delta (alpha=0.9) (acc 0.519): 47220 candidates

## Best rule

```
S' = (… + …)
P1' = …
P2' = -0.235·(((v + -0.235·S·k))⊗(k) - (P2 + 0.060·(v)⊗(S·k)))

Effective program (23 instructions):
  V3 = MatVec(M0, V0)
  M3 = Outer(V1, V3)
  s3 = 0.0603
  M3 = MatScale(s3, M3)
  M2 = MatAdd(M2, M3)
  s1 = -0.2354
  M1 = MatSub(M0, M1)
  V3 = VecScale(s1, V3)
  M3 = Outer(V0, V3)
  V1 = VecAdd(V1, V3)
  M0 = Outer(V1, V0)
  M0 = MatSub(M0, M2)
  M2 = MatScale(s1, M0)
  M3 = MatSub(M1, M3)
  M3 = MatMul(M2, M3)
  M1 = MatAdd(M1, M0)
  M1 = MatAdd(M1, M3)
  M3 = MatMul(M0, M2)
  M3 = MatScale(s3, M3)
  M1 = MatAdd(M1, M3)
  M0 = MatMul(M2, M0)
  M1 = MatAdd(M1, M0)
  M0 = MatAdd(M1, M1)

structure: unclassified  [a=1.005 b=2.669 c=-0.588 g=0.088, erase c/a=0.585, R²=0.4184, 1408 steps]

train acc 0.710 ±0.013
test regime collision3: acc 0.682  margin 0.084  ±0.006
test d16 T12 ow0.3: acc 0.897  margin 0.255  ±0.005
test d16 T12 ow0.0: acc 0.872  margin 0.226  ±0.004
test d16 T12 ow0.6: acc 0.885  margin 0.229  ±0.006
test d32 T24 ow0.3: acc 0.962  margin 0.351  ±0.003
test d8 T6 ow0.3: acc 0.721  margin 0.071  ±0.009
test d16 T64 K8 ow0.3: acc 0.793  margin 0.142  ±0.009
test d16 T128 K8 ow0.3: acc 0.779  margin 0.129  ±0.013
```

# Search seed 17

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 838382  time: 3488s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 450036 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2164 candidates
* decayed linear attention: 3060 candidates
* linear attention: 6516 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6516 candidates
- delta rule (beta=1) (acc 0.578): 362228 candidates
- delta rule (beta=0.5) (acc 0.617): 367476 candidates
- gated delta (alpha=0.9) (acc 0.519): 88180 candidates

## Best rule

```
S' = (((((v + v))⊗((k + σ(2.089)·k)) + ((v + v))⊗((k + σ(2.089)·k))) - (P1 - P2)) + ((P1 - P2))((σ(2.089)·k)⊗(k)))
P1' = ((P1 - P2) - ((P1 - P2) + (((((v + v))⊗((k + σ(2.089)·k)) + ((v + v))⊗((k + σ(2.089)·k))) - (P1 - P2)) + ((P1 - P2))((σ(2.089)·k)⊗(k)))))
P2' = ((<σ(2.089)·k, σ(2.089)·k>·P2 + ((v + v))⊗((k + σ(2.089)·k))) + (((v + v))⊗((k + σ(2.089)·k)) + ((v + v))⊗((k + σ(2.089)·k))))

Effective program (18 instructions):
  s3 = 2.0893
  s2 = Sigmoid(s3)
  V4 = VecScale(s2, V0)
  s0 = Dot(V4, V4)
  M3 = Outer(V4, V0)
  V3 = VecAdd(V0, V4)
  V1 = VecAdd(V1, V1)
  M0 = Outer(V1, V3)
  M1 = MatSub(M1, M2)
  M2 = MatScale(s0, M2)
  M2 = MatAdd(M2, M0)
  M0 = MatAdd(M0, M0)
  M2 = MatAdd(M2, M0)
  M3 = MatMul(M1, M3)
  M0 = MatSub(M0, M1)
  M0 = MatAdd(M0, M3)
  M3 = MatAdd(M1, M0)
  M1 = MatSub(M1, M3)

structure: unclassified  [a=1.074 b=7.568 c=-0.950 g=-0.000, erase c/a=0.885, R²=0.8413, 1408 steps]

train acc 0.731 ±0.013
test regime collision3: acc 0.720  margin 0.118  ±0.006
test d16 T12 ow0.3: acc 0.954  margin 0.291  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.277  ±0.003
test d16 T12 ow0.6: acc 0.939  margin 0.264  ±0.005
test d32 T24 ow0.3: acc 0.987  margin 0.378  ±0.002
test d8 T6 ow0.3: acc 0.853  margin 0.146  ±0.007
test d16 T64 K8 ow0.3: acc 0.864  margin 0.184  ±0.008
test d16 T128 K8 ow0.3: acc 0.873  margin 0.187  ±0.010
```

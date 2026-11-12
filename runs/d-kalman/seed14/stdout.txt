# Search seed 14

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 740911  time: 1837s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1396 candidates
* decayed linear attention: 1780 candidates
* linear attention: 4852 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 4852 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 744436 candidates

## Best rule

```
S' = ((P1 - P2) + (((v)⊗(k) + (v)⊗(k)) + (((v)⊗(k) + (v)⊗(k)) + ((v)⊗(k) - P2))))
P1' = σ(1.831)·((<v, (k + k)> + σ(0))·((v)⊗(k) + (v)⊗(k)) + ((P1 - P2) + (((v)⊗(k) + (v)⊗(k)) + (((v)⊗(k) + (v)⊗(k)) + ((v)⊗(k) - P2)))))
P2' = (((v)⊗(k) - P2) - ((v)⊗(k) - P2))

Effective program (17 instructions):
  M1 = MatSub(M1, M2)
  V3 = VecAdd(V0, V0)
  s2 = Dot(V1, V3)
  M0 = Outer(V1, V0)
  M3 = MatAdd(M0, M0)
  M2 = MatSub(M0, M2)
  M0 = MatAdd(M3, M2)
  s1 = Sigmoid(s1)
  M0 = MatAdd(M3, M0)
  s3 = SAdd(s2, s1)
  M2 = MatSub(M2, M2)
  M0 = MatAdd(M1, M0)
  M1 = MatScale(s3, M3)
  M1 = MatAdd(M1, M0)
  s0 = 1.8309
  s1 = Sigmoid(s0)
  M1 = MatScale(s1, M1)

structure: unclassified  [a=0.896 b=5.004 c=0.002 g=-0.001, erase c/a=-0.002, R²=0.9340, 1408 steps]

train acc 0.523 ±0.014
test regime collision3: acc 0.507  margin -0.051  ±0.006
test d16 T12 ow0.3: acc 0.718  margin 0.115  ±0.007
test d16 T12 ow0.0: acc 0.688  margin 0.095  ±0.006
test d16 T12 ow0.6: acc 0.706  margin 0.103  ±0.009
test d32 T24 ow0.3: acc 0.605  margin 0.072  ±0.007
test d8 T6 ow0.3: acc 0.616  margin 0.022  ±0.010
test d16 T64 K8 ow0.3: acc 0.553  margin -0.026  ±0.011
test d16 T128 K8 ow0.3: acc 0.538  margin -0.042  ±0.016
```

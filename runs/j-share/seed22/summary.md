# Search seed 22

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 957432  time: 2432s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 200052 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 4852 candidates
* decayed linear attention: 6260 candidates
* linear, not error-correcting: 7668 candidates
* linear attention: 15604 candidates
* delta rule: 18164 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 15604 candidates
- delta rule (beta=1) (acc 0.578): 18164 candidates
- delta rule (beta=0.5) (acc 0.617): 35060 candidates
- gated delta (alpha=0.9) (acc 0.519): 18164 candidates

## Best rule

```
S' = (σ(σ(1/(σ(1/(|k|)))))·((v - (S + ((0)⊗(0) - P2))·norm(tanh(tanh(k)))))⊗(k) + (S + ((0)⊗(0) - P2)))
P1' = (S + ((0)⊗(0) - P2))
P2' = ((0 - v))⊗(k)

Effective program (19 instructions):
  V4 = Tanh(V0)
  M3 = Outer(V2, V5)
  V2 = Tanh(V4)
  M3 = MatSub(M3, M2)
  M1 = MatAdd(M0, M3)
  V4 = Normalize(V2)
  V5 = MatVec(M1, V4)
  V2 = VecSub(V1, V5)
  M0 = Outer(V2, V0)
  V4 = VecSub(V3, V1)
  s1 = Norm(V0)
  s2 = Recip(s1)
  s0 = Sigmoid(s2)
  s0 = Recip(s0)
  s0 = Sigmoid(s0)
  s3 = Sigmoid(s0)
  M2 = MatScale(s3, M0)
  M0 = MatAdd(M2, M1)
  M2 = Outer(V4, V0)

structure: unclassified  [a=1.024 b=0.690 c=-0.690 g=0.002, erase c/a=0.674, R²=0.5360, 1408 steps]

train acc 0.657 ±0.014
test regime collision3: acc 0.668  margin 0.059  ±0.006
test d16 T12 ow0.3: acc 0.921  margin 0.265  ±0.004
test d16 T12 ow0.0: acc 0.874  margin 0.222  ±0.004
test d16 T12 ow0.6: acc 0.948  margin 0.277  ±0.004
test d32 T24 ow0.3: acc 0.980  margin 0.353  ±0.002
test d8 T6 ow0.3: acc 0.782  margin 0.111  ±0.009
test d16 T64 K8 ow0.3: acc 0.865  margin 0.206  ±0.008
test d16 T128 K8 ow0.3: acc 0.874  margin 0.204  ±0.010
```

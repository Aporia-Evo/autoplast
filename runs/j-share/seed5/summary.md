# Search seed 5

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 979873  time: 4540s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 100084 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4980 candidates
* unclassified: 6516 candidates
* linear attention: 7028 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 7028 candidates
- delta rule (beta=1) (acc 0.578): 15348 candidates
- delta rule (beta=0.5) (acc 0.617): 32500 candidates
- gated delta (alpha=0.9) (acc 0.519): 13556 candidates

## Best rule

```
S' = ((v)⊗(σ(σ(1/(0)))·norm(k)) + (((P2 - P1))(((0 + norm(k)))⊗(σ(σ(1/(0)))·norm(k))) + P1))
P1' = (((v)⊗(σ(σ(1/(0)))·norm(k)) + (((P2 - P1))(((0 + norm(k)))⊗(σ(σ(1/(0)))·norm(k))) + P1)) - (P2 - 1/(0)·(P2)ᵀ))
P2' = (σ(σ(1/(0))) + σ(σ(1/(0))))·-0.835·(v)⊗(σ(σ(1/(0)))·norm(k))

Effective program (20 instructions):
  s2 = Recip(s1)
  V4 = Normalize(V0)
  s0 = -0.8351
  V0 = VecAdd(V3, V4)
  s3 = Sigmoid(s2)
  M3 = Transpose(M2)
  M0 = MatScale(s2, M3)
  M3 = MatSub(M2, M0)
  s1 = Sigmoid(s3)
  V4 = VecScale(s1, V4)
  M0 = Outer(V0, V4)
  s1 = SAdd(s1, s1)
  M2 = MatSub(M2, M1)
  M2 = MatMul(M2, M0)
  M0 = MatAdd(M2, M1)
  M1 = Outer(V1, V4)
  M0 = MatAdd(M1, M0)
  M1 = MatScale(s0, M1)
  M2 = MatScale(s1, M1)
  M1 = MatSub(M0, M3)

structure: unclassified  [a=0.958 b=0.623 c=-0.624 g=-0.002, erase c/a=0.651, R²=0.3583, 1408 steps]

train acc 0.672 ±0.013
test regime collision3: acc 0.690  margin 0.072  ±0.006
test d16 T12 ow0.3: acc 0.943  margin 0.281  ±0.003
test d16 T12 ow0.0: acc 0.910  margin 0.251  ±0.004
test d16 T12 ow0.6: acc 0.944  margin 0.272  ±0.004
test d32 T24 ow0.3: acc 0.988  margin 0.367  ±0.002
test d8 T6 ow0.3: acc 0.828  margin 0.129  ±0.008
test d16 T64 K8 ow0.3: acc 0.859  margin 0.181  ±0.008
test d16 T128 K8 ow0.3: acc 0.861  margin 0.180  ±0.011
```

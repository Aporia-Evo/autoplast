# Search seed 12

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 930251  time: 2639s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 150004 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3572 candidates
* decayed linear attention: 4212 candidates
* linear attention: 29428 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 29428 candidates
- delta rule (beta=1) (acc 0.578): 102132 candidates
- delta rule (beta=0.5) (acc 0.617): 103028 candidates
- gated delta (alpha=0.9) (acc 0.519): 102132 candidates

## Best rule

```
S' = (P1 + ((P1 + (v)⊗((0 + k))) + ((S + (S·(0 - norm(tanh((0 + k)))))⊗(tanh((0 + k)))) - P1)))
P1' = σ((0 + σ(<norm(tanh((0 + k))), (0 + k)>)))·(P1 + (v)⊗((0 + k)))
P2' = ((P1 + (v)⊗((0 + k))) + ((S + (S·(0 - norm(tanh((0 + k)))))⊗(tanh((0 + k)))) - P1))

Effective program (17 instructions):
  V4 = VecAdd(V2, V0)
  V0 = Tanh(V4)
  M2 = Outer(V1, V4)
  V1 = Normalize(V0)
  V2 = VecSub(V3, V1)
  V2 = MatVec(M0, V2)
  M3 = MatAdd(M1, M2)
  s3 = Dot(V1, V4)
  s3 = Sigmoid(s3)
  s0 = SAdd(s0, s3)
  M2 = Outer(V2, V0)
  s2 = Sigmoid(s0)
  M2 = MatAdd(M0, M2)
  M2 = MatSub(M2, M1)
  M2 = MatAdd(M3, M2)
  M0 = MatAdd(M1, M2)
  M1 = MatScale(s2, M3)

structure: unclassified  [a=1.034 b=1.006 c=-0.874 g=0.001, erase c/a=0.845, R²=0.7697, 1408 steps]

train acc 0.644 ±0.014
test regime collision3: acc 0.663  margin 0.074  ±0.006
test d16 T12 ow0.3: acc 0.882  margin 0.232  ±0.005
test d16 T12 ow0.0: acc 0.822  margin 0.188  ±0.005
test d16 T12 ow0.6: acc 0.910  margin 0.243  ±0.005
test d32 T24 ow0.3: acc 0.947  margin 0.331  ±0.003
test d8 T6 ow0.3: acc 0.652  margin 0.041  ±0.010
test d16 T64 K8 ow0.3: acc 0.873  margin 0.221  ±0.007
test d16 T128 K8 ow0.3: acc 0.891  margin 0.225  ±0.010
```

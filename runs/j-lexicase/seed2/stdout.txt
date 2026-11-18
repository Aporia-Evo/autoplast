# Search seed 2

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 905995  time: 2381s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 900084 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 756 candidates
* unclassified: 4084 candidates
* linear attention: 8180 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8052 candidates
- delta rule (beta=1) (acc 0.578): 234484 candidates
- delta rule (beta=0.5) (acc 0.617): 235252 candidates
- gated delta (alpha=0.9) (acc 0.519): 233076 candidates

## Best rule

```
S' = (σ(2.247)·((v + P2·k))⊗((k - 0)) - P2)
P1' = ((σ(2.247)·((v + P2·k))⊗((k - 0)) - P2) + ((1.163 + 2.247)·(v)⊗(1.163·((k - 0) + k)) + (P2 + P1)))
P2' = (σ(1.163)·((1.163 + 2.247)·(v)⊗(1.163·((k - 0) + k)) + (P2 + P1)) - ((σ(2.247)·((v + P2·k))⊗((k - 0)) - P2) + ((1.163 + 2.247)·(v)⊗(1.163·((k - 0) + k)) + (P2 + P1))))

Effective program (20 instructions):
  s1 = 2.2466
  V3 = MatVec(M2, V0)
  V5 = VecSub(V0, V5)
  V3 = VecAdd(V1, V3)
  M1 = MatAdd(M2, M1)
  M0 = Outer(V3, V5)
  s3 = Sigmoid(s1)
  M3 = MatScale(s3, M0)
  M0 = MatSub(M3, M2)
  s0 = 1.1628
  V2 = VecAdd(V5, V0)
  V2 = VecScale(s0, V2)
  M3 = Outer(V1, V2)
  s1 = SAdd(s0, s1)
  M3 = MatScale(s1, M3)
  M2 = MatAdd(M3, M1)
  M1 = MatAdd(M0, M2)
  s2 = Sigmoid(s0)
  M3 = MatScale(s2, M2)
  M2 = MatSub(M3, M1)

structure: unclassified  [a=1.070 b=0.906 c=-0.963 g=-0.000, erase c/a=0.900, R²=0.7945, 1408 steps]

train acc 0.732 ±0.013
test regime collision3: acc 0.721  margin 0.116  ±0.006
test d16 T12 ow0.3: acc 0.955  margin 0.289  ±0.003
test d16 T12 ow0.0: acc 0.942  margin 0.272  ±0.003
test d16 T12 ow0.6: acc 0.943  margin 0.266  ±0.004
test d32 T24 ow0.3: acc 0.984  margin 0.377  ±0.002
test d8 T6 ow0.3: acc 0.847  margin 0.141  ±0.008
test d16 T64 K8 ow0.3: acc 0.869  margin 0.191  ±0.007
test d16 T128 K8 ow0.3: acc 0.881  margin 0.195  ±0.010
```

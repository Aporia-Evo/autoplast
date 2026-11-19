# Search seed 8

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 983172  time: 3170s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 700020 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3828 candidates
* decayed linear attention: 4596 candidates
* linear attention: 37492 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 34804 candidates
- delta rule (beta=1) (acc 0.578): 59380 candidates
- delta rule (beta=0.5) (acc 0.617): 261108 candidates
- gated delta (alpha=0.9) (acc 0.519): 41204 candidates

## Best rule

```
S' = ((0·P1·v)⊗(0) + (σ((0·0 + (0 + 0·0)))·((v)⊗(tanh(k)) + P1) - (P2 - S)))
P1' = σ((0·0 + (0 + 0·0)))·((v)⊗(tanh(k)) + P1)
P2' = ((σ((0·0 + (0 + 0·0)))·((v)⊗(tanh(k)) + P1) - (P2 - S))·tanh(k))⊗(tanh(k))

Effective program (16 instructions):
  M0 = MatSub(M2, M0)
  V0 = Tanh(V0)
  s0 = SMul(s0, s0)
  s2 = SAdd(s2, s0)
  s0 = SAdd(s0, s2)
  s0 = Sigmoid(s0)
  V3 = MatVec(M1, V1)
  M3 = Outer(V1, V0)
  M2 = MatAdd(M3, M1)
  V4 = VecScale(s1, V3)
  M1 = MatScale(s0, M2)
  M2 = MatSub(M1, M0)
  M3 = Outer(V4, V2)
  V1 = MatVec(M2, V0)
  M0 = MatAdd(M3, M2)
  M2 = Outer(V1, V0)

structure: unclassified  [a=0.833 b=0.473 c=-0.038 g=0.021, erase c/a=0.046, R²=0.4178, 1408 steps]

train acc 0.631 ±0.014
test regime collision3: acc 0.640  margin 0.043  ±0.006
test d16 T12 ow0.3: acc 0.911  margin 0.257  ±0.004
test d16 T12 ow0.0: acc 0.866  margin 0.219  ±0.004
test d16 T12 ow0.6: acc 0.914  margin 0.257  ±0.005
test d32 T24 ow0.3: acc 0.965  margin 0.356  ±0.003
test d8 T6 ow0.3: acc 0.729  margin 0.078  ±0.009
test d16 T64 K8 ow0.3: acc 0.832  margin 0.196  ±0.008
test d16 T128 K8 ow0.3: acc 0.860  margin 0.196  ±0.011
```

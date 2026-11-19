# Search seed 24

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 915446  time: 2977s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 400116 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 628 candidates
* unclassified: 3188 candidates
* linear attention: 8820 candidates
* delta rule: 337780 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8564 candidates
- delta rule (beta=1) (acc 0.578): 26612 candidates
- delta rule (beta=0.5) (acc 0.617): 337780 candidates
- gated delta (alpha=0.9) (acc 0.519): 26612 candidates

## Best rule

```
S' = (((v)⊗(k) - ((S + P2)·(k + 0))⊗(σ(σ(0))·(k + 0))) + (S + P2))
P1' = (v)⊗(k)
P2' = ((v - (0 ⊙ v)))⊗(norm(tanh((k + 0))))

Effective program (15 instructions):
  V5 = VecAdd(V0, V3)
  M1 = Outer(V1, V0)
  M2 = MatAdd(M0, M2)
  s3 = Sigmoid(s2)
  s3 = Sigmoid(s3)
  V0 = Tanh(V5)
  V2 = Hadamard(V3, V1)
  V4 = VecSub(V1, V2)
  V3 = MatVec(M2, V5)
  V2 = VecScale(s3, V5)
  M3 = Outer(V3, V2)
  M3 = MatSub(M1, M3)
  M0 = MatAdd(M3, M2)
  V1 = Normalize(V0)
  M2 = Outer(V4, V1)

structure: unclassified  [a=1.028 b=1.002 c=-0.625 g=0.002, erase c/a=0.608, R²=0.6330, 1408 steps]

train acc 0.653 ±0.014
test regime collision3: acc 0.667  margin 0.061  ±0.006
test d16 T12 ow0.3: acc 0.928  margin 0.266  ±0.004
test d16 T12 ow0.0: acc 0.885  margin 0.230  ±0.004
test d16 T12 ow0.6: acc 0.947  margin 0.272  ±0.004
test d32 T24 ow0.3: acc 0.980  margin 0.353  ±0.002
test d8 T6 ow0.3: acc 0.803  margin 0.117  ±0.008
test d16 T64 K8 ow0.3: acc 0.864  margin 0.192  ±0.008
test d16 T128 K8 ow0.3: acc 0.863  margin 0.189  ±0.011
```

# Search seed 31

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 967643  time: 549s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 6388 candidates
* decayed linear attention: 8052 candidates
* linear attention: 18548 candidates
* delta rule: 50932 candidates
* gated delta rule: 937460 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 20212 candidates
- delta rule (beta=1) (acc 0.858): 24052 candidates
- delta rule (beta=0.5) (acc 0.932): 52084 candidates
- gated delta (alpha=0.9) (acc 0.729): 18292 candidates

## Best rule

```
S' = (1.115·(σ(0.880)·(((1.115·S + 0) + 0)·tanh(k) - v))⊗(norm(((0·0 ⊙ norm(k)) - norm(k)))) + 1.115·S)

Effective program (18 instructions):
  s1 = 1.1154
  V4 = Tanh(V0)
  M2 = MatScale(s1, M0)
  V3 = Normalize(V0)
  M3 = MatAdd(M2, M3)
  s0 = 0.8802
  M1 = MatAdd(M3, M1)
  V5 = MatVec(M1, V4)
  V5 = VecSub(V5, V1)
  s3 = Sigmoid(s0)
  V0 = VecScale(s3, V5)
  V1 = VecScale(s2, V2)
  V4 = Hadamard(V1, V3)
  V5 = VecSub(V4, V3)
  V4 = Normalize(V5)
  M3 = Outer(V0, V4)
  M1 = MatScale(s1, M3)
  M0 = MatAdd(M1, M2)

structure: gated delta rule  [a=1.115 b=0.788 c=-0.836 g=0.003, erase c/a=0.749, R²=0.9997, 384 steps]

train acc 0.964 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.314  ±0.003
test d16 T12 ow0.0: acc 0.949  margin 0.283  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.314  ±0.004
test d32 T24 ow0.3: acc 0.966  margin 0.349  ±0.003
test d8 T6 ow0.3: acc 0.842  margin 0.142  ±0.008
test d16 T64 K8 ow0.3: acc 0.052  margin -0.559  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

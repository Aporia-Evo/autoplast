# Search seed 27

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 875058  time: 1028s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2164 candidates
* decayed linear attention: 2676 candidates
* linear, not error-correcting: 4596 candidates
* linear attention: 7924 candidates
* delta rule: 66420 candidates
* gated delta rule: 232692 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 7924 candidates
- delta rule (beta=1) (acc 0.858): 37620 candidates
- delta rule (beta=0.5) (acc 0.932): 68980 candidates
- gated delta (alpha=0.9) (acc 0.729): 7924 candidates

## Best rule

```
S' = (σ(0.960)·S - ((σ(0.960)·S)((k)⊗(k)) - σ((<(σ(0.960)·S)((k)⊗(k))·(tanh(k) + σ(0.960)·S·(0.960·v - tanh(k))), (σ(0.960)·S)((k)⊗(k))·(tanh(k) + σ(0.960)·S·(0.960·v - tanh(k)))> + <(σ(0.960)·S)((k)⊗(k))·(tanh(k) + σ(0.960)·S·(0.960·v - tanh(k))), (σ(0.960)·S)((k)⊗(k))·(tanh(k) + σ(0.960)·S·(0.960·v - tanh(k)))>))·(σ(0.960)·S + (0.960·v)⊗(tanh(k)))))

Effective program (19 instructions):
  s1 = 0.9597
  V2 = VecScale(s1, V1)
  s2 = Sigmoid(s1)
  M0 = MatScale(s2, M0)
  M1 = Outer(V0, V0)
  M3 = MatMul(M0, M1)
  V3 = Tanh(V0)
  V1 = VecSub(V2, V3)
  V0 = MatVec(M0, V1)
  M1 = Outer(V2, V3)
  V3 = VecAdd(V3, V0)
  V1 = MatVec(M3, V3)
  s1 = Dot(V1, V1)
  s1 = SAdd(s1, s1)
  M2 = MatAdd(M0, M1)
  s3 = Sigmoid(s1)
  M2 = MatScale(s3, M2)
  M1 = MatSub(M3, M2)
  M0 = MatSub(M0, M1)

structure: unclassified  [a=1.127 b=0.495 c=-0.693 g=-0.038, erase c/a=0.615, R²=0.9842, 384 steps]

train acc 0.981 ±0.005
test d16 T12 ow0.3: acc 0.971  margin 0.298  ±0.003
test d16 T12 ow0.0: acc 0.953  margin 0.278  ±0.003
test d16 T12 ow0.6: acc 0.955  margin 0.276  ±0.004
test d32 T24 ow0.3: acc 0.764  margin 0.193  ±0.006
test d8 T6 ow0.3: acc 0.836  margin 0.136  ±0.008
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

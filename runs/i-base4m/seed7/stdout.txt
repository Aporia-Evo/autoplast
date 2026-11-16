# Search seed 7

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 2157102  time: 1103s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4084 candidates
* linear, not error-correcting: 4980 candidates
* unclassified: 5876 candidates
* gated delta rule: 39028 candidates
* linear attention: 52212 candidates
* delta rule: 440436 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 52212 candidates
- delta rule (beta=1) (acc 0.858): 439924 candidates
- delta rule (beta=0.5) (acc 0.932): 440436 candidates
- gated delta (alpha=0.9) (acc 0.729): 48244 candidates

## Best rule

```
S' = ((σ((σ(<(0 - S)·tanh(k), (0 - S)·tanh(k)>) + σ(<(0 - S)·tanh(k), (0 - S)·tanh(k)>)))·((0 - S)·tanh(k) + tanh(v)))⊗(norm(tanh(k))) - 1.119·(0 - S))

Effective program (15 instructions):
  V5 = Tanh(V0)
  M3 = MatSub(M1, M0)
  V3 = MatVec(M3, V5)
  V2 = Tanh(V1)
  s3 = 1.1190
  V0 = VecAdd(V3, V2)
  s2 = Dot(V3, V3)
  s0 = Sigmoid(s2)
  s2 = SAdd(s0, s0)
  s0 = Sigmoid(s2)
  V3 = VecScale(s0, V0)
  V4 = Normalize(V5)
  M0 = Outer(V3, V4)
  M1 = MatScale(s3, M3)
  M0 = MatSub(M0, M1)

structure: gated delta rule  [a=1.119 b=0.724 c=-0.756 g=0.001, erase c/a=0.676, R²=0.9965, 384 steps]

train acc 0.977 ±0.005
test d16 T12 ow0.3: acc 0.971  margin 0.307  ±0.003
test d16 T12 ow0.0: acc 0.955  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.299  ±0.004
test d32 T24 ow0.3: acc 0.973  margin 0.349  ±0.002
test d8 T6 ow0.3: acc 0.836  margin 0.138  ±0.008
test d16 T64 K8 ow0.3: acc 0.052  margin -0.558  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

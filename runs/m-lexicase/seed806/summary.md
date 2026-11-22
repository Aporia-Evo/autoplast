# Search seed 806

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 690618  time: 1167s  pop: 500  tournament: 10

commit: dce11aa  task seed: 806  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 756 candidates
* unclassified: 2932 candidates
* linear attention: 5748 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.392): 5748 candidates
- delta rule (beta=1) (acc 0.619): not reached
- delta rule (beta=0.5) (acc 0.646): not reached
- gated delta (alpha=0.9) (acc 0.537): 45044 candidates

## Best rule

```
S' = ((v)⊗(k) + P2)
P2' = ((P2·tanh(tanh(k)))⊗(tanh(((v)⊗(k)·tanh(v) - k))) + σ((1/((σ(0) + <((v)⊗(k)·tanh(v) - k), tanh(P2·tanh(tanh(k)))>)) + σ(0)))·((v)⊗(k) + P2))

Effective program (19 instructions):
  M0 = Outer(V1, V0)
  s1 = Sigmoid(s1)
  V4 = Tanh(V1)
  V1 = MatVec(M0, V4)
  V5 = Tanh(V0)
  V2 = Tanh(V5)
  V4 = MatVec(M2, V2)
  M0 = MatAdd(M0, M2)
  V2 = VecSub(V1, V0)
  V1 = Tanh(V4)
  s0 = Dot(V2, V1)
  s3 = SAdd(s1, s0)
  s2 = Recip(s3)
  s3 = SAdd(s2, s1)
  s3 = Sigmoid(s3)
  M2 = MatScale(s3, M0)
  V0 = Tanh(V2)
  M3 = Outer(V4, V0)
  M2 = MatAdd(M3, M2)

structure: unclassified  [a=0.690 b=1.001 c=0.019 g=0.005, erase c/a=-0.028, R²=0.4595, 1408 steps]

train acc 0.581 ±0.014
test regime collision3: acc 0.564  margin -0.063  ±0.006
test d16 T12 ow0.3: acc 0.773  margin 0.162  ±0.006
test d16 T12 ow0.0: acc 0.687  margin 0.087  ±0.006
test d16 T12 ow0.6: acc 0.861  margin 0.222  ±0.007
test d32 T24 ow0.3: acc 0.744  margin 0.191  ±0.007
test d8 T6 ow0.3: acc 0.686  margin 0.013  ±0.010
test d16 T64 K8 ow0.3: acc 0.698  margin 0.097  ±0.010
test d16 T128 K8 ow0.3: acc 0.696  margin 0.091  ±0.014
```

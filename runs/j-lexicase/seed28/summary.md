# Search seed 28

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 687079  time: 3617s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 550004 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3188 candidates
* unclassified: 6004 candidates
* linear attention: 8948 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8948 candidates
- delta rule (beta=1) (acc 0.578): 27124 candidates
- delta rule (beta=0.5) (acc 0.617): 34932 candidates
- gated delta (alpha=0.9) (acc 0.519): 26996 candidates

## Best rule

```
S' = (((S + P1) - σ(1.073)·((S + P1))((k)⊗(k))) + ((((v)⊗(k) + (v)⊗(k)) + ((v)⊗(k) + (v)⊗(k))) + (((v)⊗(k) + (v)⊗(k)) + ((v)⊗(k) + (v)⊗(k)))))
P1' = (((((v)⊗(k) + (v)⊗(k)) + ((v)⊗(k) + (v)⊗(k))) + (((v)⊗(k) + (v)⊗(k)) + ((v)⊗(k) + (v)⊗(k)))))(((k)⊗(k) + ((v)⊗(k) + (k)⊗(k))))
P2' = ((S + P1) - σ(1.073)·((S + P1))((k)⊗(k)))

Effective program (15 instructions):
  M0 = MatAdd(M0, M1)
  s1 = 1.0731
  s0 = Sigmoid(s1)
  M1 = Outer(V0, V0)
  M2 = MatMul(M0, M1)
  M3 = MatScale(s0, M2)
  M2 = MatSub(M0, M3)
  M0 = Outer(V1, V0)
  M3 = MatAdd(M0, M1)
  M3 = MatAdd(M1, M3)
  M0 = MatAdd(M0, M0)
  M0 = MatAdd(M0, M0)
  M0 = MatAdd(M0, M0)
  M1 = MatMul(M0, M3)
  M0 = MatAdd(M2, M0)

structure: unclassified  [a=1.042 b=8.018 c=-0.769 g=0.001, erase c/a=0.738, R²=0.5916, 1408 steps]

train acc 0.667 ±0.013
test regime collision3: acc 0.675  margin 0.063  ±0.006
test d16 T12 ow0.3: acc 0.925  margin 0.281  ±0.004
test d16 T12 ow0.0: acc 0.872  margin 0.233  ±0.004
test d16 T12 ow0.6: acc 0.951  margin 0.296  ±0.004
test d32 T24 ow0.3: acc 0.978  margin 0.368  ±0.002
test d8 T6 ow0.3: acc 0.823  margin 0.130  ±0.008
test d16 T64 K8 ow0.3: acc 0.862  margin 0.212  ±0.008
test d16 T128 K8 ow0.3: acc 0.878  margin 0.212  ±0.010
```

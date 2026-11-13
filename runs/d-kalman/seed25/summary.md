# Search seed 25

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 794268  time: 5477s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1140 candidates
* linear, not error-correcting: 2036 candidates
* unclassified: 6516 candidates
* linear attention: 8436 candidates
* delta rule: 828532 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8436 candidates
- delta rule (beta=1) (acc 0.578): 827252 candidates
- delta rule (beta=0.5) (acc 0.617): 828404 candidates
- gated delta (alpha=0.9) (acc 0.519): 40820 candidates

## Best rule

```
S' = (((v)⊗((k + k)))(((k + k))⊗((k + k))) + (((k + k))⊗(tanh(k)) + ((P2 + (S + (v)⊗((k + k)))) - 0.424·0.424·((P2 + (S + (v)⊗((k + k)))))(((k + k))⊗((k + k))))))
P1' = (((k + k))⊗(tanh(k)) + ((P2 + (S + (v)⊗((k + k)))) - 0.424·0.424·((P2 + (S + (v)⊗((k + k)))))(((k + k))⊗((k + k)))))
P2' = (((v)⊗((k + k)))(((k + k))⊗((k + k))))(((k + k))⊗(tanh(k)))

Effective program (16 instructions):
  V3 = VecAdd(V0, V0)
  M3 = Outer(V1, V3)
  M0 = MatAdd(M0, M3)
  M1 = MatAdd(M2, M0)
  M2 = Outer(V3, V3)
  M3 = MatMul(M3, M2)
  M0 = MatMul(M1, M2)
  s3 = 0.4243
  s2 = SMul(s3, s3)
  M0 = MatScale(s2, M0)
  M1 = MatSub(M1, M0)
  V0 = Tanh(V0)
  M2 = Outer(V3, V0)
  M1 = MatAdd(M2, M1)
  M0 = MatAdd(M3, M1)
  M2 = MatMul(M3, M2)

structure: unclassified  [a=1.043 b=8.547 c=-0.733 g=-0.001, erase c/a=0.703, R²=0.6053, 1408 steps]

train acc 0.667 ±0.013
test regime collision3: acc 0.672  margin 0.060  ±0.006
test d16 T12 ow0.3: acc 0.926  margin 0.276  ±0.004
test d16 T12 ow0.0: acc 0.878  margin 0.232  ±0.004
test d16 T12 ow0.6: acc 0.949  margin 0.288  ±0.004
test d32 T24 ow0.3: acc 0.980  margin 0.364  ±0.002
test d8 T6 ow0.3: acc 0.810  margin 0.124  ±0.008
test d16 T64 K8 ow0.3: acc 0.859  margin 0.204  ±0.008
test d16 T128 K8 ow0.3: acc 0.861  margin 0.204  ±0.011
```

# Search seed 5

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 796488  time: 1931s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4980 candidates
* unclassified: 993116 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 9404 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 1001188 candidates

## Best rule

```
S' = ((((tanh(0.852·v) + v))⊗((k)⊗(tanh(tanh(0.852·v)))·(tanh(0.852·v) + v)) + 0.852·S) + ((((tanh(0.852·v) + v))⊗((k)⊗(tanh(tanh(0.852·v)))·(tanh(0.852·v) + v)) + 0.852·S))((tanh(tanh(0.852·v)))⊗(tanh(tanh(0.852·v)))))
P1' = ((((tanh(0.852·v) + v))⊗((k)⊗(tanh(tanh(0.852·v)))·(tanh(0.852·v) + v)) + 0.852·S))((tanh(tanh(0.852·v)))⊗(tanh(tanh(0.852·v))))
P2' = (k)⊗(tanh(tanh(0.852·v)))

Effective program (13 instructions):
  s3 = 0.8515
  M1 = MatScale(s3, M0)
  V3 = VecScale(s3, V1)
  V4 = Tanh(V3)
  V2 = Tanh(V4)
  V4 = VecAdd(V4, V1)
  M2 = Outer(V0, V2)
  V0 = MatVec(M2, V4)
  M0 = Outer(V4, V0)
  M0 = MatAdd(M0, M1)
  M3 = Outer(V2, V2)
  M1 = MatMul(M0, M3)
  M0 = MatAdd(M0, M1)

structure: unclassified  [a=0.886 b=2.731 c=0.001 g=0.005, erase c/a=-0.002, R²=0.9067, 1408 steps]

train acc 0.517 ±0.014
test regime collision3: acc 0.503  margin -0.047  ±0.006
test d16 T12 ow0.3: acc 0.727  margin 0.121  ±0.007
test d16 T12 ow0.0: acc 0.717  margin 0.109  ±0.006
test d16 T12 ow0.6: acc 0.709  margin 0.100  ±0.009
test d32 T24 ow0.3: acc 0.604  margin 0.074  ±0.007
test d8 T6 ow0.3: acc 0.614  margin 0.023  ±0.010
test d16 T64 K8 ow0.3: acc 0.551  margin -0.022  ±0.011
test d16 T128 K8 ow0.3: acc 0.544  margin -0.038  ±0.016
```

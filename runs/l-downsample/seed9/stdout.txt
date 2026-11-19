# Search seed 9

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 588947  time: 1451s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3060 candidates
* decayed linear attention: 4468 candidates
* linear, not error-correcting: 6900 candidates
* linear attention: 18164 candidates
* delta rule: 854260 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 18164 candidates
- delta rule (beta=1) (acc 0.858): 853620 candidates
- delta rule (beta=0.5) (acc 0.932): 854900 candidates
- gated delta (alpha=0.9) (acc 0.729): 18164 candidates

## Best rule

```
S' = (((S)(((tanh(v))⊗(k) + (k)⊗(v))))((σ(-0.348)·((tanh(v))⊗(k) + (k)⊗(v)) - (tanh(v))⊗(k))) - ((v)⊗(k) - ((S + (tanh(v))⊗(k)) + (tanh(v))⊗(k))))

Effective program (15 instructions):
  s3 = -0.3478
  M2 = Outer(V0, V1)
  s3 = Sigmoid(s3)
  V2 = Tanh(V1)
  M1 = Outer(V2, V0)
  M3 = MatAdd(M1, M2)
  M2 = MatMul(M0, M3)
  M0 = MatAdd(M0, M1)
  M3 = MatScale(s3, M3)
  M3 = MatSub(M3, M1)
  M3 = MatMul(M2, M3)
  M0 = MatAdd(M0, M1)
  M1 = Outer(V1, V0)
  M1 = MatSub(M1, M0)
  M0 = MatSub(M3, M1)

structure: unclassified  [a=1.026 b=0.902 c=-0.566 g=0.016, erase c/a=0.552, R²=0.9507, 384 steps]

train acc 0.949 ±0.008
test d16 T12 ow0.3: acc 0.938  margin 0.269  ±0.004
test d16 T12 ow0.0: acc 0.912  margin 0.242  ±0.004
test d16 T12 ow0.6: acc 0.946  margin 0.267  ±0.004
test d32 T24 ow0.3: acc 0.989  margin 0.358  ±0.002
test d8 T6 ow0.3: acc 0.793  margin 0.112  ±0.008
test d16 T64 K8 ow0.3: acc 0.581  margin 0.007  ±0.011
test d16 T128 K8 ow0.3: acc 0.107  margin -0.405  ±0.010
```

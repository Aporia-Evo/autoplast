# Search seed 10

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 681351  time: 1135s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 4212 candidates
* decayed linear attention: 4468 candidates
* linear, not error-correcting: 5108 candidates
* linear attention: 39028 candidates
* delta rule: 345844 candidates
* gated delta rule: 362612 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 39540 candidates
- delta rule (beta=1) (acc 0.858): 345844 candidates
- delta rule (beta=0.5) (acc 0.932): 345844 candidates
- gated delta (alpha=0.9) (acc 0.729): 39028 candidates

## Best rule

```
S' = (((σ(0.210)·S + σ(0.210)·S) - (σ(σ(1.352))·(σ(0.210)·S + σ(0.210)·S))((k)⊗(k))) + (v)⊗(tanh(tanh(k))))

Effective program (15 instructions):
  M2 = Outer(V0, V0)
  s3 = 0.2102
  s2 = 1.3516
  s0 = Sigmoid(s3)
  M1 = MatScale(s0, M0)
  s2 = Sigmoid(s2)
  s3 = Sigmoid(s2)
  V4 = Tanh(V0)
  V0 = Tanh(V4)
  M0 = MatAdd(M1, M1)
  M1 = MatScale(s3, M0)
  M1 = MatMul(M1, M2)
  M0 = MatSub(M0, M1)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)

structure: gated delta rule  [a=1.105 b=0.911 c=-0.761 g=0.001, erase c/a=0.689, R²=0.9978, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.968  margin 0.307  ±0.003
test d16 T12 ow0.0: acc 0.952  margin 0.281  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.301  ±0.004
test d32 T24 ow0.3: acc 0.963  margin 0.341  ±0.003
test d8 T6 ow0.3: acc 0.837  margin 0.139  ±0.008
test d16 T64 K8 ow0.3: acc 0.062  margin -0.524  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

# Search seed 4

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 975879  time: 465s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3316 candidates
* linear attention: 4724 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 4724 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 4724 candidates

## Best rule

```
S' = (|tanh(v)|·S + (tanh(1.026·tanh(v)))⊗(k))

Effective program (8 instructions):
  V1 = Tanh(V1)
  s1 = 1.0257
  s3 = Norm(V1)
  V4 = VecScale(s1, V1)
  V3 = Tanh(V4)
  M3 = Outer(V3, V0)
  M1 = MatScale(s3, M0)
  M0 = MatAdd(M1, M3)

structure: linear attention  [a=0.952 b=0.933 c=-0.001 g=0.005, erase c/a=0.001, R²=0.9959, 384 steps]

train acc 0.818 ±0.013
test d16 T12 ow0.3: acc 0.788  margin 0.149  ±0.006
test d16 T12 ow0.0: acc 0.867  margin 0.185  ±0.004
test d16 T12 ow0.6: acc 0.647  margin 0.069  ±0.009
test d32 T24 ow0.3: acc 0.878  margin 0.226  ±0.005
test d8 T6 ow0.3: acc 0.635  margin 0.034  ±0.010
test d16 T64 K8 ow0.3: acc 0.448  margin -0.056  ±0.011
test d16 T128 K8 ow0.3: acc 0.446  margin -0.079  ±0.016
```

# Search seed 3

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 381316  time: 676s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 4468 candidates
* decayed linear attention: 5748 candidates
* linear, not error-correcting: 6260 candidates
* linear attention: 9716 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 9716 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 9716 candidates

## Best rule

```
S' = ((S + (v)⊗(k)) + -0.042·((S + (v)⊗(k)) - ((v)⊗(k))((v)⊗(k))))

Effective program (7 instructions):
  M2 = Outer(V1, V0)
  s1 = -0.0422
  M0 = MatAdd(M0, M2)
  M2 = MatMul(M2, M2)
  M1 = MatSub(M0, M2)
  M2 = MatScale(s1, M1)
  M0 = MatAdd(M0, M2)

structure: linear attention  [a=0.958 b=0.958 c=-0.000 g=0.001, erase c/a=0.000, R²=0.9999, 384 steps]

train acc 0.819 ±0.013
test d16 T12 ow0.3: acc 0.788  margin 0.149  ±0.006
test d16 T12 ow0.0: acc 0.883  margin 0.194  ±0.004
test d16 T12 ow0.6: acc 0.634  margin 0.064  ±0.009
test d32 T24 ow0.3: acc 0.875  margin 0.225  ±0.005
test d8 T6 ow0.3: acc 0.634  margin 0.029  ±0.010
test d16 T64 K8 ow0.3: acc 0.398  margin -0.085  ±0.011
test d16 T128 K8 ow0.3: acc 0.377  margin -0.106  ±0.015
```

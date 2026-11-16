# Search seed 15

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1719320  time: 3059s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* linear, not error-correcting: 2932 candidates
* unclassified: 3828 candidates
* linear attention: 13428 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 13428 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 13428 candidates

## Best rule

```
S' = 0.955·(((norm(tanh(v)))⊗(k) + S) - (((S + S) + 0.704·(((norm(tanh(v)))⊗(k))((norm(tanh(v)))⊗(k)))ᵀ))((((norm(tanh(v)))⊗(k))((norm(tanh(v)))⊗(k)))ᵀ))

Effective program (14 instructions):
  V2 = Tanh(V1)
  V2 = Normalize(V2)
  M3 = Outer(V2, V0)
  s2 = 0.7040
  M2 = MatMul(M3, M3)
  M1 = MatAdd(M0, M0)
  M0 = MatAdd(M3, M0)
  M2 = Transpose(M2)
  M3 = MatScale(s2, M2)
  M3 = MatAdd(M1, M3)
  M3 = MatMul(M3, M2)
  M0 = MatSub(M0, M3)
  s3 = 0.9546
  M0 = MatScale(s3, M0)

structure: unclassified  [a=0.956 b=0.953 c=-0.131 g=-0.043, erase c/a=0.137, R²=0.8884, 384 steps]

train acc 0.841 ±0.013
test d16 T12 ow0.3: acc 0.810  margin 0.164  ±0.006
test d16 T12 ow0.0: acc 0.854  margin 0.185  ±0.005
test d16 T12 ow0.6: acc 0.724  margin 0.110  ±0.009
test d32 T24 ow0.3: acc 0.873  margin 0.230  ±0.005
test d8 T6 ow0.3: acc 0.669  margin 0.049  ±0.010
test d16 T64 K8 ow0.3: acc 0.544  margin -0.009  ±0.011
test d16 T128 K8 ow0.3: acc 0.511  margin -0.032  ±0.016
```

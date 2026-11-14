# Search seed 15

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 456625  time: 702s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

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
S' = 0.954·((S + (norm(tanh(v)))⊗(k)) - (((S + S) + (((norm(tanh(v)))⊗(k))((norm(tanh(v)))⊗(k)))ᵀ))((((norm(tanh(v)))⊗(k))((norm(tanh(v)))⊗(k)))ᵀ))

Effective program (12 instructions):
  V2 = Tanh(V1)
  V2 = Normalize(V2)
  M3 = Outer(V2, V0)
  M2 = MatMul(M3, M3)
  M1 = MatAdd(M0, M0)
  M0 = MatAdd(M0, M3)
  M2 = Transpose(M2)
  M3 = MatAdd(M1, M2)
  M3 = MatMul(M3, M2)
  M0 = MatSub(M0, M3)
  s3 = 0.9536
  M0 = MatScale(s3, M0)

structure: unclassified  [a=0.955 b=0.952 c=-0.131 g=-0.045, erase c/a=0.137, R²=0.8876, 384 steps]

train acc 0.840 ±0.013
test d16 T12 ow0.3: acc 0.808  margin 0.164  ±0.006
test d16 T12 ow0.0: acc 0.852  margin 0.184  ±0.005
test d16 T12 ow0.6: acc 0.723  margin 0.110  ±0.009
test d32 T24 ow0.3: acc 0.871  margin 0.229  ±0.005
test d8 T6 ow0.3: acc 0.668  margin 0.048  ±0.010
test d16 T64 K8 ow0.3: acc 0.548  margin -0.008  ±0.011
test d16 T128 K8 ow0.3: acc 0.515  margin -0.030  ±0.016
```

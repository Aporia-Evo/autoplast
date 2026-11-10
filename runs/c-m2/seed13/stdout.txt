# Search seed 13

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 793255  time: 1942s  pop: 500  tournament: 10

commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 5748 candidates
* unclassified: 9588 candidates
* linear, not error-correcting: 46708 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 45812 candidates
- delta rule (beta=1) (acc 0.578): 45940 candidates
- delta rule (beta=0.5) (acc 0.617): 56948 candidates
- gated delta (alpha=0.9) (acc 0.519): 45940 candidates

## Best rule

```
S' = ((tanh(|tanh(tanh(<(k + 0), tanh(tanh(k))>·tanh(tanh(k))))|·(v + tanh((0 - S)·tanh(<(k + 0), tanh(tanh(k))>·tanh(tanh(k)))))))⊗(tanh(tanh(<(k + 0), tanh(tanh(k))>·tanh(tanh(k))))) + S)
P1' = (tanh(|tanh(tanh(<(k + 0), tanh(tanh(k))>·tanh(tanh(k))))|·(v + tanh((0 - S)·tanh(<(k + 0), tanh(tanh(k))>·tanh(tanh(k)))))))⊗(tanh(tanh(<(k + 0), tanh(tanh(k))>·tanh(tanh(k)))))

Effective program (16 instructions):
  V2 = Tanh(V0)
  V3 = VecAdd(V0, V3)
  M3 = MatSub(M3, M0)
  V0 = Tanh(V2)
  s3 = Dot(V3, V0)
  V0 = VecScale(s3, V0)
  V2 = Tanh(V0)
  V4 = MatVec(M3, V2)
  V0 = Tanh(V2)
  s0 = Norm(V0)
  V2 = Tanh(V4)
  V1 = VecAdd(V1, V2)
  V4 = VecScale(s0, V1)
  V3 = Tanh(V4)
  M1 = Outer(V3, V0)
  M0 = MatAdd(M1, M0)

structure: unclassified  [a=0.999 b=0.562 c=-0.442 g=0.026, erase c/a=0.442, R²=0.9799, 1408 steps]

train acc 0.623 ±0.014
test regime collision3: acc 0.638  margin 0.046  ±0.006
test d16 T12 ow0.3: acc 0.919  margin 0.253  ±0.004
test d16 T12 ow0.0: acc 0.891  margin 0.229  ±0.004
test d16 T12 ow0.6: acc 0.920  margin 0.246  ±0.005
test d32 T24 ow0.3: acc 0.981  margin 0.361  ±0.002
test d8 T6 ow0.3: acc 0.713  margin 0.071  ±0.009
test d16 T64 K8 ow0.3: acc 0.805  margin 0.141  ±0.009
test d16 T128 K8 ow0.3: acc 0.769  margin 0.119  ±0.013
```

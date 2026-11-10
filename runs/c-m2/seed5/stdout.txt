# Search seed 5

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 664121  time: 1605s  pop: 500  tournament: 10

commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 2292 candidates
* linear attention: 30068 candidates
* gated delta rule: 1095540 candidates
* delta rule: 1096436 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 30068 candidates
- delta rule (beta=1) (acc 0.578): 1095796 candidates
- delta rule (beta=0.5) (acc 0.617): 1103476 candidates
- gated delta (alpha=0.9) (acc 0.519): 1095028 candidates

## Best rule

```
S' = (((v - S·tanh(tanh(tanh(tanh(k))))))⊗(|tanh(tanh(tanh(tanh(k))))|·tanh(tanh(|tanh(tanh(tanh(tanh(k))))|·tanh(tanh(tanh(tanh(tanh(k)))))))) + S)
P1' = ((v - S·tanh(tanh(tanh(tanh(k))))))⊗(|tanh(tanh(tanh(tanh(k))))|·tanh(tanh(|tanh(tanh(tanh(tanh(k))))|·tanh(tanh(tanh(tanh(tanh(k))))))))

Effective program (14 instructions):
  V0 = Tanh(V0)
  V5 = Tanh(V0)
  V0 = Tanh(V5)
  V3 = Tanh(V0)
  s1 = Norm(V3)
  V0 = Tanh(V3)
  V4 = VecScale(s1, V0)
  V2 = MatVec(M0, V3)
  V3 = Tanh(V4)
  V4 = VecSub(V1, V2)
  V1 = Tanh(V3)
  V3 = VecScale(s1, V1)
  M1 = Outer(V4, V3)
  M0 = MatAdd(M1, M0)

structure: unclassified  [a=0.999 b=0.544 c=-0.463 g=0.004, erase c/a=0.464, R²=0.9705, 1408 steps]

train acc 0.626 ±0.014
test regime collision3: acc 0.638  margin 0.045  ±0.006
test d16 T12 ow0.3: acc 0.918  margin 0.254  ±0.004
test d16 T12 ow0.0: acc 0.883  margin 0.226  ±0.004
test d16 T12 ow0.6: acc 0.924  margin 0.252  ±0.005
test d32 T24 ow0.3: acc 0.979  margin 0.361  ±0.002
test d8 T6 ow0.3: acc 0.716  margin 0.074  ±0.009
test d16 T64 K8 ow0.3: acc 0.820  margin 0.152  ±0.008
test d16 T128 K8 ow0.3: acc 0.787  margin 0.133  ±0.013
```

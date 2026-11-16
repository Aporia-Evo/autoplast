# Search seed 28

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1593157  time: 2423s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3956 candidates
* decayed linear attention: 4724 candidates
* linear, not error-correcting: 5236 candidates
* linear attention: 8180 candidates
* delta rule: 1578612 candidates
* gated delta rule: 1578996 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 8180 candidates
- delta rule (beta=1) (acc 0.858): 1578996 candidates
- delta rule (beta=0.5) (acc 0.932): 1578996 candidates
- gated delta (alpha=0.9) (acc 0.729): 8180 candidates

## Best rule

```
S' = ((1.106·S + <v, tanh(v)>·(v)⊗((tanh(tanh(k)) + tanh(k)))) - ((S)(((tanh(v))⊗(tanh(tanh(k))))ᵀ))((tanh(v))⊗(tanh(tanh(k)))))

Effective program (15 instructions):
  V5 = Tanh(V0)
  V3 = Tanh(V5)
  V0 = Tanh(V1)
  M2 = Outer(V0, V3)
  s0 = Dot(V1, V0)
  M3 = Transpose(M2)
  M3 = MatMul(M0, M3)
  s1 = 1.1062
  M0 = MatScale(s1, M0)
  M1 = MatMul(M3, M2)
  V3 = VecAdd(V3, V5)
  M2 = Outer(V1, V3)
  M3 = MatScale(s0, M2)
  M2 = MatAdd(M0, M3)
  M0 = MatSub(M2, M1)

structure: gated delta rule  [a=1.106 b=1.770 c=-0.753 g=0.016, erase c/a=0.680, R²=0.9966, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.967  margin 0.304  ±0.003
test d16 T12 ow0.0: acc 0.954  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.295  ±0.004
test d32 T24 ow0.3: acc 0.975  margin 0.365  ±0.002
test d8 T6 ow0.3: acc 0.817  margin 0.127  ±0.008
test d16 T64 K8 ow0.3: acc 0.053  margin -0.544  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

# Search seed 6

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 797251  time: 5004s  pop: 500  tournament: 10

commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1012 candidates
* linear attention: 3316 candidates
* unclassified: 5364 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3316 candidates
- delta rule (beta=1) (acc 0.578): 18676 candidates
- delta rule (beta=0.5) (acc 0.617): 25844 candidates
- gated delta (alpha=0.9) (acc 0.519): 17908 candidates

## Best rule

```
S' = (((tanh(v))⊗(k) - P1) - ((((tanh(v))⊗(k) + (P1 + (tanh(v))⊗(k))))((tanh(tanh(tanh(k))))⊗((0 - tanh(tanh(tanh(tanh(k))))))) - ((tanh(v))⊗(k) - P1)))
P1' = ((((tanh(v))⊗(k) + (P1 + (tanh(v))⊗(k))))((tanh(tanh(tanh(k))))⊗((0 - tanh(tanh(tanh(tanh(k))))))) - ((tanh(v))⊗(k) - P1))

Effective program (14 instructions):
  V5 = Tanh(V0)
  V1 = Tanh(V1)
  M2 = Outer(V1, V0)
  V0 = Tanh(V5)
  V5 = Tanh(V0)
  V0 = Tanh(V5)
  V4 = VecSub(V2, V0)
  M0 = MatSub(M2, M1)
  M1 = MatAdd(M1, M2)
  M3 = MatAdd(M2, M1)
  M2 = Outer(V5, V4)
  M3 = MatMul(M3, M2)
  M1 = MatSub(M3, M0)
  M0 = MatSub(M0, M1)

structure: unclassified  [a=1.002 b=3.273 c=-0.364 g=0.004, erase c/a=0.363, R²=0.7772, 1408 steps]

train acc 0.641 ±0.014
test regime collision3: acc 0.655  margin 0.039  ±0.006
test d16 T12 ow0.3: acc 0.916  margin 0.270  ±0.004
test d16 T12 ow0.0: acc 0.869  margin 0.226  ±0.004
test d16 T12 ow0.6: acc 0.927  margin 0.277  ±0.005
test d32 T24 ow0.3: acc 0.973  margin 0.361  ±0.002
test d8 T6 ow0.3: acc 0.768  margin 0.105  ±0.009
test d16 T64 K8 ow0.3: acc 0.845  margin 0.200  ±0.008
test d16 T128 K8 ow0.3: acc 0.848  margin 0.194  ±0.011
```

# Search seed 5

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 617559  time: 1257s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4980 candidates
* linear attention: 8948 candidates
* unclassified: 763380 candidates
* delta rule: 766068 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8948 candidates
- delta rule (beta=1) (acc 0.578): 766068 candidates
- delta rule (beta=0.5) (acc 0.617): 767220 candidates
- gated delta (alpha=0.9) (acc 0.519): 763380 candidates

## Best rule

```
S' = ((S + (tanh(1.520·v))⊗(k)) + ((tanh(tanh(1.520·v)) - P2·tanh(k)))⊗(tanh(k)))
P1' = (S + (tanh(1.520·v))⊗(k))
P2' = σ(0)·(S + (tanh(1.520·v))⊗(k))

Effective program (13 instructions):
  s0 = 1.5202
  V5 = VecScale(s0, V1)
  V5 = Tanh(V5)
  V4 = Tanh(V0)
  M1 = Outer(V5, V0)
  V3 = MatVec(M2, V4)
  V0 = Tanh(V5)
  s2 = Sigmoid(s2)
  V3 = VecSub(V0, V3)
  M1 = MatAdd(M0, M1)
  M3 = Outer(V3, V4)
  M0 = MatAdd(M1, M3)
  M2 = MatScale(s2, M1)

structure: unclassified  [a=1.000 b=2.548 c=-0.432 g=0.005, erase c/a=0.432, R²=0.9744, 1408 steps]

train acc 0.626 ±0.014
test regime collision3: acc 0.641  margin 0.037  ±0.006
test d16 T12 ow0.3: acc 0.909  margin 0.243  ±0.004
test d16 T12 ow0.0: acc 0.903  margin 0.229  ±0.004
test d16 T12 ow0.6: acc 0.916  margin 0.228  ±0.005
test d32 T24 ow0.3: acc 0.983  margin 0.338  ±0.002
test d8 T6 ow0.3: acc 0.745  margin 0.089  ±0.009
test d16 T64 K8 ow0.3: acc 0.795  margin 0.123  ±0.009
test d16 T128 K8 ow0.3: acc 0.781  margin 0.115  ±0.013
```

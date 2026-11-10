# Search seed 10

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 600495  time: 1789s  pop: 500  tournament: 10

commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3188 candidates
* decayed linear attention: 3828 candidates
* linear attention: 12788 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 12788 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((0.855·P1 + (tanh(v))⊗(tanh(k))) + <(tanh(v) - (k ⊙ k)), (tanh(v) - (k ⊙ k))>·(((tanh(v))⊗(tanh(k)) + P1) + ((tanh(v))⊗(tanh(k)) + P1)))
P1' = (0.855·P1 + (tanh(v))⊗(tanh(k)))

Effective program (13 instructions):
  s0 = 0.8547
  V1 = Tanh(V1)
  V3 = Tanh(V0)
  M2 = Outer(V1, V3)
  M0 = MatScale(s0, M1)
  V3 = Hadamard(V0, V0)
  V3 = VecSub(V1, V3)
  M3 = MatAdd(M2, M1)
  s3 = Dot(V3, V3)
  M1 = MatAdd(M0, M2)
  M0 = MatAdd(M3, M3)
  M3 = MatScale(s3, M0)
  M0 = MatAdd(M1, M3)

structure: unclassified  [a=0.865 b=2.822 c=-0.003 g=-0.023, erase c/a=0.003, R²=0.8798, 1408 steps]

train acc 0.514 ±0.014
test regime collision3: acc 0.513  margin -0.051  ±0.006
test d16 T12 ow0.3: acc 0.715  margin 0.116  ±0.007
test d16 T12 ow0.0: acc 0.680  margin 0.089  ±0.006
test d16 T12 ow0.6: acc 0.726  margin 0.114  ±0.009
test d32 T24 ow0.3: acc 0.586  margin 0.056  ±0.007
test d8 T6 ow0.3: acc 0.638  margin 0.034  ±0.010
test d16 T64 K8 ow0.3: acc 0.581  margin -0.017  ±0.011
test d16 T128 K8 ow0.3: acc 0.551  margin -0.037  ±0.016
```

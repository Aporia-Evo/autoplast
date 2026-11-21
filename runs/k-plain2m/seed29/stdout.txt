# Search seed 29

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 2100084  real evaluations (after cache): 831044  time: 3503s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* unclassified: 3956 candidates
* linear attention: 5108 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5108 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((P1)(((v)⊗(tanh(k)) + (v)⊗(tanh(k)))) + (((v)⊗(tanh(k)) + (v)⊗(tanh(k))) + ((v)⊗(tanh(k)) + P2)))
P1' = ((P1)(((v)⊗(tanh(k)) + (v)⊗(tanh(k)))))ᵀ
P2' = 0.895·((P1)(((v)⊗(tanh(k)) + (v)⊗(tanh(k)))) + (((v)⊗(tanh(k)) + (v)⊗(tanh(k))) + ((v)⊗(tanh(k)) + P2)))

Effective program (10 instructions):
  V0 = Tanh(V0)
  s2 = 0.8952
  M0 = Outer(V1, V0)
  M2 = MatAdd(M0, M2)
  M3 = MatAdd(M0, M0)
  M2 = MatAdd(M3, M2)
  M1 = MatMul(M1, M3)
  M0 = MatAdd(M1, M2)
  M2 = MatScale(s2, M0)
  M1 = Transpose(M1)

structure: unclassified  [a=0.895 b=2.902 c=-0.001 g=-0.001, erase c/a=0.001, R²=0.9210, 1408 steps]

train acc 0.512 ±0.014
test regime collision3: acc 0.513  margin -0.037  ±0.006
test d16 T12 ow0.3: acc 0.741  margin 0.129  ±0.007
test d16 T12 ow0.0: acc 0.775  margin 0.142  ±0.005
test d16 T12 ow0.6: acc 0.690  margin 0.091  ±0.009
test d32 T24 ow0.3: acc 0.696  margin 0.138  ±0.007
test d8 T6 ow0.3: acc 0.565  margin -0.008  ±0.010
test d16 T64 K8 ow0.3: acc 0.578  margin -0.006  ±0.011
test d16 T128 K8 ow0.3: acc 0.562  margin -0.025  ±0.016
```

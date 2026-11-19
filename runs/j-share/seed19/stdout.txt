# Search seed 19

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 963498  time: 2352s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 1140 candidates
* linear attention: 2804 candidates
* delta rule: 941940 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 2804 candidates
- delta rule (beta=1) (acc 0.578): 770804 candidates
- delta rule (beta=0.5) (acc 0.617): 964084 candidates
- gated delta (alpha=0.9) (acc 0.519): 241780 candidates

## Best rule

```
S' = (σ(0.433)·((norm(v) - tanh(S·k)))⊗(tanh(tanh(k))) + 1/(|((P1)((0 - P1))·((norm(v) - tanh(S·k)) - v) + tanh(tanh(k)))|)·S)
P1' = 1/(|((P1)((0 - P1))·((norm(v) - tanh(S·k)) - v) + tanh(tanh(k)))|)·S
P2' = σ(0.433)·((norm(v) - tanh(S·k)))⊗(tanh(tanh(k)))

Effective program (19 instructions):
  V2 = Tanh(V0)
  V4 = MatVec(M0, V0)
  V5 = Tanh(V4)
  V0 = Normalize(V1)
  s1 = 0.4326
  M2 = MatSub(M3, M1)
  V3 = VecSub(V0, V5)
  V0 = Tanh(V2)
  M3 = Outer(V3, V0)
  s2 = Sigmoid(s1)
  V2 = VecSub(V3, V1)
  M1 = MatMul(M1, M2)
  M2 = MatScale(s2, M3)
  V5 = MatVec(M1, V2)
  V2 = VecAdd(V5, V0)
  s0 = Norm(V2)
  s3 = Recip(s0)
  M1 = MatScale(s3, M0)
  M0 = MatAdd(M2, M1)

structure: unclassified  [a=1.023 b=0.545 c=-0.532 g=-0.005, erase c/a=0.520, R²=0.7564, 1408 steps]

train acc 0.658 ±0.014
test regime collision3: acc 0.656  margin 0.062  ±0.006
test d16 T12 ow0.3: acc 0.943  margin 0.264  ±0.003
test d16 T12 ow0.0: acc 0.958  margin 0.264  ±0.003
test d16 T12 ow0.6: acc 0.888  margin 0.220  ±0.006
test d32 T24 ow0.3: acc 0.990  margin 0.362  ±0.001
test d8 T6 ow0.3: acc 0.752  margin 0.095  ±0.009
test d16 T64 K8 ow0.3: acc 0.687  margin 0.080  ±0.010
test d16 T128 K8 ow0.3: acc 0.681  margin 0.069  ±0.015
```

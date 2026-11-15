# Search seed 17

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1041317  time: 2166s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 884 candidates
* linear attention: 5380 candidates
* unclassified: 7556 candidates
* delta rule: 102700 candidates
* delta + Kronecker mix: 279292 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5380 candidates
- delta rule (beta=1) (acc 0.578): 98972 candidates
- delta rule (beta=0.5) (acc 0.617): 102700 candidates
- gated delta (alpha=0.9) (acc 0.519): 98148 candidates

## Best rule

```
S' = (S + (<tanh(v), v>·(v - S·tanh(tanh(tanh(tanh(σ(1.307)·k))))))⊗(σ(1.307)·(tanh(tanh(σ(1.307)·k)))⊗((v - S·tanh(tanh(tanh(tanh(σ(1.307)·k))))))·v))
P1' = σ(1.307)·(tanh(tanh(σ(1.307)·k)))⊗((v - S·tanh(tanh(tanh(tanh(σ(1.307)·k))))))

Effective program (17 instructions):
  s0 = 1.3065
  s2 = Sigmoid(s0)
  V2 = VecScale(s2, V0)
  V3 = Tanh(V2)
  V0 = Tanh(V3)
  V4 = Tanh(V0)
  V3 = Tanh(V4)
  V2 = MatVec(M0, V3)
  V2 = VecSub(V1, V2)
  V5 = Tanh(V1)
  s1 = Dot(V5, V1)
  M1 = Outer(V0, V2)
  M1 = MatScale(s2, M1)
  V0 = MatVec(M1, V1)
  V2 = VecScale(s1, V2)
  M3 = Outer(V2, V0)
  M0 = MatAdd(M0, M3)

structure: delta + Kronecker mix  [a=1.000 b=0.556 c=-0.379 g=-0.367, erase c/a=0.379, R²=0.9951, 1408 steps]

train acc 0.631 ±0.014
test regime collision3: acc 0.645  margin 0.042  ±0.006
test d16 T12 ow0.3: acc 0.924  margin 0.246  ±0.004
test d16 T12 ow0.0: acc 0.911  margin 0.234  ±0.004
test d16 T12 ow0.6: acc 0.923  margin 0.228  ±0.005
test d32 T24 ow0.3: acc 0.983  margin 0.338  ±0.002
test d8 T6 ow0.3: acc 0.756  margin 0.094  ±0.009
test d16 T64 K8 ow0.3: acc 0.780  margin 0.110  ±0.009
test d16 T128 K8 ow0.3: acc 0.757  margin 0.097  ±0.013
```

# Search seed 20

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 779773  time: 3321s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 4724 candidates
* decayed linear attention: 5492 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 20468 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 195828 candidates

## Best rule

```
S' = 0.875·(S + (norm(v))⊗(norm((tanh((tanh((k + k)) + (P1)(P2)·k)) - (norm(v) ⊙ norm((P1)(P2)·k))))))
P1' = ((tanh((k + k)) ⊙ (tanh((tanh((k + k)) + (P1)(P2)·k)) - (norm(v) ⊙ norm((P1)(P2)·k)))))⊗(k)
P2' = (P1)(P2)

Effective program (17 instructions):
  V3 = Normalize(V1)
  V2 = VecAdd(V0, V0)
  M2 = MatMul(M1, M2)
  V1 = Tanh(V2)
  V2 = MatVec(M2, V0)
  V4 = VecAdd(V1, V2)
  V4 = Tanh(V4)
  V2 = Normalize(V2)
  V2 = Hadamard(V3, V2)
  V4 = VecSub(V4, V2)
  s1 = 0.8746
  V2 = Normalize(V4)
  M1 = Outer(V3, V2)
  V5 = Hadamard(V1, V4)
  M0 = MatAdd(M0, M1)
  M0 = MatScale(s1, M0)
  M1 = Outer(V5, V0)

structure: unclassified  [a=0.875 b=0.858 c=-0.000 g=-0.001, erase c/a=0.000, R²=0.9617, 1408 steps]

train acc 0.520 ±0.014
test regime collision3: acc 0.513  margin -0.046  ±0.006
test d16 T12 ow0.3: acc 0.729  margin 0.122  ±0.007
test d16 T12 ow0.0: acc 0.704  margin 0.101  ±0.006
test d16 T12 ow0.6: acc 0.715  margin 0.108  ±0.009
test d32 T24 ow0.3: acc 0.628  margin 0.091  ±0.007
test d8 T6 ow0.3: acc 0.609  margin 0.017  ±0.010
test d16 T64 K8 ow0.3: acc 0.575  margin -0.013  ±0.011
test d16 T128 K8 ow0.3: acc 0.549  margin -0.032  ±0.016
```

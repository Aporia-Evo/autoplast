# Search seed 7

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500108  real evaluations (after cache): 942980  time: 2503s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 1012 candidates
* linear attention: 7804 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 7804 candidates
- delta rule (beta=1) (acc 0.578): 976932 candidates
- delta rule (beta=0.5) (acc 0.617): 1149604 candidates
- gated delta (alpha=0.9) (acc 0.519): 52044 candidates

## Best rule

```
S' = ((v)⊗(tanh(k)) + (S - 0.166·P1))
P1' = ((S - 0.166·P1))((tanh((tanh(k) + tanh(k))))⊗((tanh(k) + tanh(k))))
P2' = 0.166·P1

Effective program (10 instructions):
  s0 = 0.1658
  M2 = MatScale(s0, M1)
  M1 = MatSub(M0, M2)
  V4 = Tanh(V0)
  M0 = Outer(V1, V4)
  V5 = VecAdd(V4, V4)
  V0 = Tanh(V5)
  M3 = Outer(V0, V5)
  M0 = MatAdd(M0, M1)
  M1 = MatMul(M1, M3)

structure: unclassified  [a=0.937 b=0.946 c=-0.032 g=-0.000, erase c/a=0.034, R²=0.8096, 1408 steps]

train acc 0.624 ±0.014
test regime collision3: acc 0.628  margin 0.037  ±0.006
test d16 T12 ow0.3: acc 0.912  margin 0.243  ±0.004
test d16 T12 ow0.0: acc 0.902  margin 0.227  ±0.004
test d16 T12 ow0.6: acc 0.886  margin 0.224  ±0.006
test d32 T24 ow0.3: acc 0.980  margin 0.346  ±0.002
test d8 T6 ow0.3: acc 0.724  margin 0.081  ±0.009
test d16 T64 K8 ow0.3: acc 0.784  margin 0.133  ±0.009
test d16 T128 K8 ow0.3: acc 0.770  margin 0.119  ±0.013
```

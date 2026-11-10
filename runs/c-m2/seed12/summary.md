# Search seed 12

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 675779  time: 1687s  pop: 500  tournament: 10

commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 1652 candidates
* linear attention: 2548 candidates
* gated delta rule: 47604 candidates
* delta rule: 51188 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 2548 candidates
- delta rule (beta=1) (acc 0.578): 49396 candidates
- delta rule (beta=0.5) (acc 0.617): 49780 candidates
- gated delta (alpha=0.9) (acc 0.519): 46964 candidates

## Best rule

```
S' = ((S + ((tanh(v) + P1·(k + k)))⊗((k + k))) + -0.146·((tanh(v) + P1·(k + k)))⊗((k + k)))
P1' = -0.146·|(tanh(v) + P1·(k + k))|·(S + ((tanh(v) + P1·(k + k)))⊗((k + k)))

Effective program (12 instructions):
  V2 = VecAdd(V0, V0)
  V3 = MatVec(M1, V2)
  V1 = Tanh(V1)
  V1 = VecAdd(V1, V3)
  s3 = -0.1459
  M1 = Outer(V1, V2)
  M0 = MatAdd(M0, M1)
  M3 = MatScale(s3, M1)
  s2 = Norm(V1)
  M1 = MatScale(s2, M0)
  M1 = MatScale(s3, M1)
  M0 = MatAdd(M0, M3)

structure: delta rule  [a=1.000 b=1.623 c=-0.546 g=-0.001, erase c/a=0.546, R²=0.9929, 1408 steps]

train acc 0.627 ±0.014
test regime collision3: acc 0.640  margin 0.047  ±0.006
test d16 T12 ow0.3: acc 0.922  margin 0.263  ±0.004
test d16 T12 ow0.0: acc 0.900  margin 0.237  ±0.004
test d16 T12 ow0.6: acc 0.942  margin 0.270  ±0.004
test d32 T24 ow0.3: acc 0.986  margin 0.353  ±0.002
test d8 T6 ow0.3: acc 0.790  margin 0.111  ±0.008
test d16 T64 K8 ow0.3: acc 0.848  margin 0.177  ±0.008
test d16 T128 K8 ow0.3: acc 0.844  margin 0.174  ±0.011
```

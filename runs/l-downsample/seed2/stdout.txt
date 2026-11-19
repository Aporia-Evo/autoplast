# Search seed 2

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 541323  time: 382s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3188 candidates
* decayed linear attention: 3956 candidates
* linear attention: 22260 candidates
* delta + Kronecker mix: 92916 candidates
* delta rule: 93172 candidates
* gated delta rule: 104948 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 22260 candidates
- delta rule (beta=1) (acc 0.858): 92916 candidates
- delta rule (beta=0.5) (acc 0.932): 93172 candidates
- gated delta (alpha=0.9) (acc 0.729): 22260 candidates

## Best rule

```
S' = (0.553·(S + S) + ((v - 0.838·S·k))⊗(tanh(tanh(k))))

Effective program (11 instructions):
  s1 = 0.5535
  s2 = 0.8377
  M1 = MatScale(s2, M0)
  V2 = MatVec(M1, V0)
  V1 = VecSub(V1, V2)
  V0 = Tanh(V0)
  V0 = Tanh(V0)
  M1 = MatAdd(M0, M0)
  M2 = MatScale(s1, M1)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M2, M1)

structure: gated delta rule  [a=1.107 b=0.911 c=-0.763 g=0.005, erase c/a=0.689, R²=0.9969, 384 steps]

train acc 0.973 ±0.006
test d16 T12 ow0.3: acc 0.967  margin 0.307  ±0.003
test d16 T12 ow0.0: acc 0.952  margin 0.281  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.300  ±0.004
test d32 T24 ow0.3: acc 0.967  margin 0.348  ±0.003
test d8 T6 ow0.3: acc 0.836  margin 0.137  ±0.008
test d16 T64 K8 ow0.3: acc 0.060  margin -0.535  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

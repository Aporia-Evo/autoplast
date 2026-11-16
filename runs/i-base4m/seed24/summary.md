# Search seed 24

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1384480  time: 1219s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 5236 candidates
* linear, not error-correcting: 6260 candidates
* unclassified: 6900 candidates
* linear attention: 42356 candidates
* gated delta rule: 1918196 candidates
* delta rule: 2334580 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 42356 candidates
- delta rule (beta=1) (acc 0.858): 1918196 candidates
- delta rule (beta=0.5) (acc 0.932): 2322036 candidates
- gated delta (alpha=0.9) (acc 0.729): 41204 candidates

## Best rule

```
S' = (((v)⊗(0.730·k) + 1.117·S) - (((v)⊗(0.730·k) + 1.117·S))((k)⊗(0.730·k)))

Effective program (9 instructions):
  s3 = 0.7300
  V4 = VecScale(s3, V0)
  M3 = Outer(V1, V4)
  s1 = 1.1165
  M0 = MatScale(s1, M0)
  M0 = MatAdd(M3, M0)
  M1 = Outer(V0, V4)
  M2 = MatMul(M0, M1)
  M0 = MatSub(M0, M2)

structure: gated delta rule  [a=1.117 b=0.197 c=-0.815 g=-0.000, erase c/a=0.730, R²=1.0000, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.312  ±0.003
test d16 T12 ow0.0: acc 0.951  margin 0.284  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.310  ±0.004
test d32 T24 ow0.3: acc 0.957  margin 0.335  ±0.003
test d8 T6 ow0.3: acc 0.844  margin 0.143  ±0.008
test d16 T64 K8 ow0.3: acc 0.051  margin -0.564  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

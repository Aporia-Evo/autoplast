# Search seed 15

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500028  real evaluations (after cache): 992486  time: 682s  pop: 500  tournament: 10

commit: 6df6477  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 8

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* linear, not error-correcting: 2940 candidates
* unclassified: 5252 candidates
* linear attention: 149468 candidates
* delta rule: 208356 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 149340 candidates
- delta rule (beta=1) (acc 0.858): 196260 candidates
- delta rule (beta=0.5) (acc 0.932): 208356 candidates
- gated delta (alpha=0.9) (acc 0.729): 149340 candidates

## Best rule

```
S' = ((v)⊗(k) - (((<S·k, S·k>·S·k)⊗(0.463·k) - S) - ((<S·k, S·k>·S·k)⊗(0.463·k))((<S·k, S·k>·S·k)⊗(0.463·k))))

Effective program (11 instructions):
  s1 = 0.4632
  V4 = VecScale(s1, V0)
  V2 = MatVec(M0, V0)
  s2 = Dot(V2, V2)
  V2 = VecScale(s2, V2)
  M3 = Outer(V2, V4)
  M2 = MatSub(M3, M0)
  M3 = MatMul(M3, M3)
  M1 = MatSub(M2, M3)
  M0 = Outer(V1, V0)
  M0 = MatSub(M0, M1)

structure: unclassified  [a=1.000 b=0.997 c=-0.429 g=-0.037, erase c/a=0.429, R²=0.9803, 384 steps]

train acc 0.954 ±0.007
test d16 T12 ow0.3: acc 0.937  margin 0.255  ±0.004
test d16 T12 ow0.0: acc 0.928  margin 0.230  ±0.003
test d16 T12 ow0.6: acc 0.944  margin 0.264  ±0.004
test d32 T24 ow0.3: acc 0.992  margin 0.344  ±0.001
test d8 T6 ow0.3: acc 0.782  margin 0.104  ±0.009
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

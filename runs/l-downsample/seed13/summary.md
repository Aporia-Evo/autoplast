# Search seed 13

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 664001  time: 567s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2420 candidates
* decayed linear attention: 3828 candidates
* linear attention: 136820 candidates
* delta rule: 302068 candidates
* gated delta rule: 308724 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 136820 candidates
- delta rule (beta=1) (acc 0.858): 302068 candidates
- delta rule (beta=0.5) (acc 0.932): 303604 candidates
- gated delta (alpha=0.9) (acc 0.729): 136820 candidates

## Best rule

```
S' = ((0.629·S + -0.543·S) + (((v - 0.629·S·k))⊗(k) + S))

Effective program (10 instructions):
  s0 = 0.6292
  M2 = MatScale(s0, M0)
  s0 = -0.5427
  M1 = MatScale(s0, M0)
  V5 = MatVec(M2, V0)
  V2 = VecSub(V1, V5)
  M3 = Outer(V2, V0)
  M2 = MatAdd(M2, M1)
  M3 = MatAdd(M3, M0)
  M0 = MatAdd(M2, M3)

structure: gated delta rule  [a=1.087 b=1.000 c=-0.629 g=-0.000, erase c/a=0.579, R²=1.0000, 384 steps]

train acc 0.970 ±0.006
test d16 T12 ow0.3: acc 0.965  margin 0.289  ±0.003
test d16 T12 ow0.0: acc 0.959  margin 0.275  ±0.003
test d16 T12 ow0.6: acc 0.957  margin 0.270  ±0.004
test d32 T24 ow0.3: acc 0.953  margin 0.327  ±0.003
test d8 T6 ow0.3: acc 0.834  margin 0.133  ±0.008
test d16 T64 K8 ow0.3: acc 0.077  margin -0.457  ±0.006
test d16 T128 K8 ow0.3: acc 0.019  margin -0.628  ±0.004
```

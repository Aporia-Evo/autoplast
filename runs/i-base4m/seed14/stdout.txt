# Search seed 14

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1886554  time: 2014s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1012 candidates
* linear, not error-correcting: 1652 candidates
* linear attention: 5620 candidates
* delta rule: 2638836 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 5620 candidates
- delta rule (beta=1) (acc 0.858): 2575220 candidates
- delta rule (beta=0.5) (acc 0.932): 2638836 candidates
- gated delta (alpha=0.9) (acc 0.729): 5620 candidates

## Best rule

```
S' = (((tanh(tanh(tanh(v))) + <S·k, S·k>·((<tanh(tanh(v)), tanh(tanh(tanh(v)))>·tanh(tanh(v)) - norm(tanh(tanh(tanh(v))))) - S·k)))⊗(tanh(k)) + S)

Effective program (15 instructions):
  V4 = Tanh(V1)
  V3 = Tanh(V4)
  V5 = Tanh(V3)
  V1 = Normalize(V5)
  s3 = Dot(V3, V5)
  V4 = MatVec(M0, V0)
  V2 = VecScale(s3, V3)
  V2 = VecSub(V2, V1)
  V1 = VecSub(V2, V4)
  s2 = Dot(V4, V4)
  V2 = VecScale(s2, V1)
  V5 = VecAdd(V5, V2)
  V0 = Tanh(V0)
  M3 = Outer(V5, V0)
  M0 = MatAdd(M3, M0)

structure: unclassified  [a=1.000 b=0.758 c=-0.532 g=0.035, erase c/a=0.532, R²=0.9582, 384 steps]

train acc 0.949 ±0.008
test d16 T12 ow0.3: acc 0.937  margin 0.265  ±0.004
test d16 T12 ow0.0: acc 0.935  margin 0.235  ±0.003
test d16 T12 ow0.6: acc 0.949  margin 0.275  ±0.004
test d32 T24 ow0.3: acc 0.988  margin 0.364  ±0.002
test d8 T6 ow0.3: acc 0.758  margin 0.095  ±0.009
test d16 T64 K8 ow0.3: acc 0.829  margin 0.176  ±0.008
test d16 T128 K8 ow0.3: acc 0.830  margin 0.170  ±0.012
```

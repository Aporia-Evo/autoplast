# Search seed 12

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: on  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 586877  time: 788s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3572 candidates
* decayed linear attention: 4212 candidates
* linear attention: 37236 candidates
* delta rule: 154996 candidates
* gated delta rule: 167796 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 37236 candidates
- delta rule (beta=1) (acc 0.858): 154996 candidates
- delta rule (beta=0.5) (acc 0.932): 156148 candidates
- gated delta (alpha=0.9) (acc 0.729): 37236 candidates

## Best rule

```
S' = (((tanh(v) - S·tanh(k)))⊗(0.751·k) + 1.099·((v)⊗((tanh(k) - k)) + S))

Effective program (13 instructions):
  V4 = Tanh(V0)
  s1 = 0.7515
  V3 = VecSub(V4, V0)
  M3 = Outer(V1, V3)
  V4 = MatVec(M0, V4)
  s0 = 1.0995
  V0 = VecScale(s1, V0)
  M3 = MatAdd(M3, M0)
  M0 = MatScale(s0, M3)
  V5 = Tanh(V1)
  V1 = VecSub(V5, V4)
  M2 = Outer(V1, V0)
  M0 = MatAdd(M2, M0)

structure: gated delta rule  [a=1.100 b=0.661 c=-0.716 g=0.008, erase c/a=0.651, R²=0.9971, 384 steps]

train acc 0.975 ±0.005
test d16 T12 ow0.3: acc 0.967 ±0.003  margin 0.301
test d16 T12 ow0.0: acc 0.955 ±0.003  margin 0.278
test d16 T12 ow0.6: acc 0.963 ±0.004  margin 0.290
test d32 T24 ow0.3: acc 0.963 ±0.003  margin 0.341
test d8 T6 ow0.3: acc 0.830 ±0.008  margin 0.135
full T24: acc 0.762 ±0.006  margin 0.116
overload T48: acc 0.215 ±0.004  margin -0.275
rewrite8 T96: acc 0.021 ±0.003  margin -0.616
rewrite14 T96: acc 0.018 ±0.002  margin -0.635
clustered T12: acc 0.192 ±0.006  margin -0.277
clustered8 T48: acc 0.057 ±0.005  margin -0.531
```

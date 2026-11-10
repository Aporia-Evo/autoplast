# Search seed 16

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: off  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 503537  time: 664s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4212 candidates
* unclassified: 8436 candidates
* linear attention: 29044 candidates
* delta rule: 49012 candidates
* linear, not error-correcting: 51828 candidates
* gated delta rule: 374004 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 29044 candidates
- delta rule (beta=1) (acc 0.858): 49012 candidates
- delta rule (beta=0.5) (acc 0.932): 71028 candidates
- gated delta (alpha=0.9) (acc 0.729): 29044 candidates

## Best rule

```
S' = ((0.554·S + 0.554·S) + ((v - S·tanh(tanh(k))))⊗(tanh(tanh(tanh(k)))))

Effective program (10 instructions):
  V0 = Tanh(V0)
  V0 = Tanh(V0)
  V3 = MatVec(M0, V0)
  V0 = Tanh(V0)
  V1 = VecSub(V1, V3)
  s1 = 0.5536
  M1 = MatScale(s1, M0)
  M3 = MatAdd(M1, M1)
  M2 = Outer(V1, V0)
  M0 = MatAdd(M3, M2)

structure: gated delta rule  [a=1.107 b=0.877 c=-0.800 g=0.012, erase c/a=0.722, R²=0.9933, 384 steps]

train acc 0.970 ±0.006
test d16 T12 ow0.3: acc 0.966 ±0.003  margin 0.310
test d16 T12 ow0.0: acc 0.947 ±0.003  margin 0.279
test d16 T12 ow0.6: acc 0.964 ±0.004  margin 0.307
test d32 T24 ow0.3: acc 0.979 ±0.002  margin 0.369
test d8 T6 ow0.3: acc 0.828 ±0.008  margin 0.133
full T24: acc 0.748 ±0.007  margin 0.113
overload T48: acc 0.178 ±0.004  margin -0.315
rewrite8 T96: acc 0.024 ±0.003  margin -0.624
rewrite14 T96: acc 0.021 ±0.002  margin -0.637
clustered T12: acc 0.185 ±0.006  margin -0.294
clustered8 T48: acc 0.051 ±0.005  margin -0.544
```

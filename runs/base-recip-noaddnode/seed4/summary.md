# Search seed 4

commit: 045ea3a  regime: base  task seed: 1  train episodes: 96
add-node mutation: off  reciprocal op: on  persistent registers: 1 matrix, 0 vector
candidates: 1500020  real evaluations (after cache): 280049  time: 367s  pop: 500  tournament: 10  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1396 candidates
* linear, not error-correcting: 3444 candidates
* unclassified: 10356 candidates
* linear attention: 13044 candidates

## Accuracy levels (best train acc reaches a reference rule's accuracy; this is NOT rediscovery)

- linear attention (acc 0.772): 13044 candidates
- delta rule (beta=1) (acc 0.858): not reached
- delta rule (beta=0.5) (acc 0.932): not reached
- gated delta (alpha=0.9) (acc 0.729): 13044 candidates

## Best rule

```
S' = ((v)⊗(k) - 0.958·(0 - S))

Effective program (5 instructions):
  M3 = MatSub(M1, M0)
  M0 = Outer(V1, V0)
  s1 = 0.9577
  M3 = MatScale(s1, M3)
  M0 = MatSub(M0, M3)

structure: linear attention  [a=0.958 b=1.000 c=0.000 g=0.000, erase c/a=-0.000, R²=1.0000, 384 steps]

train acc 0.814 ±0.014
test d16 T12 ow0.3: acc 0.787 ±0.006  margin 0.149
test d16 T12 ow0.0: acc 0.884 ±0.004  margin 0.194
test d16 T12 ow0.6: acc 0.636 ±0.009  margin 0.064
test d32 T24 ow0.3: acc 0.874 ±0.005  margin 0.225
test d8 T6 ow0.3: acc 0.633 ±0.010  margin 0.029
full T24: acc 0.596 ±0.007  margin 0.021
overload T48: acc 0.381 ±0.005  margin -0.127
rewrite8 T96: acc 0.378 ±0.011  margin -0.091
rewrite14 T96: acc 0.410 ±0.008  margin -0.098
clustered T12: acc 0.151 ±0.005  margin -0.271
clustered8 T48: acc 0.072 ±0.006  margin -0.367
```

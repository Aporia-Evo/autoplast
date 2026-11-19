# Search seed 30

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 974282  time: 3284s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 900084 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2164 candidates
* unclassified: 2420 candidates
* linear attention: 3700 candidates
* delta rule: 733812 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3700 candidates
- delta rule (beta=1) (acc 0.578): 733812 candidates
- delta rule (beta=0.5) (acc 0.617): 733812 candidates
- gated delta (alpha=0.9) (acc 0.519): 342516 candidates

## Best rule

```
S' = (|0| + σ(|0|))·(((v)⊗(k) + (P2 - P1)) - ((P2 - P1)·0.620·k)⊗(k))
P1' = ((P2 - P1)·0.620·k)⊗(tanh(k))
P2' = ((v)⊗(k) + ((P2 - P1) + (v)⊗(k)))

Effective program (16 instructions):
  s2 = 0.6195
  s1 = Norm(V4)
  V5 = VecScale(s2, V0)
  M1 = MatSub(M2, M1)
  V4 = MatVec(M1, V5)
  M0 = Outer(V1, V0)
  M3 = MatAdd(M1, M0)
  M2 = MatAdd(M0, M3)
  s2 = Sigmoid(s1)
  M3 = MatAdd(M0, M1)
  M1 = Outer(V4, V0)
  M3 = MatSub(M3, M1)
  s1 = SAdd(s1, s2)
  M0 = MatScale(s1, M3)
  V1 = Tanh(V0)
  M1 = Outer(V4, V1)

structure: unclassified  [a=1.045 b=0.501 c=-0.637 g=0.002, erase c/a=0.610, R²=0.7446, 1408 steps]

train acc 0.655 ±0.014
test regime collision3: acc 0.672  margin 0.067  ±0.006
test d16 T12 ow0.3: acc 0.936  margin 0.278  ±0.004
test d16 T12 ow0.0: acc 0.905  margin 0.245  ±0.004
test d16 T12 ow0.6: acc 0.952  margin 0.277  ±0.004
test d32 T24 ow0.3: acc 0.986  margin 0.364  ±0.002
test d8 T6 ow0.3: acc 0.819  margin 0.129  ±0.008
test d16 T64 K8 ow0.3: acc 0.858  margin 0.184  ±0.008
test d16 T128 K8 ow0.3: acc 0.859  margin 0.179  ±0.011
```

# Search seed 25

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 881324  time: 3533s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1652 candidates
* unclassified: 5236 candidates
* linear, not error-correcting: 121844 candidates
* delta rule: 133620 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 10740 candidates
- delta rule (beta=1) (acc 0.578): 119540 candidates
- delta rule (beta=0.5) (acc 0.617): 133620 candidates
- gated delta (alpha=0.9) (acc 0.519): 119028 candidates

## Best rule

```
S' = (|norm(((P2 - S)·k - k))|·((((-0.411 + -0.411)·-0.411·σ(0)·(v + (P2 - S)·k))⊗(((P2 - S)·k - k)) + (σ(0)·(v + (P2 - S)·k))⊗(k)))(((P2 - S) + ((-0.411 + -0.411)·-0.411·σ(0)·(v + (P2 - S)·k))⊗(((P2 - S)·k - k)))) - ((P2 - S) - (((-0.411 + -0.411)·-0.411·σ(0)·(v + (P2 - S)·k))⊗(((P2 - S)·k - k)) + (σ(0)·(v + (P2 - S)·k))⊗(k))))
P1' = ((P2 - S) - (((-0.411 + -0.411)·-0.411·σ(0)·(v + (P2 - S)·k))⊗(((P2 - S)·k - k)) + (σ(0)·(v + (P2 - S)·k))⊗(k)))
P2' = ((-0.411 + -0.411)·-0.411·σ(0)·(v + (P2 - S)·k))⊗(((P2 - S)·k - k))

Effective program (20 instructions):
  M1 = MatSub(M2, M0)
  s3 = Sigmoid(s1)
  V2 = MatVec(M1, V0)
  V4 = VecAdd(V1, V2)
  V3 = VecScale(s3, V4)
  V2 = VecSub(V2, V0)
  M0 = Outer(V3, V0)
  s3 = -0.4112
  V5 = VecScale(s3, V3)
  s3 = SAdd(s3, s3)
  V4 = VecScale(s3, V5)
  M2 = Outer(V4, V2)
  M0 = MatAdd(M2, M0)
  V0 = Normalize(V2)
  s2 = Norm(V0)
  M3 = MatAdd(M1, M2)
  M3 = MatMul(M0, M3)
  M1 = MatSub(M1, M0)
  M0 = MatScale(s2, M3)
  M0 = MatSub(M0, M1)

structure: unclassified  [a=0.991 b=0.516 c=-0.583 g=0.039, erase c/a=0.589, R²=0.3691, 1408 steps]

train acc 0.681 ±0.013
test regime collision3: acc 0.658  margin 0.066  ±0.006
test d16 T12 ow0.3: acc 0.867  margin 0.238  ±0.005
test d16 T12 ow0.0: acc 0.818  margin 0.190  ±0.005
test d16 T12 ow0.6: acc 0.884  margin 0.235  ±0.006
test d32 T24 ow0.3: acc 0.951  margin 0.334  ±0.003
test d8 T6 ow0.3: acc 0.696  margin 0.056  ±0.010
test d16 T64 K8 ow0.3: acc 0.796  margin 0.148  ±0.009
test d16 T128 K8 ow0.3: acc 0.787  margin 0.140  ±0.013
```

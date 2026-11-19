# Search seed 25

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 927487  time: 2401s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1140 candidates
* linear, not error-correcting: 2036 candidates
* unclassified: 2932 candidates
* linear attention: 11892 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 11892 candidates
- delta rule (beta=1) (acc 0.578): 74612 candidates
- delta rule (beta=0.5) (acc 0.617): 1428596 candidates
- gated delta (alpha=0.9) (acc 0.519): 70132 candidates

## Best rule

```
S' = ((tanh(v))⊗(k) + (P1 + P2))
P1' = <norm(((k - P2·k) + (k - P2·k))), k>·((tanh(v))⊗(k) + (P1 + P2))
P2' = ((P1 + P2)·norm(((k - P2·k) + (k - P2·k))))⊗(|σ(0)·norm(((k - P2·k) + (k - P2·k)))|·(0 - tanh(norm(((k - P2·k) + (k - P2·k))))))

Effective program (18 instructions):
  V3 = Tanh(V1)
  M0 = Outer(V3, V0)
  V5 = MatVec(M2, V0)
  V1 = VecSub(V0, V5)
  V3 = VecAdd(V1, V1)
  s0 = Sigmoid(s3)
  V5 = Normalize(V3)
  s3 = Dot(V5, V0)
  V4 = VecScale(s0, V5)
  M2 = MatAdd(M1, M2)
  M0 = MatAdd(M0, M2)
  M1 = MatScale(s3, M0)
  V0 = Tanh(V5)
  V2 = VecSub(V2, V0)
  s3 = Norm(V4)
  V1 = MatVec(M2, V5)
  V5 = VecScale(s3, V2)
  M2 = Outer(V1, V5)

structure: unclassified  [a=0.626 b=0.953 c=0.139 g=0.038, erase c/a=-0.222, R²=0.2058, 1408 steps]

train acc 0.614 ±0.014
test regime collision3: acc 0.617  margin 0.020  ±0.006
test d16 T12 ow0.3: acc 0.885  margin 0.216  ±0.005
test d16 T12 ow0.0: acc 0.847  margin 0.172  ±0.005
test d16 T12 ow0.6: acc 0.872  margin 0.210  ±0.006
test d32 T24 ow0.3: acc 0.965  margin 0.326  ±0.003
test d8 T6 ow0.3: acc 0.706  margin 0.031  ±0.010
test d16 T64 K8 ow0.3: acc 0.770  margin 0.128  ±0.009
test d16 T128 K8 ow0.3: acc 0.767  margin 0.119  ±0.013
```

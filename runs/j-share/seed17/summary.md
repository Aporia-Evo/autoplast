# Search seed 17

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 963929  time: 4455s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 150004 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 884 candidates
* unclassified: 5876 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 36212 candidates
- delta rule (beta=1) (acc 0.578): 66420 candidates
- delta rule (beta=0.5) (acc 0.617): 104564 candidates
- gated delta (alpha=0.9) (acc 0.519): 46068 candidates

## Best rule

```
S' = (((v)⊗(k) + P2) - 0.868·(P2)(((0 - k))⊗(0.868·((0 - k) - (0·(0 - k) ⊙ 0)))))
P1' = ((((0 - k) - (0·(0 - k) ⊙ 0)) + (0 - k)))⊗(v)
P2' = ((((v)⊗(k) + P2) - 0.868·(P2)(((0 - k))⊗(0.868·((0 - k) - (0·(0 - k) ⊙ 0))))) - (((((0 - k) - (0·(0 - k) ⊙ 0)) + (0 - k)))⊗(v))ᵀ)

Effective program (16 instructions):
  M1 = Outer(V1, V0)
  s0 = 0.8681
  V4 = VecSub(V3, V0)
  M0 = MatAdd(M1, M2)
  V2 = VecScale(s2, V4)
  V5 = Hadamard(V2, V3)
  V2 = VecSub(V4, V5)
  V3 = VecScale(s0, V2)
  M3 = Outer(V4, V3)
  M2 = MatMul(M2, M3)
  M1 = MatScale(s0, M2)
  M0 = MatSub(M0, M1)
  V2 = VecAdd(V2, V4)
  M1 = Outer(V2, V1)
  M3 = Transpose(M1)
  M2 = MatSub(M0, M3)

structure: unclassified  [a=1.033 b=1.002 c=-0.769 g=0.001, erase c/a=0.745, R²=0.5592, 1408 steps]

train acc 0.659 ±0.014
test regime collision3: acc 0.677  margin 0.062  ±0.006
test d16 T12 ow0.3: acc 0.923  margin 0.279  ±0.004
test d16 T12 ow0.0: acc 0.872  margin 0.231  ±0.004
test d16 T12 ow0.6: acc 0.953  margin 0.296  ±0.004
test d32 T24 ow0.3: acc 0.977  margin 0.365  ±0.002
test d8 T6 ow0.3: acc 0.825  margin 0.129  ±0.008
test d16 T64 K8 ow0.3: acc 0.870  margin 0.218  ±0.007
test d16 T128 K8 ow0.3: acc 0.881  margin 0.218  ±0.010
```

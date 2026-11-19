# Search seed 26

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 953193  time: 2638s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 150004 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* linear, not error-correcting: 4212 candidates
* unclassified: 5364 candidates
* delta rule: 13684 candidates
* delta + Kronecker mix: 30708 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 10356 candidates
- delta rule (beta=1) (acc 0.578): 13044 candidates
- delta rule (beta=0.5) (acc 0.617): 30708 candidates
- gated delta (alpha=0.9) (acc 0.519): 10868 candidates

## Best rule

```
S' = ((P1 - (((0.293 + 0)·P1·tanh(tanh(k)) - (v - 0)))⊗((tanh(tanh(k)) + k))) - ((P1 - (((0.293 + 0)·P1·tanh(tanh(k)) - (v - 0)))⊗((tanh(tanh(k)) + k))))((0.293 + 0)·(k)⊗((tanh(tanh(k)) + k))))
P1' = (P1 - (((0.293 + 0)·P1·tanh(tanh(k)) - (v - 0)))⊗((tanh(tanh(k)) + k)))
P2' = ((P1 - (((0.293 + 0)·P1·tanh(tanh(k)) - (v - 0)))⊗((tanh(tanh(k)) + k))))((0.293 + 0)·(k)⊗((tanh(tanh(k)) + k)))

Effective program (15 instructions):
  s2 = 0.2925
  V5 = VecSub(V1, V3)
  V1 = Tanh(V0)
  V1 = Tanh(V1)
  V2 = MatVec(M1, V1)
  s2 = SAdd(s2, s0)
  V4 = VecScale(s2, V2)
  V2 = VecSub(V4, V5)
  V1 = VecAdd(V1, V0)
  M2 = Outer(V2, V1)
  M1 = MatSub(M1, M2)
  M2 = Outer(V0, V1)
  M2 = MatScale(s2, M2)
  M2 = MatMul(M1, M2)
  M0 = MatSub(M1, M2)

structure: unclassified  [a=1.032 b=0.845 c=-0.792 g=0.002, erase c/a=0.768, R²=0.6204, 1408 steps]

train acc 0.653 ±0.014
test regime collision3: acc 0.668  margin 0.073  ±0.006
test d16 T12 ow0.3: acc 0.931  margin 0.262  ±0.004
test d16 T12 ow0.0: acc 0.897  margin 0.232  ±0.004
test d16 T12 ow0.6: acc 0.950  margin 0.267  ±0.004
test d32 T24 ow0.3: acc 0.984  margin 0.350  ±0.002
test d8 T6 ow0.3: acc 0.804  margin 0.112  ±0.008
test d16 T64 K8 ow0.3: acc 0.846  margin 0.170  ±0.008
test d16 T128 K8 ow0.3: acc 0.849  margin 0.164  ±0.011
```

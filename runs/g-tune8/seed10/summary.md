# Search seed 10

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500068  real evaluations (after cache): 1129701  time: 2793s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 450244 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2036 candidates
* unclassified: 3572 candidates
* linear attention: 6524 candidates
* gated delta rule: 261676 candidates
* delta rule: 262148 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6524 candidates
- delta rule (beta=1) (acc 0.578): 262148 candidates
- delta rule (beta=0.5) (acc 0.617): 273964 candidates
- gated delta (alpha=0.9) (acc 0.519): 261676 candidates

## Best rule

```
S' = ((((0 - (P2 + (S - P1)))·tanh(tanh(k)))⊗(tanh(k)) + (P2 + (S - P1))) - -0.442·(tanh(v))⊗((tanh(tanh(k)) + tanh(k))))
P1' = -0.442·(tanh(v))⊗((tanh(tanh(k)) + tanh(k)))
P2' = (tanh(v))⊗((tanh(tanh(k)) + tanh(k)))

Effective program (14 instructions):
  M0 = MatSub(M0, M1)
  s0 = -0.4423
  M0 = MatAdd(M2, M0)
  M2 = MatSub(M3, M0)
  V5 = Tanh(V0)
  V3 = Tanh(V5)
  V1 = Tanh(V1)
  V0 = MatVec(M2, V3)
  V2 = VecAdd(V3, V5)
  M2 = Outer(V1, V2)
  M1 = Outer(V0, V5)
  M0 = MatAdd(M1, M0)
  M1 = MatScale(s0, M2)
  M0 = MatSub(M0, M1)

structure: unclassified  [a=1.035 b=0.778 c=-0.879 g=0.003, erase c/a=0.849, R²=0.5368, 1408 steps]

train acc 0.667 ±0.013
test regime collision3: acc 0.674  margin 0.062  ±0.006
test d16 T12 ow0.3: acc 0.910  margin 0.285  ±0.004
test d16 T12 ow0.0: acc 0.851  margin 0.224  ±0.005
test d16 T12 ow0.6: acc 0.949  margin 0.313  ±0.004
test d32 T24 ow0.3: acc 0.965  margin 0.368  ±0.003
test d8 T6 ow0.3: acc 0.789  margin 0.116  ±0.009
test d16 T64 K8 ow0.3: acc 0.866  margin 0.233  ±0.008
test d16 T128 K8 ow0.3: acc 0.891  margin 0.232  ±0.010
```

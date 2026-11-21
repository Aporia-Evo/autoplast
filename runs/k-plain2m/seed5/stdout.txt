# Search seed 5

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 2100084  real evaluations (after cache): 925441  time: 1872s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4980 candidates
* linear attention: 8948 candidates
* unclassified: 763380 candidates
* delta rule: 766068 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8948 candidates
- delta rule (beta=1) (acc 0.578): 766068 candidates
- delta rule (beta=0.5) (acc 0.617): 767220 candidates
- gated delta (alpha=0.9) (acc 0.519): 763380 candidates

## Best rule

```
S' = ((S + 0.702·(tanh(1.406·v))⊗(k)) + ((tanh(tanh(1.406·v)) - P2·tanh(k)))⊗(tanh(k)))
P1' = (S + 0.702·(tanh(1.406·v))⊗(k))
P2' = 0.702·0.702·(S + 0.702·(tanh(1.406·v))⊗(k))

Effective program (15 instructions):
  s0 = 1.4064
  V5 = VecScale(s0, V1)
  V5 = Tanh(V5)
  s3 = 0.7018
  V4 = Tanh(V0)
  M1 = Outer(V5, V0)
  V3 = MatVec(M2, V4)
  V0 = Tanh(V5)
  V3 = VecSub(V0, V3)
  s0 = SMul(s3, s3)
  M2 = MatScale(s3, M1)
  M1 = MatAdd(M0, M2)
  M3 = Outer(V3, V4)
  M0 = MatAdd(M1, M3)
  M2 = MatScale(s0, M1)

structure: unclassified  [a=1.000 b=2.019 c=-0.418 g=0.005, erase c/a=0.418, R²=0.9708, 1408 steps]

train acc 0.627 ±0.014
test regime collision3: acc 0.641  margin 0.036  ±0.006
test d16 T12 ow0.3: acc 0.906  margin 0.239  ±0.004
test d16 T12 ow0.0: acc 0.904  margin 0.228  ±0.004
test d16 T12 ow0.6: acc 0.904  margin 0.221  ±0.006
test d32 T24 ow0.3: acc 0.981  margin 0.335  ±0.002
test d8 T6 ow0.3: acc 0.726  margin 0.083  ±0.009
test d16 T64 K8 ow0.3: acc 0.786  margin 0.117  ±0.009
test d16 T128 K8 ow0.3: acc 0.771  margin 0.109  ±0.013
```

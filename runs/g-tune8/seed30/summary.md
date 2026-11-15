# Search seed 30

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500004  real evaluations (after cache): 934166  time: 3232s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 350180 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2164 candidates
* unclassified: 2420 candidates
* linear attention: 5876 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5876 candidates
- delta rule (beta=1) (acc 0.578): 331844 candidates
- delta rule (beta=0.5) (acc 0.617): 331844 candidates
- gated delta (alpha=0.9) (acc 0.519): 331140 candidates

## Best rule

```
S' = ((0.496·P2 + 1/(0.163)·((v)⊗(k) + (v)⊗(k))) - ((0.496·P2 + 1/(0.163)·((v)⊗(k) + (v)⊗(k))))((tanh(k))⊗(k)))
P1' = (0.496·P2 + 1/(0.163)·((v)⊗(k) + (v)⊗(k)))
P2' = ((0.496·P2 + 1/(0.163)·((v)⊗(k) + (v)⊗(k))) + ((0.496·P2 + 1/(0.163)·((v)⊗(k) + (v)⊗(k))) - ((0.496·P2 + 1/(0.163)·((v)⊗(k) + (v)⊗(k))))((tanh(k))⊗(k))))

Effective program (13 instructions):
  M0 = Outer(V1, V0)
  M3 = MatAdd(M0, M0)
  s0 = 0.1634
  s2 = Recip(s0)
  M3 = MatScale(s2, M3)
  s1 = 0.4961
  M0 = MatScale(s1, M2)
  M1 = MatAdd(M0, M3)
  V2 = Tanh(V0)
  M2 = Outer(V2, V0)
  M3 = MatMul(M1, M2)
  M0 = MatSub(M1, M3)
  M2 = MatAdd(M1, M0)

structure: unclassified  [a=1.013 b=0.676 c=-0.955 g=0.003, erase c/a=0.942, R²=0.4540, 1408 steps]

train acc 0.686 ±0.013
test regime collision3: acc 0.694  margin 0.090  ±0.006
test d16 T12 ow0.3: acc 0.933  margin 0.273  ±0.004
test d16 T12 ow0.0: acc 0.908  margin 0.246  ±0.004
test d16 T12 ow0.6: acc 0.957  margin 0.274  ±0.004
test d32 T24 ow0.3: acc 0.983  margin 0.350  ±0.002
test d8 T6 ow0.3: acc 0.831  margin 0.136  ±0.008
test d16 T64 K8 ow0.3: acc 0.839  margin 0.167  ±0.008
test d16 T128 K8 ow0.3: acc 0.853  margin 0.166  ±0.011
```

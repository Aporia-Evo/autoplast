# Search seed 29

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 653520  time: 2598s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1396 candidates
* linear attention: 7156 candidates
* delta rule: 764660 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 7156 candidates
- delta rule (beta=1) (acc 0.578): 763636 candidates
- delta rule (beta=0.5) (acc 0.617): 764660 candidates
- gated delta (alpha=0.9) (acc 0.519): 162292 candidates

## Best rule

```
S' = ((S + (v)⊗(tanh(tanh(tanh(k))))) - |(S·tanh(tanh(k)) - (v)⊗(tanh(tanh(tanh(k))))·norm((v + S·tanh(tanh(k)))))|·((S + (v)⊗(tanh(tanh(tanh(k))))))((tanh(tanh(tanh(k))))⊗(tanh(tanh(k)))))
P1' = |(S·tanh(tanh(k)) - (v)⊗(tanh(tanh(tanh(k))))·norm((v + S·tanh(tanh(k)))))|·((S + (v)⊗(tanh(tanh(tanh(k))))))((tanh(tanh(tanh(k))))⊗(tanh(tanh(k))))
P2' = (S + (v)⊗(tanh(tanh(tanh(k)))))

Effective program (15 instructions):
  V5 = Tanh(V0)
  V5 = Tanh(V5)
  V2 = Tanh(V5)
  M3 = Outer(V2, V5)
  M1 = Outer(V1, V2)
  M2 = MatAdd(M0, M1)
  V4 = MatVec(M0, V5)
  V0 = VecAdd(V1, V4)
  V3 = Normalize(V0)
  V3 = MatVec(M1, V3)
  M1 = MatMul(M2, M3)
  V0 = VecSub(V4, V3)
  s0 = Norm(V0)
  M1 = MatScale(s0, M1)
  M0 = MatSub(M2, M1)

structure: unclassified  [a=0.999 b=0.516 c=-0.465 g=-0.029, erase c/a=0.466, R²=0.9447, 1408 steps]

train acc 0.649 ±0.014
test regime collision3: acc 0.648  margin 0.048  ±0.006
test d16 T12 ow0.3: acc 0.892  margin 0.238  ±0.005
test d16 T12 ow0.0: acc 0.931  margin 0.242  ±0.003
test d16 T12 ow0.6: acc 0.889  margin 0.220  ±0.006
test d32 T24 ow0.3: acc 0.939  margin 0.326  ±0.004
test d8 T6 ow0.3: acc 0.728  margin 0.085  ±0.009
test d16 T64 K8 ow0.3: acc 0.785  margin 0.130  ±0.009
test d16 T128 K8 ow0.3: acc 0.783  margin 0.120  ±0.013
```

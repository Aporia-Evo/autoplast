# Search seed 29

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500124  real evaluations (after cache): 735932  time: 1646s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* unclassified: 5500 candidates
* linear attention: 6652 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6396 candidates
- delta rule (beta=1) (acc 0.578): 1272732 candidates
- delta rule (beta=0.5) (acc 0.617): 1275308 candidates
- gated delta (alpha=0.9) (acc 0.519): 1271420 candidates

## Best rule

```
S' = ((S + (tanh(v))⊗(tanh(tanh(tanh(k))))) - ((S + (tanh(v))⊗(tanh(tanh(tanh(k))))))((tanh(tanh(tanh(k))))⊗(|S·tanh(tanh(tanh(k)))|·tanh(tanh(k)))))
P1' = (tanh(v))⊗(tanh(tanh(tanh(k))))
P2' = ((S + (tanh(v))⊗(tanh(tanh(tanh(k))))))((tanh(tanh(tanh(k))))⊗(|S·tanh(tanh(tanh(k)))|·tanh(tanh(k))))

Effective program (12 instructions):
  V5 = Tanh(V0)
  V3 = Tanh(V5)
  V0 = Tanh(V3)
  V2 = MatVec(M0, V0)
  V4 = Tanh(V1)
  s1 = Norm(V2)
  M1 = Outer(V4, V0)
  M0 = MatAdd(M0, M1)
  V4 = VecScale(s1, V3)
  M3 = Outer(V0, V4)
  M2 = MatMul(M0, M3)
  M0 = MatSub(M0, M2)

structure: unclassified  [a=1.000 b=0.524 c=-0.431 g=-0.033, erase c/a=0.432, R²=0.9468, 1408 steps]

train acc 0.636 ±0.014
test regime collision3: acc 0.649  margin 0.048  ±0.006
test d16 T12 ow0.3: acc 0.888  margin 0.232  ±0.005
test d16 T12 ow0.0: acc 0.937  margin 0.242  ±0.003
test d16 T12 ow0.6: acc 0.867  margin 0.207  ±0.006
test d32 T24 ow0.3: acc 0.932  margin 0.320  ±0.004
test d8 T6 ow0.3: acc 0.702  margin 0.074  ±0.010
test d16 T64 K8 ow0.3: acc 0.771  margin 0.115  ±0.009
test d16 T128 K8 ow0.3: acc 0.764  margin 0.105  ±0.013
```

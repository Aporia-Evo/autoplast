# Search seed 2

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 2100084  real evaluations (after cache): 1532764  time: 4748s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 100084 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1268 candidates
* decayed linear attention: 2164 candidates
* linear attention: 4596 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 4596 candidates
- delta rule (beta=1) (acc 0.578): 76788 candidates
- delta rule (beta=0.5) (acc 0.617): 83060 candidates
- gated delta (alpha=0.9) (acc 0.519): 76404 candidates

## Best rule

```
S' = (((P2 - P1) - ((P2 - P1)·tanh(tanh(k)))⊗(tanh(tanh(tanh(k))))) + |(P2 - P1)·tanh(tanh(k))|·(((P2 - P1) - ((P2 - P1)·tanh(tanh(k)))⊗(tanh(tanh(tanh(k))))) + ((tanh(v))⊗(k) + ((P2 - P1) - ((P2 - P1)·tanh(tanh(k)))⊗(tanh(tanh(tanh(k))))))))
P1' = ((((P2 - P1)·tanh(tanh(k)) - (tanh(tanh(tanh(k))) - norm(tanh(tanh(tanh(tanh(k))))))) + norm(((P2 - P1)·tanh(tanh(k)) - (tanh(tanh(tanh(k))) - norm(tanh(tanh(tanh(tanh(k))))))))))⊗((tanh(tanh(tanh(k))) - norm(tanh(tanh(tanh(tanh(k)))))))
P2' = ((tanh(v))⊗(k) + ((P2 - P1) - ((P2 - P1)·tanh(tanh(k)))⊗(tanh(tanh(tanh(k))))))

Effective program (21 instructions):
  V2 = Tanh(V1)
  M0 = Outer(V2, V0)
  V2 = Tanh(V0)
  V3 = Tanh(V2)
  V0 = Tanh(V3)
  M2 = MatSub(M2, M1)
  V1 = Tanh(V0)
  V2 = Normalize(V1)
  V5 = VecSub(V0, V2)
  V2 = MatVec(M2, V3)
  s3 = Norm(V2)
  M3 = Outer(V2, V0)
  M3 = MatSub(M2, M3)
  M2 = MatAdd(M0, M3)
  V2 = VecSub(V2, V5)
  M0 = MatAdd(M3, M2)
  V0 = Normalize(V2)
  V3 = VecAdd(V2, V0)
  M1 = Outer(V3, V5)
  M0 = MatScale(s3, M0)
  M0 = MatAdd(M3, M0)

structure: unclassified  [a=1.032 b=0.761 c=-0.782 g=0.018, erase c/a=0.758, R²=0.5036, 1408 steps]

train acc 0.676 ±0.013
test regime collision3: acc 0.683  margin 0.082  ±0.006
test d16 T12 ow0.3: acc 0.940  margin 0.278  ±0.004
test d16 T12 ow0.0: acc 0.913  margin 0.244  ±0.004
test d16 T12 ow0.6: acc 0.953  margin 0.276  ±0.004
test d32 T24 ow0.3: acc 0.984  margin 0.377  ±0.002
test d8 T6 ow0.3: acc 0.697  margin 0.066  ±0.010
test d16 T64 K8 ow0.3: acc 0.842  margin 0.182  ±0.008
test d16 T128 K8 ow0.3: acc 0.850  margin 0.170  ±0.011
```

# Search seed 2

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1084769  time: 3529s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

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
S' = (((P2 - P1) - ((P2 - P1)·tanh(tanh(k)))⊗(tanh(tanh(tanh(k))))) + |tanh((P2 - P1)·tanh(tanh(k)))|·(((P2 - P1) - ((P2 - P1)·tanh(tanh(k)))⊗(tanh(tanh(tanh(k))))) + ((tanh(v))⊗(k) + ((P2 - P1) - ((P2 - P1)·tanh(tanh(k)))⊗(tanh(tanh(tanh(k))))))))
P1' = ((norm((((P2 - P1)·tanh(tanh(k)))⊗(tanh(tanh(tanh(k))))·tanh(tanh(k)) - (tanh(tanh(tanh(k))) - norm(tanh(tanh(tanh(tanh(k)))))))) + norm((((P2 - P1)·tanh(tanh(k)))⊗(tanh(tanh(tanh(k))))·tanh(tanh(k)) - (tanh(tanh(tanh(k))) - norm(tanh(tanh(tanh(tanh(k))))))))))⊗((tanh(tanh(tanh(k))) - norm(tanh(tanh(tanh(tanh(k)))))))
P2' = ((tanh(v))⊗(k) + ((P2 - P1) - ((P2 - P1)·tanh(tanh(k)))⊗(tanh(tanh(tanh(k))))))

Effective program (23 instructions):
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
  V4 = Tanh(V2)
  s3 = Norm(V4)
  M3 = Outer(V2, V0)
  V0 = MatVec(M3, V3)
  M3 = MatSub(M2, M3)
  M2 = MatAdd(M0, M3)
  V2 = VecSub(V0, V5)
  M0 = MatAdd(M3, M2)
  V0 = Normalize(V2)
  V3 = VecAdd(V0, V0)
  M1 = Outer(V3, V5)
  M0 = MatScale(s3, M0)
  M0 = MatAdd(M3, M0)

structure: unclassified  [a=1.033 b=0.733 c=-0.784 g=0.017, erase c/a=0.759, R²=0.5048, 1408 steps]

train acc 0.676 ±0.013
test regime collision3: acc 0.684  margin 0.081  ±0.006
test d16 T12 ow0.3: acc 0.941  margin 0.272  ±0.004
test d16 T12 ow0.0: acc 0.914  margin 0.237  ±0.004
test d16 T12 ow0.6: acc 0.953  margin 0.271  ±0.004
test d32 T24 ow0.3: acc 0.986  margin 0.377  ±0.002
test d8 T6 ow0.3: acc 0.656  margin 0.045  ±0.010
test d16 T64 K8 ow0.3: acc 0.847  margin 0.181  ±0.008
test d16 T128 K8 ow0.3: acc 0.851  margin 0.170  ±0.011
```

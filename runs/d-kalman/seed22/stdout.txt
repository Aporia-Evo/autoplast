# Search seed 22

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 825063  time: 1731s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 4852 candidates
* decayed linear attention: 6260 candidates
* linear attention: 12404 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 12404 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 211444 candidates

## Best rule

```
S' = ((v)⊗((((P2)ᵀ·P1·tanh(k) + ((norm(tanh(k)) + tanh(k)) + (P2)ᵀ·P1·tanh(k))) - tanh(P1·P1·tanh(k)))) + 0.896·S)
P1' = ((P2)ᵀ·(P2)ᵀ·P1·tanh(k))⊗(norm(tanh(k)))
P2' = (v)⊗((((P2)ᵀ·P1·tanh(k) + ((norm(tanh(k)) + tanh(k)) + (P2)ᵀ·P1·tanh(k))) - tanh(P1·P1·tanh(k))))

Effective program (17 instructions):
  M2 = Transpose(M2)
  V3 = Tanh(V0)
  s2 = 0.8962
  M0 = MatScale(s2, M0)
  V4 = Normalize(V3)
  V0 = VecAdd(V4, V3)
  V2 = MatVec(M1, V3)
  V5 = MatVec(M2, V2)
  V0 = VecAdd(V0, V5)
  V3 = VecAdd(V5, V0)
  V5 = MatVec(M2, V5)
  V2 = MatVec(M1, V2)
  V2 = Tanh(V2)
  M1 = Outer(V5, V4)
  V3 = VecSub(V3, V2)
  M2 = Outer(V1, V3)
  M0 = MatAdd(M2, M0)

structure: unclassified  [a=0.896 b=1.973 c=0.000 g=-0.015, erase c/a=-0.000, R²=0.9844, 1408 steps]

train acc 0.519 ±0.014
test regime collision3: acc 0.000  margin 0.000  ±0.000
test d16 T12 ow0.3: acc 0.756  margin 0.134  ±0.006
test d16 T12 ow0.0: acc 0.780  margin 0.148  ±0.005
test d16 T12 ow0.6: acc 0.702  margin 0.097  ±0.009
test d32 T24 ow0.3: acc 0.698  margin 0.140  ±0.007
test d8 T6 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T64 K8 ow0.3: acc 0.577  margin -0.006  ±0.011
test d16 T128 K8 ow0.3: acc 0.561  margin -0.024  ±0.016
```

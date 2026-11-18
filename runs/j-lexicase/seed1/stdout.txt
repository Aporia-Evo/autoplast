# Search seed 1

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 877711  time: 2422s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 250100 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1012 candidates
* unclassified: 4724 candidates
* linear attention: 5236 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5236 candidates
- delta rule (beta=1) (acc 0.578): 198516 candidates
- delta rule (beta=0.5) (acc 0.617): 200692 candidates
- gated delta (alpha=0.9) (acc 0.519): 94708 candidates

## Best rule

```
S' = …
P1' = -0.161·((((((P2 + (tanh(tanh(v)))⊗((k + k))) + |tanh((k + k))|·(tanh(tanh(v)))⊗((k + k))) + (tanh(tanh(v)))⊗((k + k)))·tanh((k + k)) - ((k + k) ⊙ tanh(tanh(tanh(v))))) - tanh(tanh(tanh(v)))))⊗(tanh((k + k)))
P2' = (-0.161·((((((P2 + (tanh(tanh(v)))⊗((k + k))) + |tanh((k + k))|·(tanh(tanh(v)))⊗((k + k))) + (tanh(tanh(v)))⊗((k + k)))·tanh((k + k)) - ((k + k) ⊙ tanh(tanh(tanh(v))))) - tanh(tanh(tanh(v)))))⊗(tanh((k + k))) + ((tanh(tanh(v)))⊗((k + k)) + (((P2 + (tanh(tanh(v)))⊗((k + k))) + |tanh((k + k))|·(tanh(tanh(v)))⊗((k + k))) + (tanh(tanh(v)))⊗((k + k)))))

Effective program (22 instructions):
  V3 = VecAdd(V0, V0)
  V5 = Tanh(V3)
  V0 = Tanh(V1)
  s0 = Norm(V5)
  V2 = Tanh(V0)
  V1 = Tanh(V2)
  V4 = Hadamard(V3, V1)
  M0 = Outer(V2, V3)
  M3 = MatAdd(M2, M0)
  M1 = MatScale(s0, M0)
  M3 = MatAdd(M3, M1)
  M2 = MatAdd(M3, M0)
  V3 = MatVec(M2, V5)
  V2 = VecSub(V3, V4)
  V0 = VecSub(V2, V1)
  s2 = -0.1609
  M3 = Outer(V0, V5)
  M2 = MatAdd(M0, M2)
  M1 = MatScale(s2, M3)
  M0 = MatSub(M0, M1)
  M2 = MatAdd(M1, M2)
  M0 = MatSub(M2, M0)

structure: unclassified  [a=1.031 b=1.269 c=-0.881 g=0.008, erase c/a=0.854, R²=0.5024, 1408 steps]

train acc 0.684 ±0.013
test regime collision3: acc 0.684  margin 0.081  ±0.006
test d16 T12 ow0.3: acc 0.932  margin 0.263  ±0.004
test d16 T12 ow0.0: acc 0.914  margin 0.241  ±0.004
test d16 T12 ow0.6: acc 0.941  margin 0.252  ±0.005
test d32 T24 ow0.3: acc 0.951  margin 0.321  ±0.003
test d8 T6 ow0.3: acc 0.768  margin 0.103  ±0.009
test d16 T64 K8 ow0.3: acc 0.795  margin 0.128  ±0.009
test d16 T128 K8 ow0.3: acc 0.773  margin 0.113  ±0.013
```

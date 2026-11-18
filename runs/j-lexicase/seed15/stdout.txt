# Search seed 15

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 837117  time: 4146s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 350068 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1908 candidates
* decayed linear attention: 2164 candidates
* linear attention: 3572 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3572 candidates
- delta rule (beta=1) (acc 0.578): 246644 candidates
- delta rule (beta=0.5) (acc 0.617): 251252 candidates
- gated delta (alpha=0.9) (acc 0.519): 221300 candidates

## Best rule

```
S' = (((tanh(v))⊗(((0 + k) + k)) + (tanh(v))⊗(((0 + k) + k))) + (((k)⊗((0 + k)) + (S + ((P1 + P1) + (P1 + P1)))) - (((k)⊗((0 + k)) + (S + ((P1 + P1) + (P1 + P1)))))(0.935·(k)⊗((0 + k)))))
P1' = ((((((tanh(v))⊗(((0 + k) + k)) + (tanh(v))⊗(((0 + k) + k))) + (((k)⊗((0 + k)) + (S + ((P1 + P1) + (P1 + P1)))) - (((k)⊗((0 + k)) + (S + ((P1 + P1) + (P1 + P1)))))(0.935·(k)⊗((0 + k))))) + (tanh(v))⊗(((0 + k) + k))) + (((k)⊗((0 + k)) + (S + ((P1 + P1) + (P1 + P1)))) - (((k)⊗((0 + k)) + (S + ((P1 + P1) + (P1 + P1)))))(0.935·(k)⊗((0 + k))))))(0.935·(k)⊗((0 + k)))
P2' = ((((tanh(v))⊗(((0 + k) + k)) + (tanh(v))⊗(((0 + k) + k))) + (((k)⊗((0 + k)) + (S + ((P1 + P1) + (P1 + P1)))) - (((k)⊗((0 + k)) + (S + ((P1 + P1) + (P1 + P1)))))(0.935·(k)⊗((0 + k))))) + (tanh(v))⊗(((0 + k) + k)))

Effective program (18 instructions):
  M1 = MatAdd(M1, M1)
  M1 = MatAdd(M1, M1)
  M0 = MatAdd(M0, M1)
  s1 = 0.9349
  V3 = VecAdd(V2, V0)
  M1 = Outer(V0, V3)
  M3 = MatScale(s1, M1)
  M1 = MatAdd(M1, M0)
  M2 = MatMul(M1, M3)
  M1 = MatSub(M1, M2)
  V4 = VecAdd(V3, V0)
  V3 = Tanh(V1)
  M2 = Outer(V3, V4)
  M0 = MatAdd(M2, M2)
  M0 = MatAdd(M0, M1)
  M2 = MatAdd(M0, M2)
  M1 = MatAdd(M2, M1)
  M1 = MatMul(M1, M3)

structure: unclassified  [a=1.024 b=3.807 c=-0.956 g=0.001, erase c/a=0.933, R²=0.4934, 1408 steps]

train acc 0.681 ±0.013
test regime collision3: acc 0.690  margin 0.091  ±0.006
test d16 T12 ow0.3: acc 0.935  margin 0.273  ±0.004
test d16 T12 ow0.0: acc 0.919  margin 0.250  ±0.003
test d16 T12 ow0.6: acc 0.955  margin 0.270  ±0.004
test d32 T24 ow0.3: acc 0.988  margin 0.350  ±0.002
test d8 T6 ow0.3: acc 0.839  margin 0.139  ±0.008
test d16 T64 K8 ow0.3: acc 0.819  margin 0.146  ±0.009
test d16 T128 K8 ow0.3: acc 0.810  margin 0.140  ±0.012
```

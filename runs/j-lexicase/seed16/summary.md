# Search seed 16

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 989361  time: 5465s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 4212 candidates
* decayed linear attention: 5364 candidates
* linear attention: 11124 candidates
* delta rule: 68468 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 11124 candidates
- delta rule (beta=1) (acc 0.578): 68468 candidates
- delta rule (beta=0.5) (acc 0.617): 68468 candidates
- gated delta (alpha=0.9) (acc 0.519): 46964 candidates

## Best rule

```
S' = (((v)⊗((tanh(tanh(k)) + tanh(tanh(k)))) + (((norm(tanh(k)))⊗(tanh(tanh(tanh(tanh(k))))))(((((P2 - (P1 + S)) - P1) - P1))ᵀ))ᵀ) - ((P2 - (P1 + S)) - P1))
P1' = (((v)⊗((tanh(tanh(k)) + tanh(tanh(k)))) + (((norm(tanh(k)))⊗(tanh(tanh(tanh(tanh(k))))))(((((P2 - (P1 + S)) - P1) - P1))ᵀ))ᵀ) - (((norm(tanh(k)))⊗(tanh(tanh(tanh(tanh(k))))))(((((P2 - (P1 + S)) - P1) - P1))ᵀ))ᵀ)
P2' = (σ(0)·(((norm(tanh(k)))⊗(tanh(tanh(tanh(tanh(k))))))(((((P2 - (P1 + S)) - P1) - P1))ᵀ))ᵀ - (((v)⊗((tanh(tanh(k)) + tanh(tanh(k)))) + (((norm(tanh(k)))⊗(tanh(tanh(tanh(tanh(k))))))(((((P2 - (P1 + S)) - P1) - P1))ᵀ))ᵀ) - (((norm(tanh(k)))⊗(tanh(tanh(tanh(tanh(k))))))(((((P2 - (P1 + S)) - P1) - P1))ᵀ))ᵀ))

Effective program (21 instructions):
  M0 = MatAdd(M1, M0)
  M0 = MatSub(M2, M0)
  M2 = MatSub(M0, M1)
  M0 = MatSub(M2, M1)
  M1 = Transpose(M0)
  V4 = Tanh(V0)
  V5 = Normalize(V4)
  V3 = Tanh(V4)
  s1 = Sigmoid(s0)
  V2 = Tanh(V3)
  V0 = VecAdd(V3, V3)
  M0 = Outer(V1, V0)
  V0 = Tanh(V2)
  M3 = Outer(V5, V0)
  M1 = MatMul(M3, M1)
  M3 = Transpose(M1)
  M1 = MatAdd(M0, M3)
  M0 = MatSub(M1, M2)
  M1 = MatSub(M1, M3)
  M2 = MatScale(s1, M3)
  M2 = MatSub(M2, M1)

structure: unclassified  [a=1.036 b=1.800 c=-0.874 g=0.002, erase c/a=0.843, R²=0.5266, 1408 steps]

train acc 0.683 ±0.013
test regime collision3: acc 0.681  margin 0.081  ±0.006
test d16 T12 ow0.3: acc 0.939  margin 0.269  ±0.004
test d16 T12 ow0.0: acc 0.921  margin 0.246  ±0.003
test d16 T12 ow0.6: acc 0.948  margin 0.261  ±0.004
test d32 T24 ow0.3: acc 0.988  margin 0.355  ±0.002
test d8 T6 ow0.3: acc 0.779  margin 0.108  ±0.009
test d16 T64 K8 ow0.3: acc 0.804  margin 0.130  ±0.009
test d16 T128 K8 ow0.3: acc 0.785  margin 0.119  ±0.013
```

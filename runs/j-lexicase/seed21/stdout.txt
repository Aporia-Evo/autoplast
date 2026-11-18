# Search seed 21

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 860919  time: 8972s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 350068 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2164 candidates
* unclassified: 3188 candidates
* linear attention: 8052 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8052 candidates
- delta rule (beta=1) (acc 0.578): 272884 candidates
- delta rule (beta=0.5) (acc 0.617): 274932 candidates
- gated delta (alpha=0.9) (acc 0.519): 252276 candidates

## Best rule

```
S' = ((((0.444·(v)⊗(k) + 0.444·(v)⊗(k)) + …))((… + …)) + (0.444·(v)⊗(k) + (P1 - ((P1)((k)⊗(tanh(tanh(k)))))(((k)⊗(tanh(tanh(k))))(((k)⊗(tanh(tanh(k))))ᵀ)))))
P1' = (0.444·(v)⊗(k) + (P1 - ((P1)((k)⊗(tanh(tanh(k)))))(((k)⊗(tanh(tanh(k))))(((k)⊗(tanh(tanh(k))))ᵀ))))
P2' = (… + …)

Effective program (20 instructions):
  V3 = Tanh(V0)
  V2 = Tanh(V3)
  M3 = Outer(V0, V2)
  M2 = MatMul(M1, M3)
  s0 = 0.4441
  M0 = Transpose(M3)
  M0 = MatMul(M3, M0)
  M3 = MatMul(M2, M0)
  M3 = MatSub(M1, M3)
  M0 = Outer(V1, V0)
  M2 = MatScale(s0, M0)
  M0 = MatAdd(M2, M2)
  M1 = MatAdd(M2, M3)
  M3 = MatMul(M1, M3)
  M2 = MatSub(M3, M2)
  M3 = MatMul(M2, M3)
  M2 = MatAdd(M3, M3)
  M3 = MatAdd(M0, M3)
  M0 = MatMul(M3, M2)
  M0 = MatAdd(M0, M1)

structure: unclassified  [a=0.996 b=0.493 c=-0.838 g=-0.004, erase c/a=0.841, R²=0.2471, 1408 steps]

train acc 0.690 ±0.013
test regime collision3: acc 0.700  margin 0.087  ±0.006
test d16 T12 ow0.3: acc 0.885  margin 0.197  ±0.005
test d16 T12 ow0.0: acc 0.768  margin 0.119  ±0.005
test d16 T12 ow0.6: acc 0.942  margin 0.245  ±0.004
test d32 T24 ow0.3: acc 0.976  margin 0.296  ±0.002
test d8 T6 ow0.3: acc 0.624  margin 0.027  ±0.010
test d16 T64 K8 ow0.3: acc 0.807  margin 0.147  ±0.009
test d16 T128 K8 ow0.3: acc 0.806  margin 0.148  ±0.012
```

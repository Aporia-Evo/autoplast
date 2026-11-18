# Search seed 27

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 884536  time: 4269s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 300020 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2164 candidates
* decayed linear attention: 3956 candidates
* linear attention: 6900 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6900 candidates
- delta rule (beta=1) (acc 0.578): 212596 candidates
- delta rule (beta=0.5) (acc 0.617): 221300 candidates
- gated delta (alpha=0.9) (acc 0.519): 146420 candidates

## Best rule

```
S' = (((norm(tanh(tanh(v))))⊗(k) - ((P2 + (tanh(k))⊗(k)))((tanh(k))⊗(k))) + (P2 + (tanh(k))⊗(k)))
P1' = 0.489·((norm(tanh(tanh(v))))⊗(k) - ((P2 + (tanh(k))⊗(k)))((tanh(k))⊗(k)))
P2' = (((1/(σ(-1.124)) + 1/(σ(-1.124)))·(norm(tanh(tanh(v))))⊗(k) + (P2 + (tanh(k))⊗(k))) + 0.489·((norm(tanh(tanh(v))))⊗(k) - ((P2 + (tanh(k))⊗(k)))((tanh(k))⊗(k))))

Effective program (19 instructions):
  V1 = Tanh(V1)
  V3 = Tanh(V1)
  V1 = Normalize(V3)
  M0 = Outer(V1, V0)
  s0 = -1.1243
  s0 = Sigmoid(s0)
  s0 = Recip(s0)
  s0 = SAdd(s0, s0)
  V1 = Tanh(V0)
  M3 = Outer(V1, V0)
  M2 = MatAdd(M2, M3)
  s2 = 0.4890
  M1 = MatMul(M2, M3)
  M1 = MatSub(M0, M1)
  M3 = MatScale(s0, M0)
  M3 = MatAdd(M3, M2)
  M0 = MatAdd(M1, M2)
  M1 = MatScale(s2, M1)
  M2 = MatAdd(M3, M1)

structure: unclassified  [a=1.020 b=1.001 c=-0.961 g=0.001, erase c/a=0.942, R²=0.4765, 1408 steps]

train acc 0.689 ±0.013
test regime collision3: acc 0.690  margin 0.091  ±0.006
test d16 T12 ow0.3: acc 0.935  margin 0.272  ±0.004
test d16 T12 ow0.0: acc 0.914  margin 0.245  ±0.004
test d16 T12 ow0.6: acc 0.953  margin 0.269  ±0.004
test d32 T24 ow0.3: acc 0.987  margin 0.354  ±0.002
test d8 T6 ow0.3: acc 0.792  margin 0.113  ±0.008
test d16 T64 K8 ow0.3: acc 0.817  margin 0.148  ±0.009
test d16 T128 K8 ow0.3: acc 0.812  margin 0.139  ±0.012
```

# Search seed 807

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 762490  time: 4311s  pop: 500  tournament: 10

commit: dce11aa  task seed: 807  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 1100020 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 1012 candidates
* linear attention: 3316 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.383): 3316 candidates
- delta rule (beta=1) (acc 0.594): 257652 candidates
- delta rule (beta=0.5) (acc 0.628): 274676 candidates
- gated delta (alpha=0.9) (acc 0.516): 104180 candidates

## Best rule

```
S' = ((S + (((P2 - P1) + S) + (tanh(v))⊗(k))) - (((S + (((P2 - P1) + S) + (tanh(v))⊗(k))))(((tanh(v))⊗(k))ᵀ))((v)⊗(k)))
P1' = (S + (((P2 - P1) + S) + (tanh(v))⊗(k)))
P2' = 1.435·(((S + (((P2 - P1) + S) + (tanh(v))⊗(k))))(((tanh(v))⊗(k))ᵀ))((v)⊗(k))

Effective program (13 instructions):
  V2 = Tanh(V1)
  M2 = MatSub(M2, M1)
  M1 = MatAdd(M2, M0)
  M2 = Outer(V2, V0)
  s3 = 1.4354
  M1 = MatAdd(M1, M2)
  M1 = MatAdd(M0, M1)
  M0 = Outer(V1, V0)
  M3 = Transpose(M2)
  M3 = MatMul(M1, M3)
  M2 = MatMul(M3, M0)
  M0 = MatSub(M1, M2)
  M2 = MatScale(s3, M2)

structure: unclassified  [a=1.017 b=0.047 c=-0.966 g=0.002, erase c/a=0.950, R²=0.4730, 1408 steps]

train acc 0.686 ±0.013
test regime collision3: acc 0.693  margin 0.094  ±0.006
test d16 T12 ow0.3: acc 0.937  margin 0.286  ±0.004
test d16 T12 ow0.0: acc 0.910  margin 0.251  ±0.004
test d16 T12 ow0.6: acc 0.961  margin 0.291  ±0.004
test d32 T24 ow0.3: acc 0.987  margin 0.366  ±0.002
test d8 T6 ow0.3: acc 0.848  margin 0.145  ±0.007
test d16 T64 K8 ow0.3: acc 0.853  margin 0.181  ±0.008
test d16 T128 K8 ow0.3: acc 0.864  margin 0.178  ±0.011
```

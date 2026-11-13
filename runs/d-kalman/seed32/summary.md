# Search seed 32

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 701047  time: 2616s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4596 candidates
* unclassified: 9844 candidates
* linear, not error-correcting: 10996 candidates
* linear attention: 33780 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 33780 candidates
- delta rule (beta=1) (acc 0.578): 546804 candidates
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 519156 candidates

## Best rule

```
S' = ((tanh(v))⊗(tanh(k)) + 0.999·0.999·(S - (S)(P2)))
P1' = (k)⊗(tanh(0.999·(S - (S)(P2))·tanh(k)))
P2' = (tanh(tanh(k)))⊗((k)⊗(tanh(0.999·(S - (S)(P2))·tanh(k)))·norm(0.999·(S - (S)(P2))·tanh(k)))

Effective program (16 instructions):
  M3 = MatMul(M0, M2)
  M0 = MatSub(M0, M3)
  s1 = 0.9988
  M2 = MatScale(s1, M0)
  V2 = Tanh(V0)
  V3 = Tanh(V1)
  M3 = Outer(V3, V2)
  M1 = MatScale(s1, M2)
  M0 = MatAdd(M3, M1)
  V1 = MatVec(M2, V2)
  V5 = Tanh(V1)
  M1 = Outer(V0, V5)
  V5 = Normalize(V1)
  V1 = MatVec(M1, V5)
  V5 = Tanh(V2)
  M2 = Outer(V5, V1)

structure: unclassified  [a=0.816 b=0.898 c=-0.049 g=0.000, erase c/a=0.060, R²=0.8424, 1408 steps]

train acc 0.600 ±0.014
test regime collision3: acc 0.603  margin 0.011  ±0.006
test d16 T12 ow0.3: acc 0.856  margin 0.210  ±0.005
test d16 T12 ow0.0: acc 0.909  margin 0.225  ±0.004
test d16 T12 ow0.6: acc 0.836  margin 0.195  ±0.007
test d32 T24 ow0.3: acc 0.910  margin 0.302  ±0.004
test d8 T6 ow0.3: acc 0.706  margin 0.063  ±0.009
test d16 T64 K8 ow0.3: acc 0.758  margin 0.113  ±0.009
test d16 T128 K8 ow0.3: acc 0.760  margin 0.111  ±0.013
```

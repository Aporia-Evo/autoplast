# Search seed 14

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500204  real evaluations (after cache): 1165076  time: 4707s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1396 candidates
* decayed linear attention: 1780 candidates
* linear attention: 4852 candidates
* gated delta rule: 1102020 candidates
* delta rule: 1105788 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 4852 candidates
- delta rule (beta=1) (acc 0.578): 1104524 candidates
- delta rule (beta=0.5) (acc 0.617): 1120132 candidates
- gated delta (alpha=0.9) (acc 0.519): 50980 candidates

## Best rule

```
S' = ((1/(1.958)·P2 + ((v)⊗((((tanh(tanh(tanh(k))) + tanh(k)) + (tanh(tanh(tanh(k))) + tanh(k))) + ((tanh(tanh(tanh(k))) + tanh(k)) + (tanh(tanh(tanh(k))) + tanh(k))))) + S)) - (1/(1.958) + 1/(1.958))·((1/(1.958)·P2 + ((v)⊗((((tanh(tanh(tanh(k))) + tanh(k)) + (tanh(tanh(tanh(k))) + tanh(k))) + ((tanh(tanh(tanh(k))) + tanh(k)) + (tanh(tanh(tanh(k))) + tanh(k))))) + S))·tanh(k))⊗(tanh(k)))
P1' = (1/(1.958)·P2 + ((v)⊗((((tanh(tanh(tanh(k))) + tanh(k)) + (tanh(tanh(tanh(k))) + tanh(k))) + ((tanh(tanh(tanh(k))) + tanh(k)) + (tanh(tanh(tanh(k))) + tanh(k))))) + S))
P2' = (1/(1.958) + 1/(1.958))·((1/(1.958)·P2 + ((v)⊗((((tanh(tanh(tanh(k))) + tanh(k)) + (tanh(tanh(tanh(k))) + tanh(k))) + ((tanh(tanh(tanh(k))) + tanh(k)) + (tanh(tanh(tanh(k))) + tanh(k))))) + S))·tanh(k))⊗(tanh(k))

Effective program (17 instructions):
  V4 = Tanh(V0)
  V0 = Tanh(V4)
  V3 = Tanh(V0)
  V2 = VecAdd(V3, V4)
  V0 = VecAdd(V2, V2)
  V5 = VecAdd(V0, V0)
  M1 = Outer(V1, V5)
  M1 = MatAdd(M1, M0)
  s2 = 1.9582
  s3 = Recip(s2)
  M3 = MatScale(s3, M2)
  M1 = MatAdd(M3, M1)
  V0 = MatVec(M1, V4)
  s1 = SAdd(s3, s3)
  M2 = Outer(V0, V4)
  M2 = MatScale(s1, M2)
  M0 = MatSub(M1, M2)

structure: unclassified  [a=1.026 b=0.620 c=-0.934 g=0.003, erase c/a=0.911, R²=0.4891, 1408 steps]

train acc 0.686 ±0.013
test regime collision3: acc 0.692  margin 0.087  ±0.006
test d16 T12 ow0.3: acc 0.937  margin 0.271  ±0.004
test d16 T12 ow0.0: acc 0.919  margin 0.248  ±0.003
test d16 T12 ow0.6: acc 0.956  margin 0.263  ±0.004
test d32 T24 ow0.3: acc 0.987  margin 0.352  ±0.002
test d8 T6 ow0.3: acc 0.823  margin 0.129  ±0.008
test d16 T64 K8 ow0.3: acc 0.820  margin 0.141  ±0.008
test d16 T128 K8 ow0.3: acc 0.807  margin 0.133  ±0.012
```

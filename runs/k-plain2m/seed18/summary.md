# Search seed 18

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 2100084  real evaluations (after cache): 882148  time: 1619s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2676 candidates
* unclassified: 4980 candidates
* linear attention: 6772 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6772 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 949748 candidates

## Best rule

```
S' = (0.897·S + (tanh(v))⊗(norm((k + P2·tanh(k)))))
P1' = (tanh(v))⊗(norm((k + P2·tanh(k))))
P2' = (norm(tanh(P2·k)))⊗(tanh((0 - norm(tanh(P2·k)))))

Effective program (15 instructions):
  V4 = Tanh(V0)
  V2 = MatVec(M2, V4)
  V4 = VecAdd(V0, V2)
  V0 = MatVec(M2, V0)
  V0 = Tanh(V0)
  V2 = Normalize(V0)
  V0 = Normalize(V4)
  V1 = Tanh(V1)
  M1 = Outer(V1, V0)
  s3 = 0.8972
  V4 = VecSub(V3, V2)
  M3 = MatScale(s3, M0)
  M0 = MatAdd(M3, M1)
  V0 = Tanh(V4)
  M2 = Outer(V2, V0)

structure: unclassified  [a=0.898 b=0.878 c=-0.001 g=0.006, erase c/a=0.001, R²=0.8530, 1408 steps]

train acc 0.568 ±0.014
test regime collision3: acc 0.564  margin -0.004  ±0.006
test d16 T12 ow0.3: acc 0.790  margin 0.161  ±0.006
test d16 T12 ow0.0: acc 0.805  margin 0.175  ±0.005
test d16 T12 ow0.6: acc 0.722  margin 0.110  ±0.009
test d32 T24 ow0.3: acc 0.730  margin 0.163  ±0.007
test d8 T6 ow0.3: acc 0.686  margin 0.057  ±0.010
test d16 T64 K8 ow0.3: acc 0.593  margin 0.003  ±0.011
test d16 T128 K8 ow0.3: acc 0.561  margin -0.020  ±0.016
```

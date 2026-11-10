# Search seed 5

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 310548  time: 512s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 17140 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((tanh(v))⊗(tanh(tanh(tanh(k)))) + <tanh(v), ((tanh(tanh(tanh(k))) - k) + tanh(v))>·S)
o = S·tanh(tanh(q))

Effective program (10 instructions):
  V4 = Tanh(V1)
  V2 = Tanh(V0)
  V5 = Tanh(V2)
  V1 = Tanh(V5)
  V3 = VecSub(V1, V0)
  M1 = Outer(V4, V1)
  V5 = VecAdd(V3, V4)
  s1 = Dot(V4, V5)
  M0 = MatScale(s1, M0)
  M0 = MatAdd(M1, M0)

train acc 0.512
test regime collision3: acc 0.518  margin -0.033
test d16 T12 ow0.3: acc 0.759  margin 0.140
test d16 T12 ow0.0: acc 0.754  margin 0.134
test d16 T12 ow0.6: acc 0.706  margin 0.099
test d32 T24 ow0.3: acc 0.845  margin 0.216
test d8 T6 ow0.3: acc 0.638  margin 0.024
test d16 T64 K8 ow0.3: acc 0.569  margin -0.009
test d16 T128 K8 ow0.3: acc 0.546  margin -0.027
```

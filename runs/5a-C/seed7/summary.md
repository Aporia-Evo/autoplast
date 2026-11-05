# Search seed 7

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 410959  time: 569s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 36596 candidates
- delta rule (beta=1) (acc 0.578): 60660 candidates
- delta rule (beta=0.5) (acc 0.617): 67060 candidates
- gated delta (alpha=0.9) (acc 0.519): 60660 candidates

## Best rule

```
S' = (S + (σ(0.128)·tanh((norm(tanh(v)) - S·k)))⊗(k))
o = tanh(tanh(1.265·S·q))

Effective program (10 instructions):
  V5 = Tanh(V1)
  V1 = Normalize(V5)
  V4 = MatVec(M0, V0)
  s1 = 0.1279
  s3 = Sigmoid(s1)
  V1 = VecSub(V1, V4)
  V2 = Tanh(V1)
  V5 = VecScale(s3, V2)
  M3 = Outer(V5, V0)
  M0 = MatAdd(M0, M3)

train acc 0.622
test regime collision3: acc 0.638  margin 0.048
test d16 T12 ow0.3: acc 0.920  margin 0.261
test d16 T12 ow0.0: acc 0.901  margin 0.236
test d16 T12 ow0.6: acc 0.939  margin 0.261
test d32 T24 ow0.3: acc 0.986  margin 0.352
test d8 T6 ow0.3: acc 0.787  margin 0.109
test d16 T64 K8 ow0.3: acc 0.832  margin 0.155
test d16 T128 K8 ow0.3: acc 0.815  margin 0.149
```

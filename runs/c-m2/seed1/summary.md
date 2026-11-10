# Search seed 1

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 672681  time: 1621s  pop: 500  tournament: 10

commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3060 candidates
* unclassified: 21620 candidates
* linear attention: 22900 candidates
* gated delta rule: 79348 candidates
* delta rule: 79988 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 22900 candidates
- delta rule (beta=1) (acc 0.578): 79988 candidates
- delta rule (beta=0.5) (acc 0.617): 80884 candidates
- gated delta (alpha=0.9) (acc 0.519): 79348 candidates

## Best rule

```
S' = ((tanh((σ(((-0.941 + |S·k|) + |S·k|)) + (-0.941 + |S·k|)·((-0.941 + |S·k|) + |S·k|))·(v - S·tanh(k))))⊗(norm(tanh(k))) - (0 - S))

Effective program (17 instructions):
  M2 = MatSub(M3, M0)
  V4 = Tanh(V0)
  V3 = Normalize(V4)
  V5 = MatVec(M0, V0)
  s2 = -0.9414
  s3 = Norm(V5)
  s0 = SAdd(s2, s3)
  V0 = MatVec(M0, V4)
  s3 = SAdd(s0, s3)
  s1 = Sigmoid(s3)
  V1 = VecSub(V1, V0)
  s0 = SMul(s0, s3)
  s3 = SAdd(s1, s0)
  V0 = VecScale(s3, V1)
  V0 = Tanh(V0)
  M0 = Outer(V0, V3)
  M0 = MatSub(M0, M2)

structure: unclassified  [a=1.000 b=0.547 c=-0.502 g=-0.021, erase c/a=0.502, R²=0.9366, 1408 steps]

train acc 0.651 ±0.014
test regime collision3: acc 0.661  margin 0.062  ±0.006
test d16 T12 ow0.3: acc 0.923  margin 0.262  ±0.004
test d16 T12 ow0.0: acc 0.922  margin 0.249  ±0.003
test d16 T12 ow0.6: acc 0.917  margin 0.243  ±0.005
test d32 T24 ow0.3: acc 0.977  margin 0.346  ±0.002
test d8 T6 ow0.3: acc 0.775  margin 0.109  ±0.009
test d16 T64 K8 ow0.3: acc 0.816  margin 0.136  ±0.009
test d16 T128 K8 ow0.3: acc 0.799  margin 0.131  ±0.013
```

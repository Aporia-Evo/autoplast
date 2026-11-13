# Search seed 18

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 561368  time: 994s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

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
S' = ((v)⊗(norm(tanh((k + P2·k)))) + 0.881·S)
P1' = (v)⊗(norm(tanh((k + P2·k))))
P2' = (<(tanh((k + P2·k)) - P2·k), (tanh((k + P2·k)) - P2·k)>·|norm(tanh((k + P2·k)))|·(P2·k - tanh(tanh((k + P2·k)))))⊗((tanh((k + P2·k)) - P2·k))

Effective program (16 instructions):
  V2 = MatVec(M2, V0)
  V4 = VecAdd(V0, V2)
  V3 = Tanh(V4)
  V5 = Tanh(V3)
  V0 = Normalize(V3)
  M1 = Outer(V1, V0)
  V1 = VecSub(V2, V5)
  s3 = 0.8805
  V4 = VecSub(V3, V2)
  M3 = MatScale(s3, M0)
  M0 = MatAdd(M1, M3)
  s0 = Norm(V0)
  s3 = Dot(V4, V4)
  V2 = VecScale(s0, V1)
  V1 = VecScale(s3, V2)
  M2 = Outer(V1, V4)

structure: unclassified  [a=0.880 b=0.960 c=0.001 g=-0.008, erase c/a=-0.001, R²=0.9210, 1408 steps]

train acc 0.536 ±0.014
test regime collision3: acc 0.528  margin -0.037  ±0.006
test d16 T12 ow0.3: acc 0.745  margin 0.138  ±0.007
test d16 T12 ow0.0: acc 0.729  margin 0.124  ±0.006
test d16 T12 ow0.6: acc 0.734  margin 0.120  ±0.008
test d32 T24 ow0.3: acc 0.647  margin 0.109  ±0.007
test d8 T6 ow0.3: acc 0.669  margin 0.048  ±0.010
test d16 T64 K8 ow0.3: acc 0.586  margin -0.004  ±0.011
test d16 T128 K8 ow0.3: acc 0.566  margin -0.021  ±0.015
```

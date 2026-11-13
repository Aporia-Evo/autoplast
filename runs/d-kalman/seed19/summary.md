# Search seed 19

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 754527  time: 1176s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 1140 candidates
* linear attention: 14452 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 14452 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 315764 candidates

## Best rule

```
S' = (<tanh(norm((((v ⊙ v) ⊙ 1.806·k) + k))), tanh(norm((((v ⊙ v) ⊙ 1.806·k) + k)))>·S + (<tanh(norm((((v ⊙ v) ⊙ 1.806·k) + k))), tanh(norm((((v ⊙ v) ⊙ 1.806·k) + k)))> + -0.170)·(v)⊗(k))
P1' = <tanh(norm((((v ⊙ v) ⊙ 1.806·k) + k))), tanh(norm((((v ⊙ v) ⊙ 1.806·k) + k)))>·S

Effective program (14 instructions):
  s3 = 1.8059
  s2 = -0.1696
  V4 = Hadamard(V1, V1)
  V2 = VecScale(s3, V0)
  V2 = Hadamard(V4, V2)
  M3 = Outer(V1, V0)
  V0 = VecAdd(V2, V0)
  V1 = Normalize(V0)
  V1 = Tanh(V1)
  s1 = Dot(V1, V1)
  M1 = MatScale(s1, M0)
  s1 = SAdd(s1, s2)
  M0 = MatScale(s1, M3)
  M0 = MatAdd(M1, M0)

structure: decayed linear attention  [a=0.891 b=0.721 c=0.001 g=0.007, erase c/a=-0.001, R²=0.9949, 1408 steps]

train acc 0.515 ±0.014
test regime collision3: acc 0.518  margin -0.030  ±0.006
test d16 T12 ow0.3: acc 0.763  margin 0.141  ±0.006
test d16 T12 ow0.0: acc 0.759  margin 0.138  ±0.005
test d16 T12 ow0.6: acc 0.714  margin 0.105  ±0.009
test d32 T24 ow0.3: acc 0.848  margin 0.217  ±0.005
test d8 T6 ow0.3: acc 0.644  margin 0.025  ±0.010
test d16 T64 K8 ow0.3: acc 0.573  margin -0.009  ±0.011
test d16 T128 K8 ow0.3: acc 0.558  margin -0.025  ±0.016
```

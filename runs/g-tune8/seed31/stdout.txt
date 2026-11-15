# Search seed 31

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500164  real evaluations (after cache): 1021375  time: 1833s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2164 candidates
* unclassified: 5884 candidates
* linear attention: 9060 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6908 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 553780 candidates

## Best rule

```
S' = ((v)⊗(50.469·k) - σ((-1.911 + |tanh((v + 50.469·k))|))·((v)⊗(50.469·k) - P2))
P1' = σ((-1.911 + |tanh((v + 50.469·k))|))·((v)⊗(50.469·k) - P2)
P2' = (((v)⊗(50.469·k) - σ((-1.911 + |tanh((v + 50.469·k))|))·((v)⊗(50.469·k) - P2)) - 0)

Effective program (13 instructions):
  s1 = 50.4691
  V0 = VecScale(s1, V0)
  M0 = Outer(V1, V0)
  V3 = VecAdd(V1, V0)
  V5 = Tanh(V3)
  s1 = -1.9111
  M2 = MatSub(M0, M2)
  s3 = Norm(V5)
  s2 = SAdd(s1, s3)
  s0 = Sigmoid(s2)
  M1 = MatScale(s0, M2)
  M0 = MatSub(M0, M1)
  M2 = MatSub(M0, M3)

structure: unclassified  [a=0.873 b=6.418 c=-0.001 g=-0.005, erase c/a=0.001, R²=0.9755, 1408 steps]

train acc 0.515 ±0.014
test regime collision3: acc 0.517  margin -0.043  ±0.006
test d16 T12 ow0.3: acc 0.728  margin 0.122  ±0.007
test d16 T12 ow0.0: acc 0.712  margin 0.107  ±0.006
test d16 T12 ow0.6: acc 0.719  margin 0.110  ±0.009
test d32 T24 ow0.3: acc 0.858  margin 0.195  ±0.005
test d8 T6 ow0.3: acc 0.595  margin -0.022  ±0.010
test d16 T64 K8 ow0.3: acc 0.582  margin -0.008  ±0.011
test d16 T128 K8 ow0.3: acc 0.554  margin -0.029  ±0.016
```

# Search seed 9

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 910112  time: 2060s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 356810 attempts, 255103 blocks inserted, 263709 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 3444 candidates
* linear attention: 3700 candidates
* delta rule: 101620 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3700 candidates
- delta rule (beta=1) (acc 0.578): 99828 candidates
- delta rule (beta=0.5) (acc 0.617): 101876 candidates
- gated delta (alpha=0.9) (acc 0.519): 40436 candidates

## Best rule

```
S' = (((S + 0.176·P2) + ((0.176 + 0.012) + (0.176 + 0.012)·<norm((tanh(v) + -0.458·((S + 0.176·P2)·k + 0))), ((S + 0.176·P2)·k + 0)>)·(S + 0.176·P2)) + ((tanh(v) + -0.458·((S + 0.176·P2)·k + 0)))⊗((k + -0.183·tanh(v))))
P2' = ((tanh(v) + -0.458·((S + 0.176·P2)·k + 0)))⊗((k + -0.183·tanh(v)))

Effective program (22 instructions):
  s3 = 0.1762
  M2 = MatScale(s3, M2)
  M0 = MatAdd(M0, M2)
  V5 = MatVec(M0, V0)
  V2 = VecAdd(V5, V2)
  s2 = -0.4585
  V5 = VecScale(s2, V2)
  V3 = Tanh(V1)
  s2 = 0.0117
  s3 = SAdd(s3, s2)
  V1 = VecAdd(V3, V5)
  s2 = -0.1832
  V3 = VecScale(s2, V3)
  V0 = VecAdd(V0, V3)
  V5 = Normalize(V1)
  s1 = Dot(V5, V2)
  s1 = SMul(s3, s1)
  s3 = SAdd(s3, s1)
  M2 = MatScale(s3, M0)
  M0 = MatAdd(M0, M2)
  M2 = Outer(V1, V0)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=1.029 b=0.967 c=-0.492 g=0.030, erase c/a=0.478, R²=0.8375, 1408 steps]

train acc 0.681 ±0.013
test regime collision3: acc 0.678  margin 0.064  ±0.006
test d16 T12 ow0.3: acc 0.958  margin 0.260  ±0.003
test d16 T12 ow0.0: acc 0.956  margin 0.251  ±0.003
test d16 T12 ow0.6: acc 0.941  margin 0.236  ±0.004
test d32 T24 ow0.3: acc 0.988  margin 0.329  ±0.002
test d8 T6 ow0.3: acc 0.794  margin 0.114  ±0.008
test d16 T64 K8 ow0.3: acc 0.742  margin 0.100  ±0.010
test d16 T128 K8 ow0.3: acc 0.737  margin 0.083  ±0.014
```

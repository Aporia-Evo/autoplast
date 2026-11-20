# Search seed 13

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 872588  time: 3304s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 356592 attempts, 292274 blocks inserted, 307678 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 1000052 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1780 candidates
* linear attention: 2420 candidates
* decayed linear attention: 3828 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 2420 candidates
- delta rule (beta=1) (acc 0.578): 55796 candidates
- delta rule (beta=0.5) (acc 0.617): 71924 candidates
- gated delta (alpha=0.9) (acc 0.519): 37876 candidates

## Best rule

```
S' = ((((v + |(S + P1)·k|·-0.252·(S + P1)·k))⊗(k) - ((|(S + P1)·k|·-0.252·P1 - (S + 0.035·(k)⊗(v))) + -0.011·(S + 0.035·(k)⊗(v)))) + -0.009·((|(S + P1)·k|·-0.252·P1 - (S + 0.035·(k)⊗(v))) + -0.011·(S + 0.035·(k)⊗(v))))
P1' = ((v + |(S + P1)·k|·-0.252·(S + P1)·k))⊗(k)
P2' = -0.009·((|(S + P1)·k|·-0.252·P1 - (S + 0.035·(k)⊗(v))) + -0.011·(S + 0.035·(k)⊗(v)))

Effective program (22 instructions):
  M3 = MatAdd(M0, M1)
  V2 = MatVec(M3, V0)
  s1 = Norm(V2)
  s3 = -0.2521
  M3 = Outer(V0, V1)
  s2 = 0.0350
  M3 = MatScale(s2, M3)
  M0 = MatAdd(M0, M3)
  M2 = MatScale(s3, M1)
  V2 = VecScale(s3, V2)
  V2 = VecScale(s1, V2)
  V1 = VecAdd(V1, V2)
  M1 = Outer(V1, V0)
  M2 = MatScale(s1, M2)
  M2 = MatSub(M2, M0)
  s1 = -0.0112
  M0 = MatScale(s1, M0)
  M2 = MatAdd(M2, M0)
  M0 = MatSub(M1, M2)
  s2 = -0.0092
  M2 = MatScale(s2, M2)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=1.027 b=1.001 c=-0.461 g=-0.005, erase c/a=0.449, R²=0.8480, 1408 steps]

train acc 0.661 ±0.014
test regime collision3: acc 0.663  margin 0.058  ±0.006
test d16 T12 ow0.3: acc 0.939  margin 0.248  ±0.004
test d16 T12 ow0.0: acc 0.938  margin 0.233  ±0.003
test d16 T12 ow0.6: acc 0.935  margin 0.246  ±0.005
test d32 T24 ow0.3: acc 0.990  margin 0.335  ±0.002
test d8 T6 ow0.3: acc 0.794  margin 0.110  ±0.008
test d16 T64 K8 ow0.3: acc 0.799  margin 0.159  ±0.009
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```

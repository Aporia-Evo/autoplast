# Search seed 5

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 879940  time: 1872s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357932 attempts, 284939 blocks inserted, 292612 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 200052 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 2292 candidates
* delta rule: 27764 candidates
* linear, not error-correcting: 29172 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6516 candidates
- delta rule (beta=1) (acc 0.578): 27764 candidates
- delta rule (beta=0.5) (acc 0.617): 32244 candidates
- gated delta (alpha=0.9) (acc 0.519): 12916 candidates

## Best rule

```
S' = ((S + -0.166·(P1 + P1)) + (0.532·(P2 + 0.038·((v - (P2 + S)·k))⊗((P2 + S)·k)) + ((((v - (P2 + S)·k) + 0.532·norm((P2 + S)·k)) + 0.532·norm((P2 + S)·k)))⊗(k)))
P1' = ((((v - (P2 + S)·k) + 0.532·norm((P2 + S)·k)) + 0.532·norm((P2 + S)·k)))⊗(k)
P2' = (0.532·(P2 + 0.038·((v - (P2 + S)·k))⊗((P2 + S)·k)) + ((((v - (P2 + S)·k) + 0.532·norm((P2 + S)·k)) + 0.532·norm((P2 + S)·k)))⊗(k))

Effective program (20 instructions):
  M3 = MatAdd(M2, M0)
  V5 = MatVec(M3, V0)
  V2 = VecSub(V1, V5)
  M1 = MatAdd(M1, M1)
  s3 = -0.1656
  M3 = Outer(V2, V5)
  s0 = 0.0379
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)
  M1 = MatScale(s3, M1)
  M0 = MatAdd(M0, M1)
  V3 = Normalize(V5)
  s1 = 0.5315
  V3 = VecScale(s1, V3)
  V2 = VecAdd(V2, V3)
  V2 = VecAdd(V2, V3)
  M2 = MatScale(s1, M2)
  M1 = Outer(V2, V0)
  M2 = MatAdd(M2, M1)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=1.028 b=1.004 c=-0.454 g=-0.003, erase c/a=0.442, R²=0.8326, 1408 steps]

train acc 0.660 ±0.014
test regime collision3: acc 0.667  margin 0.049  ±0.006
test d16 T12 ow0.3: acc 0.929  margin 0.232  ±0.004
test d16 T12 ow0.0: acc 0.888  margin 0.197  ±0.004
test d16 T12 ow0.6: acc 0.930  margin 0.235  ±0.005
test d32 T24 ow0.3: acc 0.986  margin 0.337  ±0.002
test d8 T6 ow0.3: acc 0.700  margin 0.070  ±0.010
test d16 T64 K8 ow0.3: acc 0.843  margin 0.185  ±0.008
test d16 T128 K8 ow0.3: acc 0.852  margin 0.178  ±0.011
```

# Search seed 22

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 960275  time: 4667s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357142 attempts, 241117 blocks inserted, 259683 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1140 candidates
* linear attention: 2292 candidates
* decayed linear attention: 4724 candidates
* delta rule: 43252 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 2292 candidates
- delta rule (beta=1) (acc 0.578): 40820 candidates
- delta rule (beta=0.5) (acc 0.617): 43252 candidates
- gated delta (alpha=0.9) (acc 0.519): 36724 candidates

## Best rule

```
S' = ((((S + ((P2 + -0.005·(0 + P1)))(S)) + (P2 + -0.005·(0 + P1))) + -0.212·(((((0 - v) + ((P2 + -0.005·(0 + P1)))(S)·k) + S·k))⊗(k))(((S + ((P2 + -0.005·(0 + P1)))(S)) + (P2 + -0.005·(0 + P1))))) + (-0.484·((((0 - v) + ((P2 + -0.005·(0 + P1)))(S)·k) + S·k))⊗(k) + 0.254·(((S + ((P2 + -0.005·(0 + P1)))(S)) + (P2 + -0.005·(0 + P1))))(P1)))
P1' = (-0.484·((((0 - v) + ((P2 + -0.005·(0 + P1)))(S)·k) + S·k))⊗(k) + 0.254·(((S + ((P2 + -0.005·(0 + P1)))(S)) + (P2 + -0.005·(0 + P1))))(P1))
P2' = -0.212·(((((0 - v) + ((P2 + -0.005·(0 + P1)))(S)·k) + S·k))⊗(k))(((S + ((P2 + -0.005·(0 + P1)))(S)) + (P2 + -0.005·(0 + P1))))

Effective program (24 instructions):
  V4 = VecSub(V3, V1)
  M3 = MatAdd(M3, M1)
  s0 = -0.0049
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)
  V3 = MatVec(M0, V0)
  M3 = MatMul(M2, M0)
  V1 = MatVec(M3, V0)
  V4 = VecAdd(V4, V1)
  M0 = MatAdd(M0, M3)
  V4 = VecAdd(V4, V3)
  M0 = MatAdd(M0, M2)
  M3 = MatMul(M0, M1)
  s3 = -0.4836
  M1 = Outer(V4, V0)
  M2 = MatMul(M1, M0)
  M1 = MatScale(s3, M1)
  s3 = -0.2116
  s1 = 0.2541
  M3 = MatScale(s1, M3)
  M1 = MatAdd(M1, M3)
  M2 = MatScale(s3, M2)
  M0 = MatAdd(M0, M2)
  M0 = MatAdd(M0, M1)

structure: unclassified  [a=1.002 b=0.543 c=-0.583 g=0.016, erase c/a=0.582, R²=0.3451, 1408 steps]

train acc 0.676 ±0.013
test regime collision3: acc 0.674  margin 0.065  ±0.006
test d16 T12 ow0.3: acc 0.852  margin 0.205  ±0.005
test d16 T12 ow0.0: acc 0.803  margin 0.153  ±0.005
test d16 T12 ow0.6: acc 0.853  margin 0.201  ±0.007
test d32 T24 ow0.3: acc 0.942  margin 0.315  ±0.004
test d8 T6 ow0.3: acc 0.657  margin 0.027  ±0.010
test d16 T64 K8 ow0.3: acc 0.807  margin 0.144  ±0.009
test d16 T128 K8 ow0.3: acc 0.824  margin 0.150  ±0.012
```

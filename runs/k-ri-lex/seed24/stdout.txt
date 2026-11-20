# Search seed 24

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 841086  time: 2439s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 356023 attempts, 297824 blocks inserted, 313935 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 3700 candidates
* linear attention: 4084 candidates
* delta rule: 136564 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 4084 candidates
- delta rule (beta=1) (acc 0.578): 136564 candidates
- delta rule (beta=0.5) (acc 0.617): 137332 candidates
- gated delta (alpha=0.9) (acc 0.519): 46964 candidates

## Best rule

```
S' = (S + ((((v + v) + -0.367·((S + P2)·k - v)))⊗(k) + (0.172·P2 + 0.172·P2)))
P2' = ((((((v + v) + -0.367·((S + P2)·k - v)))⊗(k) + (0.172·P2 + 0.172·P2)) + (0.172·P2 + 0.172·P2)) + 0.430·(0.172·P2 + 0.172·P2))

Effective program (17 instructions):
  M3 = MatAdd(M0, M2)
  V5 = MatVec(M3, V0)
  V5 = VecSub(V5, V1)
  s1 = -0.3673
  s0 = 0.1718
  V5 = VecScale(s1, V5)
  V3 = VecAdd(V1, V1)
  V1 = VecAdd(V3, V5)
  M2 = MatScale(s0, M2)
  M3 = MatAdd(M2, M2)
  M2 = Outer(V1, V0)
  M2 = MatAdd(M2, M3)
  M0 = MatAdd(M0, M2)
  M2 = MatAdd(M2, M3)
  s1 = 0.4297
  M3 = MatScale(s1, M3)
  M2 = MatAdd(M2, M3)

structure: unclassified  [a=1.034 b=2.367 c=-0.405 g=-0.000, erase c/a=0.392, R²=0.8474, 1408 steps]

train acc 0.672 ±0.013
test regime collision3: acc 0.666  margin 0.076  ±0.006
test d16 T12 ow0.3: acc 0.938  margin 0.274  ±0.004
test d16 T12 ow0.0: acc 0.923  margin 0.253  ±0.003
test d16 T12 ow0.6: acc 0.905  margin 0.247  ±0.006
test d32 T24 ow0.3: acc 0.967  margin 0.364  ±0.003
test d8 T6 ow0.3: acc 0.812  margin 0.122  ±0.008
test d16 T64 K8 ow0.3: acc 0.803  margin 0.167  ±0.009
test d16 T128 K8 ow0.3: acc 0.805  margin 0.165  ±0.012
```

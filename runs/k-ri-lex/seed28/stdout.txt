# Search seed 28

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 950834  time: 2895s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357551 attempts, 264299 blocks inserted, 287078 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1908 candidates
* decayed linear attention: 3060 candidates
* linear, not error-correcting: 4980 candidates
* gated delta rule: 7284 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5364 candidates
- delta rule (beta=1) (acc 0.578): 8308 candidates
- delta rule (beta=0.5) (acc 0.617): 23668 candidates
- gated delta (alpha=0.9) (acc 0.519): 6772 candidates

## Best rule

```
S' = (((((v + 0.013·k) + 0.077·(P1 - P2)·S·k) - S·k))⊗(k) + 0.543·(((S + (P1 - P2)) - ((((v + 0.013·k) + 0.077·(P1 - P2)·S·k) - S·k))⊗(k)) + -0.280·((((P2 - (P1 - P2)) + P2))ᵀ - P2)))
P1' = (S + (P1 - P2))
P2' = 0.543·(((S + (P1 - P2)) - ((((v + 0.013·k) + 0.077·(P1 - P2)·S·k) - S·k))⊗(k)) + -0.280·((((P2 - (P1 - P2)) + P2))ᵀ - P2))

Effective program (23 instructions):
  V5 = MatVec(M0, V0)
  M3 = MatSub(M1, M2)
  M1 = MatAdd(M0, M3)
  s2 = 0.0128
  V4 = VecScale(s2, V0)
  V1 = VecAdd(V1, V4)
  V2 = MatVec(M3, V5)
  s0 = 0.0769
  V2 = VecScale(s0, V2)
  V1 = VecAdd(V1, V2)
  M0 = MatSub(M2, M3)
  M3 = MatAdd(M0, M2)
  M0 = Transpose(M3)
  M3 = MatSub(M0, M2)
  s1 = -0.2797
  M3 = MatScale(s1, M3)
  V5 = VecSub(V1, V5)
  M0 = Outer(V5, V0)
  M2 = MatSub(M1, M0)
  M2 = MatAdd(M2, M3)
  s3 = 0.5434
  M2 = MatScale(s3, M2)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=0.985 b=0.456 c=-0.418 g=0.006, erase c/a=0.424, R²=0.5256, 1408 steps]

train acc 0.676 ±0.013
test regime collision3: acc 0.664  margin 0.057  ±0.006
test d16 T12 ow0.3: acc 0.930  margin 0.245  ±0.004
test d16 T12 ow0.0: acc 0.928  margin 0.237  ±0.003
test d16 T12 ow0.6: acc 0.886  margin 0.205  ±0.006
test d32 T24 ow0.3: acc 0.980  margin 0.343  ±0.002
test d8 T6 ow0.3: acc 0.739  margin 0.085  ±0.009
test d16 T64 K8 ow0.3: acc 0.792  margin 0.128  ±0.009
test d16 T128 K8 ow0.3: acc 0.785  margin 0.123  ±0.013
```

# Search seed 23

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 949497  time: 2566s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 356686 attempts, 271587 blocks inserted, 288668 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 300020 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1780 candidates
* decayed linear attention: 2932 candidates
* linear, not error-correcting: 3444 candidates
* gated delta rule: 16884 candidates
* delta rule: 18676 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5364 candidates
- delta rule (beta=1) (acc 0.578): 18036 candidates
- delta rule (beta=0.5) (acc 0.617): 20596 candidates
- gated delta (alpha=0.9) (acc 0.519): 16884 candidates

## Best rule

```
S' = (((v + -0.227·(v + (P2 + (S - P1))·k)))⊗((k + k)) + (P2 + (S - P1)))
P1' = (0.646·(((v + -0.227·(v + (P2 + (S - P1))·k)))⊗((k + k)) - ((P1 + 0.084·((S - P1))(P2)) + -0.003·P2)))ᵀ
P2' = (((v + -0.227·(v + (P2 + (S - P1))·k)))⊗((k + k)))ᵀ

Effective program (22 instructions):
  M0 = MatSub(M0, M1)
  M3 = MatAdd(M2, M0)
  V3 = MatVec(M3, V0)
  V3 = VecAdd(V1, V3)
  s3 = -0.2275
  V3 = VecScale(s3, V3)
  V1 = VecAdd(V1, V3)
  M0 = MatMul(M0, M2)
  s3 = 0.0839
  M0 = MatScale(s3, M0)
  M1 = MatAdd(M1, M0)
  V3 = VecAdd(V0, V0)
  M0 = Outer(V1, V3)
  s1 = 0.6459
  s2 = -0.0028
  M2 = MatScale(s2, M2)
  M1 = MatAdd(M1, M2)
  M1 = MatSub(M0, M1)
  M1 = MatScale(s1, M1)
  M1 = Transpose(M1)
  M2 = Transpose(M0)
  M0 = MatAdd(M0, M3)

structure: unclassified  [a=1.010 b=1.548 c=-0.449 g=-0.000, erase c/a=0.445, R²=0.6768, 1408 steps]

train acc 0.674 ±0.013
test regime collision3: acc 0.674  margin 0.063  ±0.006
test d16 T12 ow0.3: acc 0.939  margin 0.266  ±0.004
test d16 T12 ow0.0: acc 0.919  margin 0.247  ±0.003
test d16 T12 ow0.6: acc 0.913  margin 0.237  ±0.005
test d32 T24 ow0.3: acc 0.981  margin 0.359  ±0.002
test d8 T6 ow0.3: acc 0.776  margin 0.104  ±0.009
test d16 T64 K8 ow0.3: acc 0.835  margin 0.166  ±0.008
test d16 T128 K8 ow0.3: acc 0.825  margin 0.161  ±0.012
```

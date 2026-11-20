# Search seed 1

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1067790  time: 2929s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 356412 attempts, 114683 blocks inserted, 122596 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 150004 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1140 candidates
* unclassified: 2292 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5620 candidates
- delta rule (beta=1) (acc 0.578): 111220 candidates
- delta rule (beta=0.5) (acc 0.617): 111732 candidates
- gated delta (alpha=0.9) (acc 0.519): 106484 candidates

## Best rule

```
S' = ((-0.147·((S - P1) + (S - P1))·k)⊗((k - 0)) + ((((S - P1) + (v)⊗(((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + ((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + v)))) + (-0.147·((S - P1) + (S - P1))·k)⊗((k - 0))) + (-0.147·((S - P1) + (S - P1))·k)⊗((k - 0))))
P1' = -0.767·(((S - P1) + (v)⊗(((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + ((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + v)))) + ((v)⊗(((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + ((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + v))) - (0 + S)))
P2' = ((v)⊗(((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + ((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + v))) - (0 + S))

Effective program (23 instructions):
  M1 = MatSub(M0, M1)
  M3 = MatAdd(M3, M0)
  M2 = MatAdd(M1, M1)
  V3 = MatVec(M2, V0)
  V2 = VecSub(V0, V5)
  V0 = VecAdd(V0, V0)
  V0 = VecAdd(V0, V0)
  s3 = -0.1468
  V0 = VecAdd(V2, V0)
  V4 = VecAdd(V0, V0)
  V5 = VecAdd(V4, V1)
  V0 = VecAdd(V4, V5)
  V3 = VecScale(s3, V3)
  M2 = Outer(V1, V0)
  M1 = MatAdd(M1, M2)
  M0 = Outer(V3, V2)
  M2 = MatSub(M2, M3)
  M3 = MatAdd(M1, M0)
  M1 = MatAdd(M1, M2)
  M3 = MatAdd(M3, M0)
  s0 = -0.7666
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M3)

structure: unclassified  [a=1.073 b=20.009 c=-0.939 g=-0.000, erase c/a=0.875, R²=0.8313, 1408 steps]

train acc 0.735 ±0.013
test regime collision3: acc 0.721  margin 0.117  ±0.006
test d16 T12 ow0.3: acc 0.957  margin 0.293  ±0.003
test d16 T12 ow0.0: acc 0.946  margin 0.276  ±0.003
test d16 T12 ow0.6: acc 0.947  margin 0.270  ±0.004
test d32 T24 ow0.3: acc 0.986  margin 0.379  ±0.002
test d8 T6 ow0.3: acc 0.860  margin 0.148  ±0.007
test d16 T64 K8 ow0.3: acc 0.869  margin 0.190  ±0.007
test d16 T128 K8 ow0.3: acc 0.878  margin 0.193  ±0.010
```

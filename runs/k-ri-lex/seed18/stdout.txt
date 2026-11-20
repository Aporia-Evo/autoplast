# Search seed 18

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1001164  time: 5020s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357109 attempts, 195671 blocks inserted, 211298 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 150004 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* linear attention: 1012 candidates
* unclassified: 3700 candidates
* decayed linear attention: 4084 candidates
* delta rule: 69748 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 1012 candidates
- delta rule (beta=1) (acc 0.578): 64372 candidates
- delta rule (beta=0.5) (acc 0.617): 66676 candidates
- gated delta (alpha=0.9) (acc 0.519): 37748 candidates

## Best rule

```
S' = ((-0.220·(S + P2))((((0 + k) + (0 + k)))⊗(((0 + k) + (0 + k)))) + ((S + P2) + (((v + v) + (v + v)))⊗((0 + k))))
P1' = (((v + 0.115·(((v + v) + (v + v)) + v)) + (v + v)))⊗(((0 + k) + (0 + k)))
P2' = (((P2 + -0.220·P2) + -0.006·((S + P2) + (((v + v) + (v + v)))⊗((0 + k)))) + (((v + 0.115·(((v + v) + (v + v)) + v)) + (v + v)))⊗(((0 + k) + (0 + k))))

Effective program (24 instructions):
  V4 = VecAdd(V2, V0)
  V5 = VecAdd(V1, V1)
  V0 = VecAdd(V5, V5)
  M1 = Outer(V0, V4)
  M3 = MatAdd(M0, M2)
  s1 = -0.2198
  M0 = MatScale(s1, M2)
  M2 = MatAdd(M2, M0)
  M0 = MatScale(s1, M3)
  V2 = VecAdd(V0, V1)
  s3 = 0.1149
  V2 = VecScale(s3, V2)
  V1 = VecAdd(V1, V2)
  V0 = VecAdd(V4, V4)
  V1 = VecAdd(V1, V5)
  M3 = MatAdd(M3, M1)
  M1 = Outer(V0, V0)
  M1 = MatMul(M0, M1)
  M0 = MatAdd(M1, M3)
  M1 = Outer(V1, V0)
  s3 = -0.0063
  M3 = MatScale(s3, M3)
  M2 = MatAdd(M2, M3)
  M2 = MatAdd(M2, M1)

structure: unclassified  [a=1.078 b=4.006 c=-0.941 g=-0.000, erase c/a=0.873, R²=0.8010, 1408 steps]

train acc 0.737 ±0.013
test regime collision3: acc 0.725  margin 0.116  ±0.006
test d16 T12 ow0.3: acc 0.950  margin 0.287  ±0.003
test d16 T12 ow0.0: acc 0.941  margin 0.270  ±0.003
test d16 T12 ow0.6: acc 0.940  margin 0.261  ±0.005
test d32 T24 ow0.3: acc 0.971  margin 0.363  ±0.003
test d8 T6 ow0.3: acc 0.843  margin 0.140  ±0.008
test d16 T64 K8 ow0.3: acc 0.879  margin 0.205  ±0.007
test d16 T128 K8 ow0.3: acc 0.890  margin 0.207  ±0.010
```

# Search seed 14

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 968447  time: 2570s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357223 attempts, 254949 blocks inserted, 266004 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 150004 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2164 candidates
* decayed linear attention: 13172 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 10100 candidates
- delta rule (beta=1) (acc 0.578): 60404 candidates
- delta rule (beta=0.5) (acc 0.617): 60404 candidates
- gated delta (alpha=0.9) (acc 0.519): 58100 candidates

## Best rule

```
S' = (((0.111·((S + S) - P2) + 0.111·((S + S) - P2)) + ((0.111·((S + S) - P2) + 0.111·((S + S) - P2)) + ((v + -0.132·P1·(k + k)))⊗(((k + k) + k)))) + ((P1 + ((v + -0.132·P1·(k + k)))⊗(((k + k) + k))) + 0.082·(((v + -0.132·P1·(k + k)))⊗(((k + k) + k)))((0.111·((S + S) - P2) + 0.111·((S + S) - P2)))))
P1' = ((P1 + ((v + -0.132·P1·(k + k)))⊗(((k + k) + k))) + 0.082·(((v + -0.132·P1·(k + k)))⊗(((k + k) + k)))((0.111·((S + S) - P2) + 0.111·((S + S) - P2))))
P2' = (((v + -0.132·P1·(k + k)))⊗(((k + k) + k)) + ((0.111·((S + S) - P2) + 0.111·((S + S) - P2)) + ((v + -0.132·P1·(k + k)))⊗(((k + k) + k))))

Effective program (21 instructions):
  s3 = -0.1322
  M0 = MatAdd(M0, M0)
  M0 = MatSub(M0, M2)
  s0 = 0.1115
  M0 = MatScale(s0, M0)
  M3 = MatAdd(M0, M0)
  V2 = VecAdd(V0, V0)
  V4 = MatVec(M1, V2)
  V4 = VecScale(s3, V4)
  V1 = VecAdd(V1, V4)
  V2 = VecAdd(V2, V0)
  M2 = Outer(V1, V2)
  M1 = MatAdd(M1, M2)
  M0 = MatMul(M2, M3)
  s1 = 0.0816
  M0 = MatScale(s1, M0)
  M1 = MatAdd(M1, M0)
  M0 = MatAdd(M3, M2)
  M2 = MatAdd(M2, M0)
  M3 = MatAdd(M3, M0)
  M0 = MatAdd(M3, M1)

structure: unclassified  [a=1.025 b=6.028 c=-0.494 g=-0.001, erase c/a=0.482, R²=0.8599, 1408 steps]

train acc 0.676 ±0.013
test regime collision3: acc 0.673  margin 0.073  ±0.006
test d16 T12 ow0.3: acc 0.940  margin 0.276  ±0.004
test d16 T12 ow0.0: acc 0.913  margin 0.248  ±0.004
test d16 T12 ow0.6: acc 0.917  margin 0.257  ±0.005
test d32 T24 ow0.3: acc 0.971  margin 0.366  ±0.003
test d8 T6 ow0.3: acc 0.824  margin 0.125  ±0.008
test d16 T64 K8 ow0.3: acc 0.823  margin 0.167  ±0.008
test d16 T128 K8 ow0.3: acc 0.821  margin 0.163  ±0.012
```

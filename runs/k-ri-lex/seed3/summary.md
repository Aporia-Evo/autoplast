# Search seed 3

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 958723  time: 5006s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357779 attempts, 226257 blocks inserted, 248356 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 200052 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3316 candidates
* linear attention: 4340 candidates
* decayed linear attention: 6900 candidates
* gated delta rule: 176244 candidates
* delta rule: 177652 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 4340 candidates
- delta rule (beta=1) (acc 0.578): 177268 candidates
- delta rule (beta=0.5) (acc 0.617): 178036 candidates
- gated delta (alpha=0.9) (acc 0.519): 156404 candidates

## Best rule

```
S' = (((S + P2) + ((v + v))⊗(1.694·k)) + (((S + P2))(-0.821·(k)⊗(k)) + (-0.006·(S + P2))ᵀ))
P1' = (((S + P2))(-0.821·(k)⊗(k)) + (-0.006·(S + P2))ᵀ)
P2' = ((-0.821·(P2 - (P2 + P2)) + -0.006·(S + P2)) + ((v + v))⊗(1.694·k))

Effective program (20 instructions):
  s1 = -0.8213
  M0 = MatAdd(M0, M2)
  M1 = MatAdd(M2, M2)
  M2 = MatSub(M2, M1)
  s3 = 1.6939
  M1 = Outer(V0, V0)
  M2 = MatScale(s1, M2)
  M1 = MatScale(s1, M1)
  M1 = MatMul(M0, M1)
  V2 = VecAdd(V1, V1)
  V1 = VecScale(s3, V0)
  s0 = -0.0064
  M3 = MatScale(s0, M0)
  M2 = MatAdd(M2, M3)
  M3 = Transpose(M3)
  M1 = MatAdd(M1, M3)
  M3 = Outer(V2, V1)
  M2 = MatAdd(M2, M3)
  M0 = MatAdd(M0, M3)
  M0 = MatAdd(M0, M1)

structure: unclassified  [a=1.075 b=3.391 c=-0.874 g=-0.001, erase c/a=0.813, R²=0.8335, 1408 steps]

train acc 0.734 ±0.013
test regime collision3: acc 0.719  margin 0.110  ±0.006
test d16 T12 ow0.3: acc 0.949  margin 0.278  ±0.003
test d16 T12 ow0.0: acc 0.944  margin 0.268  ±0.003
test d16 T12 ow0.6: acc 0.926  margin 0.247  ±0.005
test d32 T24 ow0.3: acc 0.971  margin 0.359  ±0.003
test d8 T6 ow0.3: acc 0.833  margin 0.133  ±0.008
test d16 T64 K8 ow0.3: acc 0.871  margin 0.193  ±0.007
test d16 T128 K8 ow0.3: acc 0.881  margin 0.192  ±0.010
```

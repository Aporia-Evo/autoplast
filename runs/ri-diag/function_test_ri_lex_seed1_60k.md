# Search seed 1

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 60020  real evaluations (after cache): 26423  time: 130s  pop: 500  tournament: 10

commit: c5eee89  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 14075 attempts, 12059 blocks inserted, 12080 times dead instructions removed first

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1140 candidates
* unclassified: 2292 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5620 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((v)⊗((k + -0.009·(v ⊙ 0))) + ((((S - P1) + -0.067·(P2 + (S - P1))) + (0.088 + -0.067)·0) + (v)⊗((k + -0.009·(v ⊙ 0)))))
P1' = (0.088 + -0.067)·(((v)⊗((k + -0.009·(v ⊙ 0))) + ((((S - P1) + -0.067·(P2 + (S - P1))) + (0.088 + -0.067)·0) + (v)⊗((k + -0.009·(v ⊙ 0))))))(((v)⊗((k + -0.009·(v ⊙ 0))) + ((((S - P1) + -0.067·(P2 + (S - P1))) + (0.088 + -0.067)·0) + (v)⊗((k + -0.009·(v ⊙ 0))))))
P2' = ((((S - P1) + -0.067·(P2 + (S - P1))) + (0.088 + -0.067)·0) + -0.067·(P2 + (S - P1)))

Effective program (20 instructions):
  V5 = Hadamard(V1, V5)
  s3 = -0.0087
  V5 = VecScale(s3, V5)
  V0 = VecAdd(V0, V5)
  M1 = MatSub(M0, M1)
  M0 = Outer(V1, V0)
  s3 = -0.0675
  M2 = MatAdd(M2, M1)
  M2 = MatScale(s3, M2)
  M1 = MatAdd(M1, M2)
  s1 = 0.0877
  s0 = SAdd(s1, s3)
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  M3 = MatAdd(M1, M0)
  M2 = MatAdd(M1, M2)
  M1 = MatAdd(M0, M3)
  M1 = MatMul(M1, M1)
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M3)

structure: unclassified  [a=0.896 b=1.999 c=0.000 g=0.001, erase c/a=-0.000, R²=0.8761, 1408 steps]

train acc 0.514 ±0.014
test regime collision3: acc 0.516  margin -0.038  ±0.006
test d16 T12 ow0.3: acc 0.743  margin 0.128  ±0.007
test d16 T12 ow0.0: acc 0.750  margin 0.129  ±0.006
test d16 T12 ow0.6: acc 0.699  margin 0.095  ±0.009
test d32 T24 ow0.3: acc 0.652  margin 0.111  ±0.007
test d8 T6 ow0.3: acc 0.591  margin 0.012  ±0.010
test d16 T64 K8 ow0.3: acc 0.579  margin -0.012  ±0.011
test d16 T128 K8 ow0.3: acc 0.549  margin -0.032  ±0.016
```

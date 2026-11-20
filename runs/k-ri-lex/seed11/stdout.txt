# Search seed 11

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 909216  time: 2471s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357352 attempts, 273565 blocks inserted, 293143 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 600052 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1396 candidates
* decayed linear attention: 1908 candidates
* linear attention: 13428 candidates
* gated delta rule: 20340 candidates
* delta rule: 20596 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 13428 candidates
- delta rule (beta=1) (acc 0.578): 20596 candidates
- delta rule (beta=0.5) (acc 0.617): 21364 candidates
- gated delta (alpha=0.9) (acc 0.519): 20340 candidates

## Best rule

```
S' = ((((S + 0) + -0.029·(P2 + S)) + (((v + v) + -0.513·(P2 + S)·(k - 0)))⊗((k - 0))) + ((0.349·(P2 + σ(0)·((P2 + S)·(k - 0))⊗((k - 0))) + (((v + v) + -0.513·(P2 + S)·(k - 0)))⊗((k - 0))) - -0.513·(P2 + σ(0)·((P2 + S)·(k - 0))⊗((k - 0)))))
P1' = (((S + 0) + -0.029·(P2 + S)) + (((v + v) + -0.513·(P2 + S)·(k - 0)))⊗((k - 0)))
P2' = ((0.349·(P2 + σ(0)·((P2 + S)·(k - 0))⊗((k - 0))) + (((v + v) + -0.513·(P2 + S)·(k - 0)))⊗((k - 0))) - -0.513·(P2 + σ(0)·((P2 + S)·(k - 0))⊗((k - 0))))

Effective program (23 instructions):
  V1 = VecAdd(V1, V1)
  M1 = MatAdd(M0, M3)
  V2 = VecSub(V0, V5)
  M0 = MatAdd(M2, M0)
  V0 = MatVec(M0, V2)
  M3 = Outer(V0, V2)
  s0 = Sigmoid(s1)
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)
  s2 = -0.5125
  V0 = VecScale(s2, V0)
  s3 = -0.0293
  M0 = MatScale(s3, M0)
  M1 = MatAdd(M1, M0)
  V1 = VecAdd(V1, V0)
  M0 = Outer(V1, V2)
  M3 = MatScale(s2, M2)
  M1 = MatAdd(M1, M0)
  s2 = 0.3485
  M2 = MatScale(s2, M2)
  M0 = MatAdd(M2, M0)
  M2 = MatSub(M0, M3)
  M0 = MatAdd(M1, M2)

structure: unclassified  [a=1.053 b=4.002 c=-0.642 g=-0.000, erase c/a=0.610, R²=0.8952, 1408 steps]

train acc 0.704 ±0.013
test regime collision3: acc 0.695  margin 0.093  ±0.006
test d16 T12 ow0.3: acc 0.953  margin 0.274  ±0.003
test d16 T12 ow0.0: acc 0.931  margin 0.255  ±0.003
test d16 T12 ow0.6: acc 0.946  margin 0.254  ±0.004
test d32 T24 ow0.3: acc 0.975  margin 0.362  ±0.002
test d8 T6 ow0.3: acc 0.818  margin 0.123  ±0.008
test d16 T64 K8 ow0.3: acc 0.885  margin 0.202  ±0.007
test d16 T128 K8 ow0.3: acc 0.897  margin 0.201  ±0.009
```

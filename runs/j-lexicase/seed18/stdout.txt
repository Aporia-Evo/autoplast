# Search seed 18

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 748751  time: 6558s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* decayed linear attention: 1268 candidates
* linear attention: 5108 candidates
* delta rule: 635380 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5108 candidates
- delta rule (beta=1) (acc 0.578): 632820 candidates
- delta rule (beta=0.5) (acc 0.617): 635892 candidates
- gated delta (alpha=0.9) (acc 0.519): 142068 candidates

## Best rule

```
S' = (((S - P1) + (0.770·(v)⊗(k) - ((S - P1))(((0.770·(v)⊗(k))ᵀ)(0.770·(v)⊗(k))))) + …)
P1' = …
P2' = ((S - P1) + (0.770·(v)⊗(k) - ((S - P1))(((0.770·(v)⊗(k))ᵀ)(0.770·(v)⊗(k)))))

Effective program (16 instructions):
  M2 = MatSub(M0, M1)
  s0 = 0.7700
  M0 = Outer(V1, V0)
  M0 = MatScale(s0, M0)
  M1 = MatSub(M3, M0)
  M3 = Transpose(M0)
  M3 = MatMul(M3, M0)
  M3 = MatMul(M2, M3)
  M0 = MatSub(M0, M3)
  M2 = MatAdd(M2, M0)
  M3 = Transpose(M3)
  M0 = MatSub(M2, M3)
  M1 = MatAdd(M0, M1)
  M0 = MatMul(M2, M1)
  M1 = MatMul(M0, M1)
  M0 = MatAdd(M2, M1)

structure: unclassified  [a=1.003 b=0.686 c=-0.695 g=0.004, erase c/a=0.693, R²=0.3262, 1408 steps]

train acc 0.681 ±0.013
test regime collision3: acc 0.684  margin 0.067  ±0.006
test d16 T12 ow0.3: acc 0.906  margin 0.220  ±0.004
test d16 T12 ow0.0: acc 0.855  margin 0.178  ±0.004
test d16 T12 ow0.6: acc 0.939  margin 0.235  ±0.005
test d32 T24 ow0.3: acc 0.984  margin 0.311  ±0.002
test d8 T6 ow0.3: acc 0.719  margin 0.076  ±0.009
test d16 T64 K8 ow0.3: acc 0.792  margin 0.129  ±0.009
test d16 T128 K8 ow0.3: acc 0.796  margin 0.129  ±0.013
```

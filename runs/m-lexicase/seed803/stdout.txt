# Search seed 803

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 707819  time: 1579s  pop: 500  tournament: 10

commit: dce11aa  task seed: 803  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 6388 candidates
* decayed linear attention: 34420 candidates
* gated Kronecker delta rule: 476404 candidates
* delta rule: 949748 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.384): 14068 candidates
- delta rule (beta=1) (acc 0.590): 949748 candidates
- delta rule (beta=0.5) (acc 0.618): 951540 candidates
- gated delta (alpha=0.9) (acc 0.518): 34420 candidates

## Best rule

```
S' = (((S)ᵀ - 0.414·((P1·v - k))⊗((v - S·k))))ᵀ
P1' = 0.414·((0 + P2) - S)
P2' = ((S)ᵀ - 0.414·((P1·v - k))⊗((v - S·k)))

Effective program (13 instructions):
  M3 = MatAdd(M3, M2)
  M2 = Transpose(M0)
  s3 = 0.4141
  V4 = MatVec(M1, V1)
  V5 = MatVec(M0, V0)
  V1 = VecSub(V1, V5)
  V0 = VecSub(V4, V0)
  M1 = Outer(V0, V1)
  M3 = MatSub(M3, M0)
  M1 = MatScale(s3, M1)
  M2 = MatSub(M2, M1)
  M1 = MatScale(s3, M3)
  M0 = Transpose(M2)

structure: unclassified  [a=0.993 b=0.416 c=-0.405 g=-0.118, erase c/a=0.408, R²=0.9498, 1408 steps]

train acc 0.636 ±0.014
test regime collision3: acc 0.631  margin 0.037  ±0.006
test d16 T12 ow0.3: acc 0.904  margin 0.235  ±0.004
test d16 T12 ow0.0: acc 0.881  margin 0.215  ±0.004
test d16 T12 ow0.6: acc 0.914  margin 0.230  ±0.005
test d32 T24 ow0.3: acc 0.981  margin 0.327  ±0.002
test d8 T6 ow0.3: acc 0.743  margin 0.076  ±0.009
test d16 T64 K8 ow0.3: acc 0.795  margin 0.126  ±0.009
test d16 T128 K8 ow0.3: acc 0.776  margin 0.118  ±0.013
```

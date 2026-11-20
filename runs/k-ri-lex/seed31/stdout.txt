# Search seed 31

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 916886  time: 2279s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 356367 attempts, 277928 blocks inserted, 304166 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 2292 candidates
* decayed linear attention: 2804 candidates
* linear attention: 8564 candidates
* delta rule: 104180 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8564 candidates
- delta rule (beta=1) (acc 0.578): 104692 candidates
- delta rule (beta=0.5) (acc 0.617): 104692 candidates
- gated delta (alpha=0.9) (acc 0.519): 99188 candidates

## Best rule

```
S' = (((v + (-0.217 + -0.019·σ(0))·S·k))⊗((k + k)) + ((P1 + S) + ((0 - (0 - ((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)))ᵀ)) + ((-0.217 + -0.019·σ(0))·(((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)) + (0 - ((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)))ᵀ)) + (0 - ((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)))ᵀ)))((0 - (0 - ((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)))ᵀ))))))
P1' = (((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)) + (0 - ((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)))ᵀ)) + (0 - ((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)))ᵀ))
P2' = ((P1 + S) + ((0 - (0 - ((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)))ᵀ)) + ((-0.217 + -0.019·σ(0))·(((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)) + (0 - ((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)))ᵀ)) + (0 - ((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)))ᵀ)))((0 - (0 - ((-0.217 + -0.019·σ(0))·(P2 - (P1 + S)))ᵀ)))))

Effective program (23 instructions):
  V5 = MatVec(M0, V0)
  s0 = -0.2172
  M0 = MatAdd(M1, M0)
  s3 = Sigmoid(s3)
  s2 = -0.0191
  s3 = SMul(s2, s3)
  s0 = SAdd(s0, s3)
  V5 = VecScale(s0, V5)
  V1 = VecAdd(V1, V5)
  V4 = VecAdd(V0, V0)
  M2 = MatSub(M2, M0)
  M1 = MatScale(s0, M2)
  M2 = Transpose(M1)
  M2 = MatSub(M3, M2)
  M1 = MatAdd(M1, M2)
  M3 = MatSub(M3, M2)
  M1 = MatAdd(M1, M2)
  M2 = MatScale(s0, M1)
  M2 = MatMul(M2, M3)
  M3 = MatAdd(M3, M2)
  M2 = MatAdd(M0, M3)
  M0 = Outer(V1, V4)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=1.012 b=2.000 c=-0.432 g=-0.001, erase c/a=0.427, R²=0.7145, 1408 steps]

train acc 0.671 ±0.013
test regime collision3: acc 0.664  margin 0.056  ±0.006
test d16 T12 ow0.3: acc 0.929  margin 0.236  ±0.004
test d16 T12 ow0.0: acc 0.920  margin 0.228  ±0.003
test d16 T12 ow0.6: acc 0.888  margin 0.200  ±0.006
test d32 T24 ow0.3: acc 0.975  margin 0.332  ±0.002
test d8 T6 ow0.3: acc 0.726  margin 0.081  ±0.009
test d16 T64 K8 ow0.3: acc 0.794  margin 0.125  ±0.009
test d16 T128 K8 ow0.3: acc 0.784  margin 0.118  ±0.013
```

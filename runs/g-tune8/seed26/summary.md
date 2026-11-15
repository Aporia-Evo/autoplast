# Search seed 26

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500172  real evaluations (after cache): 957486  time: 2539s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* unclassified: 2804 candidates
* linear attention: 8580 candidates
* delta rule: 368500 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8580 candidates
- delta rule (beta=1) (acc 0.578): 368500 candidates
- delta rule (beta=0.5) (acc 0.617): 371364 candidates
- gated delta (alpha=0.9) (acc 0.519): 368500 candidates

## Best rule

```
S' = (((0 - P1) + S) + (tanh(0.720·0.720·(v - ((0 - P1) + S)·tanh(k))))⊗((k - 0)))
P1' = ((tanh(0.720·0.720·(v - ((0 - P1) + S)·tanh(k))))⊗((k - 0)))(0.720·((0 - P1) + S))
P2' = (tanh(0.720·0.720·(v - ((0 - P1) + S)·tanh(k))))⊗((k - 0))

Effective program (14 instructions):
  V4 = Tanh(V0)
  M1 = MatSub(M3, M1)
  M0 = MatAdd(M1, M0)
  s1 = 0.7199
  V3 = VecSub(V0, V5)
  V0 = MatVec(M0, V4)
  V1 = VecSub(V1, V0)
  s0 = SMul(s1, s1)
  V5 = VecScale(s0, V1)
  V0 = Tanh(V5)
  M2 = Outer(V0, V3)
  M1 = MatScale(s1, M0)
  M1 = MatMul(M2, M1)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=0.999 b=0.506 c=-0.479 g=0.018, erase c/a=0.479, R²=0.3863, 1408 steps]

train acc 0.653 ±0.014
test regime collision3: acc 0.650  margin 0.051  ±0.006
test d16 T12 ow0.3: acc 0.880  margin 0.218  ±0.005
test d16 T12 ow0.0: acc 0.877  margin 0.206  ±0.004
test d16 T12 ow0.6: acc 0.887  margin 0.207  ±0.006
test d32 T24 ow0.3: acc 0.960  margin 0.317  ±0.003
test d8 T6 ow0.3: acc 0.659  margin 0.050  ±0.010
test d16 T64 K8 ow0.3: acc 0.788  margin 0.132  ±0.009
test d16 T128 K8 ow0.3: acc 0.765  margin 0.120  ±0.013
```

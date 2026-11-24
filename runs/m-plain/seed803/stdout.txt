# Search seed 803

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 818846  time: 1748s  pop: 500  tournament: 10

commit: dce11aa  task seed: 803  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 884 candidates
* unclassified: 4980 candidates
* linear attention: 6516 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.384): 6516 candidates
- delta rule (beta=1) (acc 0.590): 137332 candidates
- delta rule (beta=0.5) (acc 0.618): 137332 candidates
- gated delta (alpha=0.9) (acc 0.518): 108404 candidates

## Best rule

```
S' = (((v)⊗(k) + (S + (v)⊗(k))) + (tanh(σ(0.670)·P1·(0 - tanh(k))))⊗(tanh(k)))
P1' = σ(<(σ(0.670)·P1·(0 - tanh(k)) + (0 - tanh(k))), σ(0.670)·P1·(0 - tanh(k))>·<(σ(0.670)·P1·(0 - tanh(k)) + (0 - tanh(k))), σ(0.670)·P1·(0 - tanh(k))>)·((v)⊗(k) + (S + (v)⊗(k)))
P2' = ((v)⊗(k) + (S + (v)⊗(k)))

Effective program (17 instructions):
  M2 = Outer(V1, V0)
  V4 = Tanh(V0)
  s2 = 0.6700
  V3 = VecSub(V3, V4)
  V5 = MatVec(M1, V3)
  M0 = MatAdd(M0, M2)
  M2 = MatAdd(M2, M0)
  s3 = Sigmoid(s2)
  V1 = VecScale(s3, V5)
  V5 = Tanh(V1)
  M0 = Outer(V5, V4)
  V3 = VecAdd(V1, V3)
  s3 = Dot(V3, V1)
  s3 = SMul(s3, s3)
  s1 = Sigmoid(s3)
  M1 = MatScale(s1, M2)
  M0 = MatAdd(M2, M0)

structure: unclassified  [a=1.000 b=1.994 c=-0.471 g=0.006, erase c/a=0.471, R²=0.9762, 1408 steps]

train acc 0.642 ±0.014
test regime collision3: acc 0.643  margin 0.046  ±0.006
test d16 T12 ow0.3: acc 0.912  margin 0.231  ±0.004
test d16 T12 ow0.0: acc 0.926  margin 0.233  ±0.003
test d16 T12 ow0.6: acc 0.899  margin 0.214  ±0.006
test d32 T24 ow0.3: acc 0.981  margin 0.319  ±0.002
test d8 T6 ow0.3: acc 0.738  margin 0.089  ±0.009
test d16 T64 K8 ow0.3: acc 0.812  margin 0.148  ±0.009
test d16 T128 K8 ow0.3: acc 0.808  margin 0.140  ±0.012
```

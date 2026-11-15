# Search seed 20

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500132  real evaluations (after cache): 1064068  time: 2729s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2044 candidates
* unclassified: 10300 candidates
* delta rule: 309924 candidates
* linear, not error-correcting: 312396 candidates
* delta + Kronecker mix: 417316 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 309092 candidates
- delta rule (beta=1) (acc 0.578): 309092 candidates
- delta rule (beta=0.5) (acc 0.617): 314236 candidates
- gated delta (alpha=0.9) (acc 0.519): 309092 candidates

## Best rule

```
S' = (((P2 + P2))((|tanh((v - S·tanh(tanh(k))))|·(v - S·tanh(tanh(k))))⊗(0.461·k)) + ((|tanh((v - S·tanh(tanh(k))))|·(v - S·tanh(tanh(k))))⊗(0.461·k) + S))
P1' = ((P2 + P2))((|tanh((v - S·tanh(tanh(k))))|·(v - S·tanh(tanh(k))))⊗(0.461·k))
P2' = σ(σ(<v, tanh((v - S·tanh(tanh(k))))>))·P2

Effective program (18 instructions):
  s3 = 0.4612
  V2 = Tanh(V0)
  V4 = Tanh(V2)
  V4 = MatVec(M0, V4)
  V5 = VecSub(V1, V4)
  V3 = Tanh(V5)
  s2 = Norm(V3)
  V2 = VecScale(s2, V5)
  s2 = Dot(V1, V3)
  M1 = MatAdd(M2, M2)
  V1 = VecScale(s3, V0)
  M3 = Outer(V2, V1)
  M0 = MatAdd(M3, M0)
  M1 = MatMul(M1, M3)
  s3 = Sigmoid(s2)
  M0 = MatAdd(M1, M0)
  s3 = Sigmoid(s3)
  M2 = MatScale(s3, M2)

structure: unclassified  [a=1.000 b=0.601 c=-0.577 g=-0.310, erase c/a=0.577, R²=0.8693, 1408 steps]

train acc 0.657 ±0.014
test regime collision3: acc 0.668  margin 0.061  ±0.006
test d16 T12 ow0.3: acc 0.957  margin 0.270  ±0.003
test d16 T12 ow0.0: acc 0.952  margin 0.258  ±0.003
test d16 T12 ow0.6: acc 0.939  margin 0.250  ±0.005
test d32 T24 ow0.3: acc 0.992  margin 0.350  ±0.001
test d8 T6 ow0.3: acc 0.835  margin 0.131  ±0.008
test d16 T64 K8 ow0.3: acc 0.818  margin 0.134  ±0.009
test d16 T128 K8 ow0.3: acc 0.809  margin 0.128  ±0.012
```

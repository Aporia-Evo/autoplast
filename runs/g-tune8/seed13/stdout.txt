# Search seed 13

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500060  real evaluations (after cache): 968988  time: 2282s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* unclassified: 2676 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6388 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = ((((v)⊗(k))ᵀ + (1/(|tanh(tanh(v))|)·((((v)⊗(k) + (v)⊗(k)) + (v)⊗(k)) + (((v)⊗(k) + (v)⊗(k)) + (v)⊗(k))) + P1)) - ((v)⊗(k))ᵀ)
P1' = 0.892·(((v)⊗(k))ᵀ + (1/(|tanh(tanh(v))|)·((((v)⊗(k) + (v)⊗(k)) + (v)⊗(k)) + (((v)⊗(k) + (v)⊗(k)) + (v)⊗(k))) + P1))
P2' = ((((v)⊗(k) + (v)⊗(k)) + (v)⊗(k)) + (((v)⊗(k) + (v)⊗(k)) + (v)⊗(k)))

Effective program (15 instructions):
  M0 = Outer(V1, V0)
  V2 = Tanh(V1)
  V3 = Tanh(V2)
  s0 = Norm(V3)
  M2 = MatAdd(M0, M0)
  M3 = MatAdd(M2, M0)
  s3 = Recip(s0)
  M2 = MatAdd(M3, M3)
  M3 = MatScale(s3, M2)
  M1 = MatAdd(M3, M1)
  M3 = Transpose(M0)
  M1 = MatAdd(M3, M1)
  M0 = MatSub(M1, M3)
  s1 = 0.8917
  M1 = MatScale(s1, M1)

structure: unclassified  [a=0.894 b=6.592 c=-0.000 g=-0.005, erase c/a=0.000, R²=0.9702, 1408 steps]

train acc 0.514 ±0.014
test regime collision3: acc 0.517  margin -0.037  ±0.006
test d16 T12 ow0.3: acc 0.745  margin 0.133  ±0.007
test d16 T12 ow0.0: acc 0.749  margin 0.130  ±0.006
test d16 T12 ow0.6: acc 0.718  margin 0.105  ±0.009
test d32 T24 ow0.3: acc 0.682  margin 0.129  ±0.007
test d8 T6 ow0.3: acc 0.628  margin 0.031  ±0.010
test d16 T64 K8 ow0.3: acc 0.579  margin -0.008  ±0.011
test d16 T128 K8 ow0.3: acc 0.551  margin -0.026  ±0.016
```

# Search seed 7

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 960341  time: 2381s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 756 candidates
* decayed linear attention: 1012 candidates
* linear, not error-correcting: 177140 candidates
* delta rule: 182900 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 18932 candidates
- delta rule (beta=1) (acc 0.578): 177140 candidates
- delta rule (beta=0.5) (acc 0.617): 482292 candidates
- gated delta (alpha=0.9) (acc 0.519): 19700 candidates

## Best rule

```
S' = (((v)⊗(tanh((tanh(k) + tanh(k)))) - (P2 - (v)⊗(tanh((tanh(k) + tanh(k)))))) + (S + P1))
P1' = (((tanh((tanh(k) + tanh(k))) + v) - (((v)⊗(tanh((tanh(k) + tanh(k)))) - (P2 - (v)⊗(tanh((tanh(k) + tanh(k)))))) + (S + P1))·tanh((tanh(k) + tanh(k)))))⊗(tanh(σ((0 + 0))·k))
P2' = σ(σ((0 + 0)))·(P2 - (v)⊗(tanh((tanh(k) + tanh(k)))))

Effective program (19 instructions):
  V4 = Tanh(V0)
  V2 = VecAdd(V4, V4)
  V5 = Tanh(V2)
  s3 = SAdd(s1, s0)
  V2 = VecAdd(V5, V1)
  s1 = Sigmoid(s3)
  M3 = Outer(V1, V5)
  s2 = Sigmoid(s1)
  M2 = MatSub(M2, M3)
  M0 = MatAdd(M0, M1)
  M1 = MatSub(M3, M2)
  M2 = MatScale(s2, M2)
  M3 = MatAdd(M1, M0)
  V3 = MatVec(M3, V5)
  V4 = VecSub(V2, V3)
  M0 = MatAdd(M1, M0)
  V5 = VecScale(s1, V0)
  V0 = Tanh(V5)
  M1 = Outer(V4, V0)

structure: unclassified  [a=0.942 b=3.205 c=-0.081 g=-0.001, erase c/a=0.086, R²=0.6007, 1408 steps]

train acc 0.638 ±0.014
test regime collision3: acc 0.628  margin 0.035  ±0.006
test d16 T12 ow0.3: acc 0.905  margin 0.231  ±0.004
test d16 T12 ow0.0: acc 0.880  margin 0.209  ±0.004
test d16 T12 ow0.6: acc 0.890  margin 0.217  ±0.006
test d32 T24 ow0.3: acc 0.965  margin 0.327  ±0.003
test d8 T6 ow0.3: acc 0.709  margin 0.072  ±0.009
test d16 T64 K8 ow0.3: acc 0.810  margin 0.151  ±0.009
test d16 T128 K8 ow0.3: acc 0.789  margin 0.144  ±0.013
```

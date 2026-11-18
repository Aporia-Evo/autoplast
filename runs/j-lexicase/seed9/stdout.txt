# Search seed 9

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 958140  time: 4886s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 100084 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1524 candidates
* linear attention: 5492 candidates
* decayed linear attention: 10868 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5492 candidates
- delta rule (beta=1) (acc 0.578): 37236 candidates
- delta rule (beta=0.5) (acc 0.617): 37492 candidates
- gated delta (alpha=0.9) (acc 0.519): 36084 candidates

## Best rule

```
S' = ((((((v)⊗(k) + -0.493·P2))((tanh(k))⊗(tanh(k))) + (((v)⊗(k) + -0.493·P2))((tanh(k))⊗(tanh(k)))) - (((v)⊗(k) + -0.493·P2) - ((v)⊗(k) + (v)⊗(k)))) - (((v)⊗(k) + -0.493·P2) - ((v)⊗(k) + (v)⊗(k))))
P1' = ((-0.493·1.495·(S - P2) + (((v)⊗(k) + (v)⊗(k)) + ((v)⊗(k) + (v)⊗(k)))) + (((v)⊗(k) + (v)⊗(k)) + ((v)⊗(k) + (v)⊗(k))))
P2' = (((-0.493·1.495·(S - P2) + (((v)⊗(k) + (v)⊗(k)) + ((v)⊗(k) + (v)⊗(k)))) + (((v)⊗(k) + (v)⊗(k)) + ((v)⊗(k) + (v)⊗(k)))) + ((((((v)⊗(k) + -0.493·P2))((tanh(k))⊗(tanh(k))) + (((v)⊗(k) + -0.493·P2))((tanh(k))⊗(tanh(k)))) - (((v)⊗(k) + -0.493·P2) - ((v)⊗(k) + (v)⊗(k)))) - (((v)⊗(k) + -0.493·P2) - ((v)⊗(k) + (v)⊗(k)))))

Effective program (20 instructions):
  M1 = MatSub(M0, M2)
  s2 = 1.4948
  M3 = Outer(V1, V0)
  s1 = -0.4934
  M2 = MatScale(s1, M2)
  V4 = Tanh(V0)
  M0 = Outer(V4, V4)
  M2 = MatAdd(M3, M2)
  M0 = MatMul(M2, M0)
  M1 = MatScale(s2, M1)
  M1 = MatScale(s1, M1)
  M0 = MatAdd(M0, M0)
  M3 = MatAdd(M3, M3)
  M2 = MatSub(M2, M3)
  M0 = MatSub(M0, M2)
  M0 = MatSub(M0, M2)
  M3 = MatAdd(M3, M3)
  M2 = MatAdd(M1, M3)
  M1 = MatAdd(M2, M3)
  M2 = MatAdd(M1, M0)

structure: unclassified  [a=1.074 b=3.799 c=-0.952 g=-0.001, erase c/a=0.886, R²=0.7894, 1408 steps]

train acc 0.729 ±0.013
test regime collision3: acc 0.720  margin 0.120  ±0.006
test d16 T12 ow0.3: acc 0.951  margin 0.295  ±0.003
test d16 T12 ow0.0: acc 0.933  margin 0.270  ±0.003
test d16 T12 ow0.6: acc 0.950  margin 0.275  ±0.004
test d32 T24 ow0.3: acc 0.977  margin 0.378  ±0.002
test d8 T6 ow0.3: acc 0.804  margin 0.118  ±0.008
test d16 T64 K8 ow0.3: acc 0.883  margin 0.213  ±0.007
test d16 T128 K8 ow0.3: acc 0.899  margin 0.213  ±0.009
```

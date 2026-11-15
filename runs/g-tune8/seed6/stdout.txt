# Search seed 6

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500028  real evaluations (after cache): 1056448  time: 4356s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 628 candidates
* unclassified: 12068 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 13476 candidates
- delta rule (beta=1) (acc 0.578): 749340 candidates
- delta rule (beta=0.5) (acc 0.617): 756588 candidates
- gated delta (alpha=0.9) (acc 0.519): 63476 candidates

## Best rule

```
S' = (((((v)⊗(k) - ((v)⊗(k) + -0.506·P2)) - -0.506·(v)⊗(k)) - 1.933·-0.506·(v)⊗(k)) + ((((((v)⊗(k) - ((v)⊗(k) + -0.506·P2)) - -0.506·(v)⊗(k)) - 1.933·-0.506·(v)⊗(k)) - (((((v)⊗(k) + -0.506·P2))((k)⊗(v)) - 1.933·-0.506·(v)⊗(k)))(1.933·-0.506·(v)⊗(k))) + ((((v)⊗(k) - ((v)⊗(k) + -0.506·P2)) - -0.506·(v)⊗(k)) - 1.933·-0.506·(v)⊗(k))))
P1' = (((v)⊗(k) + -0.506·P2))((k)⊗(v))
P2' = ((((((v)⊗(k) - ((v)⊗(k) + -0.506·P2)) - -0.506·(v)⊗(k)) - 1.933·-0.506·(v)⊗(k)) - (((((v)⊗(k) + -0.506·P2))((k)⊗(v)) - 1.933·-0.506·(v)⊗(k)))(1.933·-0.506·(v)⊗(k))) + ((((v)⊗(k) - ((v)⊗(k) + -0.506·P2)) - -0.506·(v)⊗(k)) - 1.933·-0.506·(v)⊗(k)))

Effective program (17 instructions):
  M0 = Outer(V1, V0)
  s0 = -0.5059
  M1 = MatScale(s0, M2)
  M3 = MatScale(s0, M0)
  M1 = MatAdd(M0, M1)
  M2 = Outer(V0, V1)
  M0 = MatSub(M0, M1)
  M0 = MatSub(M0, M3)
  s3 = 1.9330
  M3 = MatScale(s3, M3)
  M1 = MatMul(M1, M2)
  M0 = MatSub(M0, M3)
  M2 = MatSub(M1, M3)
  M3 = MatMul(M2, M3)
  M3 = MatSub(M0, M3)
  M2 = MatAdd(M3, M0)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=1.006 b=5.416 c=-0.331 g=0.009, erase c/a=0.329, R²=0.9318, 1408 steps]

train acc 0.641 ±0.014
test regime collision3: acc 0.645  margin 0.049  ±0.006
test d16 T12 ow0.3: acc 0.930  margin 0.252  ±0.004
test d16 T12 ow0.0: acc 0.915  margin 0.237  ±0.004
test d16 T12 ow0.6: acc 0.925  margin 0.239  ±0.005
test d32 T24 ow0.3: acc 0.989  margin 0.345  ±0.002
test d8 T6 ow0.3: acc 0.779  margin 0.101  ±0.009
test d16 T64 K8 ow0.3: acc 0.775  margin 0.109  ±0.009
test d16 T128 K8 ow0.3: acc 0.714  margin 0.083  ±0.014
```

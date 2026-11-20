# Search seed 32

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 897912  time: 5919s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357160 attempts, 292066 blocks inserted, 302356 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1140 candidates
* decayed linear attention: 1652 candidates
* linear attention: 3572 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3572 candidates
- delta rule (beta=1) (acc 0.578): 35316 candidates
- delta rule (beta=0.5) (acc 0.617): 753140 candidates
- gated delta (alpha=0.9) (acc 0.519): 27764 candidates

## Best rule

```
S' = (((((((P2)(-0.213·(S)((S)ᵀ)) + ((S)ᵀ + 0.247·P2)) + -0.016·((S)ᵀ + 0.247·P2)) + 0.062·((k)⊗(v))((P2)(-0.213·(S)((S)ᵀ)))) + (k)⊗(v)) + 0.083·(v)⊗(k)))ᵀ
P1' = (k)⊗(v)
P2' = ((k)⊗(v) + (k)⊗(v))

Effective program (24 instructions):
  s2 = 0.0832
  M1 = Transpose(M0)
  M0 = MatMul(M0, M1)
  s1 = -0.2132
  M0 = MatScale(s1, M0)
  s3 = 0.2467
  M3 = MatScale(s3, M2)
  M1 = MatAdd(M1, M3)
  M2 = MatMul(M2, M0)
  M3 = MatAdd(M2, M1)
  s1 = -0.0160
  M1 = MatScale(s1, M1)
  M3 = MatAdd(M3, M1)
  M1 = Outer(V0, V1)
  M2 = MatMul(M1, M2)
  s1 = 0.0623
  M2 = MatScale(s1, M2)
  M3 = MatAdd(M3, M2)
  M2 = MatAdd(M3, M1)
  M0 = Outer(V1, V0)
  M0 = MatScale(s2, M0)
  M2 = MatAdd(M2, M0)
  M0 = Transpose(M2)
  M2 = MatAdd(M1, M1)

structure: unclassified  [a=0.910 b=1.006 c=-0.038 g=-0.008, erase c/a=0.042, R²=0.8133, 1408 steps]

train acc 0.619 ±0.014
test regime collision3: acc 0.626  margin 0.029  ±0.006
test d16 T12 ow0.3: acc 0.903  margin 0.222  ±0.004
test d16 T12 ow0.0: acc 0.892  margin 0.210  ±0.004
test d16 T12 ow0.6: acc 0.880  margin 0.206  ±0.006
test d32 T24 ow0.3: acc 0.970  margin 0.313  ±0.003
test d8 T6 ow0.3: acc 0.715  margin 0.074  ±0.009
test d16 T64 K8 ow0.3: acc 0.774  margin 0.121  ±0.009
test d16 T128 K8 ow0.3: acc 0.777  margin 0.117  ±0.013
```

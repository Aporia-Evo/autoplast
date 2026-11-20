# Search seed 16

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 989699  time: 2625s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 355846 attempts, 234476 blocks inserted, 250608 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 200052 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2804 candidates
* unclassified: 3316 candidates
* linear, not error-correcting: 3956 candidates
* linear attention: 5108 candidates
* gated delta rule: 34036 candidates
* delta rule: 34292 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5108 candidates
- delta rule (beta=1) (acc 0.578): 34164 candidates
- delta rule (beta=0.5) (acc 0.617): 34420 candidates
- gated delta (alpha=0.9) (acc 0.519): 21364 candidates

## Best rule

```
S' = (((S + (P2)ᵀ) + (-0.008·((S + (P2)ᵀ))ᵀ)(-0.008·((S + (P2)ᵀ))ᵀ)) + (((v + v) + -0.224·(S + (P2)ᵀ)·(k + k)))⊗((k + k)))
P1' = (((v + v) + -0.224·(S + (P2)ᵀ)·(k + k)))⊗((k + k))
P2' = (0.780·(P2 + -0.008·((S + (P2)ᵀ))ᵀ) + (((k + k))⊗((v + v)) + ((k + k))⊗((v + v))))

Effective program (21 instructions):
  V0 = VecAdd(V0, V0)
  M1 = Transpose(M2)
  M0 = MatAdd(M0, M1)
  V1 = VecAdd(V1, V1)
  M1 = Outer(V0, V1)
  M3 = MatAdd(M1, M1)
  V2 = MatVec(M0, V0)
  s1 = -0.2240
  V2 = VecScale(s1, V2)
  V1 = VecAdd(V1, V2)
  M1 = Transpose(M0)
  s2 = -0.0081
  M1 = MatScale(s2, M1)
  M2 = MatAdd(M2, M1)
  M1 = MatMul(M1, M1)
  M0 = MatAdd(M0, M1)
  s1 = 0.7797
  M1 = Outer(V1, V0)
  M2 = MatScale(s1, M2)
  M2 = MatAdd(M2, M3)
  M0 = MatAdd(M0, M1)

structure: unclassified  [a=1.078 b=4.006 c=-0.960 g=-0.000, erase c/a=0.891, R²=0.7980, 1408 steps]

train acc 0.738 ±0.013
test regime collision3: acc 0.726  margin 0.118  ±0.006
test d16 T12 ow0.3: acc 0.951  margin 0.289  ±0.003
test d16 T12 ow0.0: acc 0.940  margin 0.271  ±0.003
test d16 T12 ow0.6: acc 0.941  margin 0.264  ±0.004
test d32 T24 ow0.3: acc 0.970  margin 0.364  ±0.003
test d8 T6 ow0.3: acc 0.843  margin 0.142  ±0.008
test d16 T64 K8 ow0.3: acc 0.880  margin 0.208  ±0.007
test d16 T128 K8 ow0.3: acc 0.893  margin 0.211  ±0.010
```

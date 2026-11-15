# Search seed 25

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500172  real evaluations (after cache): 1161031  time: 2490s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 150124 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1140 candidates
* linear, not error-correcting: 2036 candidates
* unclassified: 4100 candidates
* linear attention: 15588 candidates
* delta rule: 15988 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 15588 candidates
- delta rule (beta=1) (acc 0.578): 15988 candidates
- delta rule (beta=0.5) (acc 0.617): 24900 candidates
- gated delta (alpha=0.9) (acc 0.519): 15988 candidates

## Best rule

```
S' = ((S + P1) - (((S + P1)·tanh(tanh(k)) - (((v + v) + (v + v)) - ((tanh(tanh(k)) ⊙ (v + v)) - ((v + v) + (v + v))))))⊗(norm(tanh(k))))
P1' = σ(1.148)·(P1 + ((((v + v) + (v + v)) + ((((v + v) + (v + v)) - ((tanh(tanh(k)) ⊙ (v + v)) - ((v + v) + (v + v)))) + (((v + v) + (v + v)) - ((tanh(tanh(k)) ⊙ (v + v)) - ((v + v) + (v + v)))))))⊗(norm(tanh(k))))
P2' = (((S + P1)·tanh(tanh(k)) - (((v + v) + (v + v)) - ((tanh(tanh(k)) ⊙ (v + v)) - ((v + v) + (v + v))))))⊗(norm(tanh(k)))

Effective program (20 instructions):
  V1 = VecAdd(V1, V1)
  V4 = Tanh(V0)
  V0 = Tanh(V4)
  M0 = MatAdd(M0, M1)
  V5 = VecAdd(V1, V1)
  V2 = Hadamard(V0, V1)
  V3 = MatVec(M0, V0)
  V0 = Normalize(V4)
  s3 = 1.1484
  V1 = VecSub(V2, V5)
  V4 = VecSub(V5, V1)
  V2 = VecAdd(V4, V4)
  V5 = VecAdd(V5, V2)
  V3 = VecSub(V3, V4)
  M2 = Outer(V3, V0)
  M3 = Outer(V5, V0)
  M1 = MatAdd(M1, M3)
  s0 = Sigmoid(s3)
  M1 = MatScale(s0, M1)
  M0 = MatSub(M0, M2)

structure: unclassified  [a=1.073 b=8.012 c=-0.961 g=-0.000, erase c/a=0.896, R²=0.8188, 1408 steps]

train acc 0.730 ±0.013
test regime collision3: acc 0.721  margin 0.120  ±0.006
test d16 T12 ow0.3: acc 0.953  margin 0.293  ±0.003
test d16 T12 ow0.0: acc 0.944  margin 0.272  ±0.003
test d16 T12 ow0.6: acc 0.946  margin 0.272  ±0.004
test d32 T24 ow0.3: acc 0.983  margin 0.385  ±0.002
test d8 T6 ow0.3: acc 0.818  margin 0.124  ±0.008
test d16 T64 K8 ow0.3: acc 0.865  margin 0.196  ±0.008
test d16 T128 K8 ow0.3: acc 0.882  margin 0.197  ±0.010
```

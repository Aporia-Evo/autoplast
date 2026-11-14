# Search seed 11

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 960245  time: 675s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1908 candidates
* linear, not error-correcting: 2804 candidates
* unclassified: 4468 candidates
* linear attention: 14068 candidates
* delta rule: 30452 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 14068 candidates
- delta rule (beta=1) (acc 0.858): 30452 candidates
- delta rule (beta=0.5) (acc 0.932): 99188 candidates
- gated delta (alpha=0.9) (acc 0.729): 14068 candidates

## Best rule

```
S' = ((v)⊗(tanh(k)) - ((S)(((tanh(k) + ((tanh(k) + (tanh(k) - tanh(k))) ⊙ (tanh(k) + (tanh(k) - tanh(k))))))⊗(σ((0 + <tanh(k), v>))·tanh(k))) - S))

Effective program (14 instructions):
  V0 = Tanh(V0)
  V2 = VecSub(V0, V0)
  V4 = VecAdd(V0, V2)
  s1 = Dot(V0, V1)
  s2 = SAdd(s2, s1)
  M2 = Outer(V1, V0)
  s1 = Sigmoid(s2)
  V5 = VecScale(s1, V0)
  V1 = Hadamard(V4, V4)
  V0 = VecAdd(V0, V1)
  M1 = Outer(V0, V5)
  M3 = MatMul(M0, M1)
  M0 = MatSub(M3, M0)
  M0 = MatSub(M2, M0)

structure: delta rule  [a=1.000 b=0.951 c=-0.472 g=0.007, erase c/a=0.472, R²=0.9914, 384 steps]

train acc 0.935 ±0.009
test d16 T12 ow0.3: acc 0.919  margin 0.247  ±0.004
test d16 T12 ow0.0: acc 0.903  margin 0.232  ±0.004
test d16 T12 ow0.6: acc 0.920  margin 0.246  ±0.005
test d32 T24 ow0.3: acc 0.985  margin 0.343  ±0.002
test d8 T6 ow0.3: acc 0.766  margin 0.099  ±0.009
test d16 T64 K8 ow0.3: acc 0.775  margin 0.122  ±0.009
test d16 T128 K8 ow0.3: acc 0.725  margin 0.095  ±0.014
```

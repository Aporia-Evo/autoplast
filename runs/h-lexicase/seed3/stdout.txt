# Search seed 3

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 772459  time: 399s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1268 candidates
* decayed linear attention: 2804 candidates
* linear, not error-correcting: 4340 candidates
* linear attention: 83700 candidates
* delta rule: 133108 candidates
* delta + Kronecker mix: 140148 candidates
* gated delta rule: 310132 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 83700 candidates
- delta rule (beta=1) (acc 0.858): 112116 candidates
- delta rule (beta=0.5) (acc 0.932): 133876 candidates
- gated delta (alpha=0.9) (acc 0.729): 83700 candidates

## Best rule

```
S' = (σ(|tanh(|tanh(k)|·((0 - S)·tanh(k) + v))|)·(|tanh(k)|·((0 - S)·tanh(k) + v))⊗(k) - -1.100·S)

Effective program (14 instructions):
  s1 = -1.0998
  M1 = MatSub(M2, M0)
  V2 = Tanh(V0)
  V5 = MatVec(M1, V2)
  s2 = Norm(V2)
  M1 = MatScale(s1, M0)
  V5 = VecAdd(V5, V1)
  V1 = VecScale(s2, V5)
  V3 = Tanh(V1)
  s2 = Norm(V3)
  M0 = Outer(V1, V0)
  s0 = Sigmoid(s2)
  M0 = MatScale(s0, M0)
  M0 = MatSub(M0, M1)

structure: delta + Kronecker mix  [a=1.100 b=0.700 c=-0.685 g=-0.097, erase c/a=0.623, R²=0.9986, 384 steps]

train acc 0.978 ±0.005
test d16 T12 ow0.3: acc 0.969  margin 0.297  ±0.003
test d16 T12 ow0.0: acc 0.958  margin 0.277  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.285  ±0.004
test d32 T24 ow0.3: acc 0.994  margin 0.367  ±0.001
test d8 T6 ow0.3: acc 0.828  margin 0.130  ±0.008
test d16 T64 K8 ow0.3: acc 0.108  margin -0.431  ±0.007
test d16 T128 K8 ow0.3: acc 0.021  margin -0.628  ±0.004
```

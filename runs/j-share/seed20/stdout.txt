# Search seed 20

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 984267  time: 2633s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 4724 candidates
* decayed linear attention: 5492 candidates
* linear attention: 12660 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 12660 candidates
- delta rule (beta=1) (acc 0.578): 24692 candidates
- delta rule (beta=0.5) (acc 0.617): 34036 candidates
- gated delta (alpha=0.9) (acc 0.519): 24436 candidates

## Best rule

```
S' = ((((((v + v) + ((P1 - P2) + 0)·tanh(k)))⊗(k) + P2) + (v)⊗(k)) - (v)⊗(k))
P1' = σ(|v|)·σ(|v|)·(((((v + v) + ((P1 - P2) + 0)·tanh(k)))⊗(k) + P2) + (v)⊗(k))
P2' = (((((v + v) + ((P1 - P2) + 0)·tanh(k)))⊗(k) + P2) + (v)⊗(k))

Effective program (15 instructions):
  M1 = MatSub(M1, M2)
  V4 = VecAdd(V1, V1)
  M1 = MatAdd(M1, M3)
  V5 = Tanh(V0)
  s1 = Norm(V1)
  V3 = MatVec(M1, V5)
  M0 = Outer(V1, V0)
  V4 = VecAdd(V4, V3)
  M3 = Outer(V4, V0)
  s2 = Sigmoid(s1)
  s0 = SMul(s2, s2)
  M2 = MatAdd(M3, M2)
  M2 = MatAdd(M2, M0)
  M1 = MatScale(s0, M2)
  M0 = MatSub(M2, M0)

structure: unclassified  [a=1.027 b=2.003 c=-0.440 g=0.001, erase c/a=0.429, R²=0.8107, 1408 steps]

train acc 0.642 ±0.014
test regime collision3: acc 0.657  margin 0.054  ±0.006
test d16 T12 ow0.3: acc 0.928  margin 0.246  ±0.004
test d16 T12 ow0.0: acc 0.913  margin 0.233  ±0.004
test d16 T12 ow0.6: acc 0.914  margin 0.227  ±0.005
test d32 T24 ow0.3: acc 0.985  margin 0.336  ±0.002
test d8 T6 ow0.3: acc 0.762  margin 0.096  ±0.009
test d16 T64 K8 ow0.3: acc 0.797  margin 0.121  ±0.009
test d16 T128 K8 ow0.3: acc 0.771  margin 0.109  ±0.013
```

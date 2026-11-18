# Search seed 7

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 980806  time: 2088s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 850036 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1780 candidates
* decayed linear attention: 2804 candidates
* linear attention: 9460 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 9460 candidates
- delta rule (beta=1) (acc 0.578): 476020 candidates
- delta rule (beta=0.5) (acc 0.617): 806644 candidates
- gated delta (alpha=0.9) (acc 0.519): 141812 candidates

## Best rule

```
S' = (((v + (<P1·tanh(norm(k)), P1·tanh(norm(k))> + σ(-0.720))·(0 - S)·(tanh(k) + P1·tanh(norm(k)))))⊗(norm(σ(-0.720)·σ(-0.720)·(tanh(k) - P1·tanh(norm(k))))) - (0 - S))
P1' = (norm(norm(P1·tanh(norm(k)))))⊗(norm(norm(norm(P1·tanh(norm(k))))))
P2' = (0 - S)

Effective program (23 instructions):
  M2 = MatSub(M3, M0)
  V3 = Normalize(V0)
  V5 = Tanh(V3)
  V3 = MatVec(M1, V5)
  s0 = -0.7200
  V4 = Tanh(V0)
  s3 = Sigmoid(s0)
  V0 = Normalize(V3)
  V5 = VecSub(V4, V3)
  V0 = Normalize(V0)
  V2 = Normalize(V0)
  M1 = Outer(V0, V2)
  V0 = VecAdd(V4, V3)
  V2 = VecScale(s3, V5)
  s1 = Dot(V3, V3)
  V5 = VecScale(s3, V2)
  V5 = Normalize(V5)
  V3 = MatVec(M2, V0)
  s1 = SAdd(s1, s3)
  V4 = VecScale(s1, V3)
  V1 = VecAdd(V1, V4)
  M0 = Outer(V1, V5)
  M0 = MatSub(M0, M2)

structure: unclassified  [a=0.994 b=0.815 c=-0.337 g=0.031, erase c/a=0.339, R²=0.7818, 1408 steps]

train acc 0.710 ±0.013
test regime collision3: acc 0.712  margin 0.104  ±0.006
test d16 T12 ow0.3: acc 0.940  margin 0.271  ±0.004
test d16 T12 ow0.0: acc 0.929  margin 0.253  ±0.003
test d16 T12 ow0.6: acc 0.936  margin 0.254  ±0.005
test d32 T24 ow0.3: acc 0.985  margin 0.337  ±0.002
test d8 T6 ow0.3: acc 0.835  margin 0.140  ±0.008
test d16 T64 K8 ow0.3: acc 0.745  margin 0.103  ±0.010
test d16 T128 K8 ow0.3: acc 0.713  margin 0.082  ±0.014
```

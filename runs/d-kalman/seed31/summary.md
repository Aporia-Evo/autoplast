# Search seed 31

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1020751  time: 4346s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2164 candidates
* unclassified: 6772 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 7412 candidates
- delta rule (beta=1) (acc 0.578): 306804 candidates
- delta rule (beta=0.5) (acc 0.617): 311284 candidates
- gated delta (alpha=0.9) (acc 0.519): 305908 candidates

## Best rule

```
S' = (σ(0)·(((S + P2) + (((norm(tanh(v)) + (norm(tanh(v)) + norm(tanh(v)))) + tanh(v)))⊗(k)) + (((norm(tanh(v)) + (norm(tanh(v)) + norm(tanh(v)))) + tanh(v)))⊗(k)) + σ(0)·(((S + P2) + (((norm(tanh(v)) + (norm(tanh(v)) + norm(tanh(v)))) + tanh(v)))⊗(k)) + (((norm(tanh(v)) + (norm(tanh(v)) + norm(tanh(v)))) + tanh(v)))⊗(k)))
P1' = …
P2' = (…·norm(tanh(k)))⊗(norm(tanh(k)))

Effective program (20 instructions):
  M2 = MatAdd(M0, M2)
  V4 = Tanh(V1)
  V1 = Normalize(V4)
  V5 = VecAdd(V1, V1)
  V5 = VecAdd(V1, V5)
  V2 = VecAdd(V5, V4)
  M0 = Outer(V2, V0)
  M2 = MatAdd(M2, M0)
  M0 = MatAdd(M2, M0)
  s0 = Sigmoid(s3)
  M0 = MatScale(s0, M0)
  V5 = Tanh(V0)
  M1 = MatSub(M0, M2)
  M3 = Outer(V4, V4)
  V5 = Normalize(V5)
  M3 = MatMul(M3, M1)
  M1 = MatAdd(M3, M1)
  V4 = MatVec(M1, V5)
  M0 = MatAdd(M0, M0)
  M2 = Outer(V4, V5)

structure: unclassified  [a=0.932 b=7.907 c=-0.035 g=0.005, erase c/a=0.038, R²=0.7983, 1408 steps]

train acc 0.633 ±0.014
test regime collision3: acc 0.634  margin 0.036  ±0.006
test d16 T12 ow0.3: acc 0.912  margin 0.243  ±0.004
test d16 T12 ow0.0: acc 0.901  margin 0.227  ±0.004
test d16 T12 ow0.6: acc 0.890  margin 0.225  ±0.006
test d32 T24 ow0.3: acc 0.980  margin 0.340  ±0.002
test d8 T6 ow0.3: acc 0.741  margin 0.087  ±0.009
test d16 T64 K8 ow0.3: acc 0.792  margin 0.132  ±0.009
test d16 T128 K8 ow0.3: acc 0.784  margin 0.125  ±0.013
```

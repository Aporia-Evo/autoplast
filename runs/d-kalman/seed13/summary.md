# Search seed 13

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 770247  time: 2102s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1780 candidates
* unclassified: 2676 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 6388 candidates
- delta rule (beta=1) (acc 0.578): 1498612 candidates
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 1474292 candidates

## Best rule

```
S' = (σ(<k, (k + tanh(k))>)·((((v)⊗((k + tanh(k))) + (v)⊗((k + tanh(k)))) + P1) + (((v)⊗((k + tanh(k))) + (v)⊗((k + tanh(k)))) + P1)) - (σ(<k, (k + tanh(k))>)·(((v)⊗((k + tanh(k))) + (v)⊗((k + tanh(k)))) + P1))((k)⊗((k + tanh(k)))))
P1' = σ(<k, (k + tanh(k))>)·(((v)⊗((k + tanh(k))) + (v)⊗((k + tanh(k)))) + P1)
P2' = (σ(<k, (k + tanh(k))>)·(((v)⊗((k + tanh(k))) + (v)⊗((k + tanh(k)))) + P1))((k)⊗((k + tanh(k))))

Effective program (13 instructions):
  V5 = Tanh(V0)
  V3 = VecAdd(V0, V5)
  M0 = Outer(V1, V3)
  s2 = Dot(V0, V3)
  M0 = MatAdd(M0, M0)
  M1 = MatAdd(M0, M1)
  M0 = MatAdd(M1, M1)
  s1 = Sigmoid(s2)
  M1 = MatScale(s1, M1)
  M0 = MatScale(s1, M0)
  M2 = Outer(V0, V3)
  M2 = MatMul(M1, M2)
  M0 = MatSub(M0, M2)

structure: unclassified  [a=0.880 b=0.188 c=-0.854 g=0.000, erase c/a=0.971, R²=0.2505, 1408 steps]

train acc 0.577 ±0.014
test regime collision3: acc 0.588  margin 0.006  ±0.006
test d16 T12 ow0.3: acc 0.786  margin 0.162  ±0.006
test d16 T12 ow0.0: acc 0.756  margin 0.145  ±0.005
test d16 T12 ow0.6: acc 0.776  margin 0.147  ±0.008
test d32 T24 ow0.3: acc 0.678  margin 0.133  ±0.007
test d8 T6 ow0.3: acc 0.684  margin 0.064  ±0.010
test d16 T64 K8 ow0.3: acc 0.627  margin 0.025  ±0.011
test d16 T128 K8 ow0.3: acc 0.619  margin 0.011  ±0.015
```

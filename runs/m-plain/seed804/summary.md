# Search seed 804

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 611943  time: 1113s  pop: 500  tournament: 10

commit: dce11aa  task seed: 804  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 4212 candidates
* decayed linear attention: 5364 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.379): 10868 candidates
- delta rule (beta=1) (acc 0.589): not reached
- delta rule (beta=0.5) (acc 0.621): not reached
- gated delta (alpha=0.9) (acc 0.522): 79860 candidates

## Best rule

```
S' = ((σ(|((k + k) - tanh(v))|)·((S)ᵀ + ((k + k))⊗(v)) + ((k + k))⊗(v)))ᵀ
P1' = (σ(|((k + k) - tanh(v))|)·((S)ᵀ + ((k + k))⊗(v)) + ((k + k))⊗(v))
P2' = σ(|((k + k) - tanh(v))|)·((S)ᵀ + ((k + k))⊗(v))

Effective program (11 instructions):
  V3 = VecAdd(V0, V0)
  V0 = Tanh(V1)
  V0 = VecSub(V3, V0)
  M2 = Transpose(M0)
  s1 = Norm(V0)
  M0 = Outer(V3, V1)
  s0 = Sigmoid(s1)
  M3 = MatAdd(M2, M0)
  M2 = MatScale(s0, M3)
  M1 = MatAdd(M2, M0)
  M0 = Transpose(M1)

structure: decayed linear attention  [a=0.898 b=3.796 c=0.000 g=-0.001, erase c/a=-0.000, R²=0.9981, 1408 steps]

train acc 0.537 ±0.014
test regime collision3: acc 0.521  margin -0.032  ±0.006
test d16 T12 ow0.3: acc 0.761  margin 0.140  ±0.006
test d16 T12 ow0.0: acc 0.768  margin 0.141  ±0.005
test d16 T12 ow0.6: acc 0.714  margin 0.104  ±0.009
test d32 T24 ow0.3: acc 0.715  margin 0.149  ±0.007
test d8 T6 ow0.3: acc 0.639  margin 0.036  ±0.010
test d16 T64 K8 ow0.3: acc 0.578  margin -0.007  ±0.011
test d16 T128 K8 ow0.3: acc 0.560  margin -0.025  ±0.016
```

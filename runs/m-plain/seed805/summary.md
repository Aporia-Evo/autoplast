# Search seed 805

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 863976  time: 4957s  pop: 500  tournament: 10

commit: dce11aa  task seed: 805  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 628 candidates
* decayed linear attention: 1396 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.406): 34932 candidates
- delta rule (beta=1) (acc 0.620): not reached
- delta rule (beta=0.5) (acc 0.648): not reached
- gated delta (alpha=0.9) (acc 0.530): 109940 candidates

## Best rule

```
S' = (<tanh(v), tanh(v)>·S + (v)⊗((k - P1·k)))
P1' = (((v)⊗((k - P1·k)) + 1/(<tanh(v), tanh(v)>)·(((P2 - S))ᵀ)(((P2 - S))ᵀ)))(((v)⊗((k - P1·k)) + 1/(<tanh(v), tanh(v)>)·(((P2 - S))ᵀ)(((P2 - S))ᵀ)))
P2' = ((<tanh(v), tanh(v)>·S + (v)⊗((k - P1·k))) - (v)⊗(-1.374·P1·k))

Effective program (18 instructions):
  V5 = Tanh(V1)
  V2 = MatVec(M1, V0)
  s0 = Dot(V5, V5)
  M3 = MatSub(M2, M0)
  M0 = MatScale(s0, M0)
  V0 = VecSub(V0, V2)
  M1 = Transpose(M3)
  M1 = MatMul(M1, M1)
  M2 = Outer(V1, V0)
  s1 = Recip(s0)
  M3 = MatScale(s1, M1)
  s3 = -1.3737
  M3 = MatAdd(M2, M3)
  M0 = MatAdd(M0, M2)
  V3 = VecScale(s3, V2)
  M1 = Outer(V1, V3)
  M2 = MatSub(M0, M1)
  M1 = MatMul(M3, M3)

structure: unclassified  [a=0.903 b=0.909 c=0.001 g=0.009, erase c/a=-0.001, R²=0.8983, 1408 steps]

train acc 0.547 ±0.014
test regime collision3: acc 0.517  margin -0.058  ±0.006
test d16 T12 ow0.3: acc 0.743  margin 0.092  ±0.007
test d16 T12 ow0.0: acc 0.707  margin 0.043  ±0.006
test d16 T12 ow0.6: acc 0.000  margin 0.000  ±0.000
test d32 T24 ow0.3: acc 0.840  margin 0.205  ±0.006
test d8 T6 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T64 K8 ow0.3: acc 0.566  margin -0.008  ±0.011
test d16 T128 K8 ow0.3: acc 0.552  margin -0.027  ±0.016
```

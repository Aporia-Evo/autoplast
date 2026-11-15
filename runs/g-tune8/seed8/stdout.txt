# Search seed 8

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500044  real evaluations (after cache): 1031817  time: 5160s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3828 candidates
* decayed linear attention: 4596 candidates
* linear attention: 8612 candidates
* delta rule: 305604 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8612 candidates
- delta rule (beta=1) (acc 0.578): 305604 candidates
- delta rule (beta=0.5) (acc 0.617): 310548 candidates
- gated delta (alpha=0.9) (acc 0.519): 304276 candidates

## Best rule

```
S' = (1/(σ(5.369))·S + (((v)⊗(tanh(tanh(tanh(tanh(tanh(k)))))) - (S)((tanh(tanh(tanh(tanh(k)))))⊗(tanh(tanh(tanh(tanh(tanh(k)))))))))(1/(σ(5.369))·(tanh(tanh(tanh(tanh(k)))))⊗(tanh(tanh(tanh(tanh(tanh(k))))))))
P1' = (((v)⊗(tanh(tanh(tanh(tanh(tanh(k)))))) - (S)((tanh(tanh(tanh(tanh(k)))))⊗(tanh(tanh(tanh(tanh(tanh(k)))))))))(1/(σ(5.369))·(tanh(tanh(tanh(tanh(k)))))⊗(tanh(tanh(tanh(tanh(tanh(k)))))))
P2' = 1/(σ(5.369))·S

Effective program (16 instructions):
  V5 = Tanh(V0)
  V5 = Tanh(V5)
  V0 = Tanh(V5)
  V2 = Tanh(V0)
  V0 = Tanh(V2)
  M3 = Outer(V1, V0)
  M1 = Outer(V2, V0)
  M2 = MatMul(M0, M1)
  M3 = MatSub(M3, M2)
  s1 = 5.3690
  s0 = Sigmoid(s1)
  s0 = Recip(s0)
  M2 = MatScale(s0, M0)
  M1 = MatScale(s0, M1)
  M1 = MatMul(M3, M1)
  M0 = MatAdd(M2, M1)

structure: unclassified  [a=1.004 b=0.553 c=-0.470 g=0.004, erase c/a=0.468, R²=0.9749, 1408 steps]

train acc 0.628 ±0.014
test regime collision3: acc 0.639  margin 0.047  ±0.006
test d16 T12 ow0.3: acc 0.922  margin 0.257  ±0.004
test d16 T12 ow0.0: acc 0.889  margin 0.230  ±0.004
test d16 T12 ow0.6: acc 0.927  margin 0.254  ±0.005
test d32 T24 ow0.3: acc 0.983  margin 0.367  ±0.002
test d8 T6 ow0.3: acc 0.713  margin 0.074  ±0.009
test d16 T64 K8 ow0.3: acc 0.808  margin 0.145  ±0.009
test d16 T128 K8 ow0.3: acc 0.764  margin 0.121  ±0.013
```

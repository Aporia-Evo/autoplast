# Search seed 1

task: regime collision3  alphabet: 19 ops  readout: evolved  add-node mutation: on  candidates: 300020  real evaluations (after cache): 39137  time: 85s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 8436 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = <tanh(k), tanh(k)>·((v)⊗(tanh(k)) + S)
o = S·q

Effective program (5 instructions):
  V2 = Tanh(V0)
  s0 = Dot(V2, V2)
  M2 = Outer(V1, V2)
  M0 = MatAdd(M2, M0)
  M0 = MatScale(s0, M0)

train acc 0.509
test regime collision3: acc 0.517  margin -0.030
test d16 T12 ow0.3: acc 0.765  margin 0.143
test d16 T12 ow0.0: acc 0.767  margin 0.142
test d16 T12 ow0.6: acc 0.711  margin 0.103
test d32 T24 ow0.3: acc 0.850  margin 0.218
test d8 T6 ow0.3: acc 0.640  margin 0.026
test d16 T64 K8 ow0.3: acc 0.563  margin -0.009
test d16 T128 K8 ow0.3: acc 0.554  margin -0.026
```

# Search seed 4

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 624038  time: 901s  pop: 500  tournament: 10

## Milestones (first candidate count where best train acc reached the reference rule)

- linear attention (acc 0.362): 4724 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): not reached

## Best rule

```
S' = (|tanh(tanh(k))|·(<v, tanh(v)>·v)⊗(tanh(tanh(k))) + <v, tanh(v)>·<v, tanh(v)>·S)

Effective program (11 instructions):
  V2 = Tanh(V1)
  V0 = Tanh(V0)
  V3 = Tanh(V0)
  s0 = Dot(V1, V2)
  V4 = VecScale(s0, V1)
  s1 = SMul(s0, s0)
  M3 = Outer(V4, V3)
  M0 = MatScale(s1, M0)
  s3 = Norm(V3)
  M3 = MatScale(s3, M3)
  M0 = MatAdd(M3, M0)

train acc 0.512
test regime collision3: acc 0.517  margin -0.033
test d16 T12 ow0.3: acc 0.754  margin 0.139
test d16 T12 ow0.0: acc 0.754  margin 0.135
test d16 T12 ow0.6: acc 0.709  margin 0.101
test d32 T24 ow0.3: acc 0.845  margin 0.216
test d8 T6 ow0.3: acc 0.633  margin 0.025
test d16 T64 K8 ow0.3: acc 0.577  margin -0.008
test d16 T128 K8 ow0.3: acc 0.553  margin -0.027
```
